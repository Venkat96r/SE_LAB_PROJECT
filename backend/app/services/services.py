import os
import io
import base64
import logging
from typing import Dict, Any, List, Optional
from PIL import Image

# Utilities (existing functions reused without modification)
from app.utils import (
    is_pdf_file,
    convert_pdf_to_image,
    convert_pdf_to_images,
    save_image_temporarily,
)
from app.utils.image_utils import deskew_image, process_bounding_box, get_confidence_level, safe_float_conversion
from app.dto.models import (
    Detection,
    ExtractionProcessingInfo,
    ExtractionPageResult,
    ExtractionResponse,
)
from app.llm_integration.llm import QwenFieldMapper
from app.ocr_modules.modules import BaseExtractionModule, ExtractionModuleFactory

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# PreprocessingService (SOLID — Single Responsibility)
# ----------------------------------------------------------------------------
class PreprocessingService:
    """Handles image pre-processing such as deskewing and conversions.
    This service is intentionally small to follow SRP.
    """

    def preprocess(self, image: Image.Image) -> Image.Image:
        try:
            corrected_img, angle = deskew_image(image)
            logger.info(f"Deskew angle: {angle}")
            return corrected_img
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return image


# ----------------------------------------------------------------------------
# QualityService — (SRP) only checks quality and gives suggestions
# ----------------------------------------------------------------------------
class QualityService:
    def analyze(self, file_path: str) -> Dict[str, Any]:
        # Placeholder: you may integrate your existing quality checks.
        # For now, keep minimal to preserve functionality.
        return {"score": 100, "issues": [], "suggestions": []}


# ----------------------------------------------------------------------------
# ExtractionService — Core Orchestrator for OCR Extraction
# Follows Strategy Pattern + DIP (depends on abstractions, not implementations)
# ----------------------------------------------------------------------------
class ExtractionService:
    def __init__(
        self,
        module_factory: ExtractionModuleFactory,
        preprocessor: PreprocessingService,
        quality_service: QualityService,
        field_mapper: QwenFieldMapper,
    ):
        self.module_factory = module_factory
        self.preprocessor = preprocessor
        self.quality_service = quality_service
        self.field_mapper = field_mapper

    # ----------------------------
    # Extract SINGLE PAGE
    # ----------------------------
    def extract_single_page(
        self, file_path: str, language: str, page_number: int, custom_fields: Optional[List[str]]
    ) -> ExtractionResponse:
        logger.info(f"Extracting single page: page={page_number}, lang={language}")

        is_pdf = is_pdf_file(file_path)
        if is_pdf:
            image = convert_pdf_to_image(file_path, page_number, 200)
        else:
            image = Image.open(file_path).convert("RGB")

        # Preprocessing
        processed_image = self.preprocessor.preprocess(image)

        # OCR module selection (Strategy)
        module = self.module_factory.get_module(language)
        ocr_result = module.extract(processed_image)

        # Parse OCR detections into DTOs
        detections = []
        texts = ocr_result.get("txts", [])
        scores = ocr_result.get("scores", [])
        boxes = ocr_result.get("boxes", [])

        for i in range(min(len(texts), len(scores), len(boxes))):
            text_val = str(texts[i])
            score_val = safe_float_conversion(scores[i])
            bbox = process_bounding_box(boxes[i])
            lvl = get_confidence_level(score_val)

            detections.append(
                Detection(
                    text=text_val,
                    confidence=score_val,
                    bbox=bbox,
                    polygon=boxes[i],
                    confidence_level=lvl,
                )
            )

        # Full text for LLM field mapping
        full_text = " ".join([d.text for d in detections])

        # Call LLM mapper
        mapped_fields = self.field_mapper.map_fields(full_text, custom_fields)

        # Build processing info
        info = ExtractionProcessingInfo(
            language=language,
            elapsed_time=ocr_result.get("elapse", 0.0),
            page_number=page_number,
            is_pdf=is_pdf,
            custom_fields_used=len(custom_fields or []),
        )

        # Final response
        return ExtractionResponse(
            mapped_fields=mapped_fields,
            detections=detections,
            total_detections=len(detections),
            has_detection_data=True,
            processing_info=info,
            is_pdf=is_pdf,
        )

    # ----------------------------
    # Extract MULTIPAGE PDF
    # ----------------------------
    def extract_all_pages(
        self, file_path: str, language: str, custom_fields: Optional[List[str]]
    ) -> ExtractionResponse:
        images = convert_pdf_to_images(file_path, dpi=200)
        pages: Dict[str, ExtractionPageResult] = {}

        for page_num, image in enumerate(images, start=1):
            temp = save_image_temporarily(image, suffix='.png')
            page_res = self.extract_single_page(
                temp, language, page_num, custom_fields
            )

            pages[str(page_num)] = ExtractionPageResult(
                page_number=page_num,
                text="" if not page_res.mapped_fields else None,
                detections=page_res.detections,
                mapped_fields=page_res.mapped_fields,
                processing_info=page_res.processing_info,
            )

            os.remove(temp)

        return ExtractionResponse(
            pages=pages,
            is_pdf=True,
        )

    # ----------------------------
    # Build overlay (preserves your original functionality)
    # ----------------------------
    def build_confidence_overlay(
        self, file_path: str, detections: List[Detection]
    ) -> Optional[str]:
        try:
            if is_pdf_file(file_path):
                image = convert_pdf_to_image(file_path, page_number=1, dpi=200)
            else:
                image = Image.open(file_path).convert("RGB")

            import PIL.ImageDraw as ImageDraw
            import PIL.ImageFont as ImageFont
            overlay = image.copy().convert("RGBA")
            draw = ImageDraw.Draw(overlay)

            colors = {
                "high": (34, 197, 94, 120),
                "medium": (251, 191, 36, 120),
                "low": (239, 68, 68, 120),
                "very_low": (107, 114, 128, 120),
            }

            font = ImageFont.load_default()

            for d in detections:
                bbox = d.bbox
                color = colors[d.confidence_level]
                draw.rectangle(
                    [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]],
                    outline=color[:3], width=3
                )
                draw.rectangle(
                    [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]], fill=color
                )
                draw.text((bbox["x1"] + 2, bbox["y1"] - 20), f"{d.confidence:.2f}", fill=(255,255,255), font=font)

            buf = io.BytesIO()
            overlay.convert("RGB").save(buf, format='PNG')
            return base64.b64encode(buf.getvalue()).decode()

        except Exception as e:
            logger.error(f"Error building overlay: {e}")
            return None


# ----------------------------------------------------------------------------
# VerificationService
# ----------------------------------------------------------------------------
class VerificationService:
    """Compares submitted fields with OCR-extracted fields (LLM + heuristics)."""

    def verify(
        self,
        submitted_data: Dict[str, Any],
        extracted_fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            verified = {}
            for key, sub_value in submitted_data.items():
                extracted = extracted_fields.get(key, {})
                verified[key] = {
                    "submitted": sub_value,
                    "extracted": extracted.get("value"),
                    "confidence": extracted.get("confidence"),
                    "match": str(sub_value).lower() == str(extracted.get("value", "")).lower(),
                }
            return verified
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {"error": str(e)}


__all__ = [
    "PreprocessingService",
    "QualityService",
    "ExtractionService",
    "VerificationService",
]
