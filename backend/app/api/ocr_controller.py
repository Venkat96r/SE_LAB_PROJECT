import os
import json
import uuid
import logging
from fastapi import UploadFile
from typing import Optional, List, Dict, Any

from app.services.services import (
    ExtractionService,
    VerificationService,
)
from app.dto.models import (
    OCRRequest,
    ExtractionResponse,
    VerificationRequest,
    VerificationResult,
)
from app.utils import is_pdf_file

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class OCRController:
    """
    High-level controller that connects FastAPI endpoints with the services layer.

    Responsibilities:
    - Manage UploadFile I/O
    - Dispatch to services
    - No business logic (follows SRP)
    - Implements the design shown in your class diagram
    """

    def __init__(
        self,
        extraction_service: ExtractionService,
        verification_service: VerificationService,
    ):
        self.extraction_service = extraction_service
        self.verification_service = verification_service

    # ------------------------------------------------------------------
    # Extract Single Page
    # ------------------------------------------------------------------
    async def extract(self, file: UploadFile, req: OCRRequest) -> ExtractionResponse:
        file_path = self._save_temp_file(file)
        try:
            response = self.extraction_service.extract_single_page(
                file_path=file_path,
                language=req.language,
                page_number=req.page_number,
                custom_fields=req.fields,
            )

            # Add overlay if requested
            if req.include_detection:
                encoded = self.extraction_service.build_confidence_overlay(
                    file_path, response.detections
                )
                response.confidence_overlay = encoded
                response.has_detection_data = True

            return response
        finally:
            self._cleanup(file_path)

    # ------------------------------------------------------------------
    # Extract All PDF Pages
    # ------------------------------------------------------------------
    async def extract_all_pages(self, file: UploadFile, req: OCRRequest) -> ExtractionResponse:
        file_path = self._save_temp_file(file)
        try:
            if not is_pdf_file(file_path):
                return ExtractionResponse(
                    mapped_fields=None,
                    pages=None,
                    is_pdf=False,
                )

            return self.extraction_service.extract_all_pages(
                file_path=file_path,
                language=req.language,
                custom_fields=req.fields,
            )
        finally:
            self._cleanup(file_path)

    # ------------------------------------------------------------------
    # Detect Only
    # ------------------------------------------------------------------
    async def detect(self, file: UploadFile, req: OCRRequest) -> Dict[str, Any]:
        file_path = self._save_temp_file(file)
        try:
            response = self.extraction_service.extract_single_page(
                file_path=file_path,
                language=req.language,
                page_number=req.page_number,
                custom_fields=req.fields,
            )

            overlay = self.extraction_service.build_confidence_overlay(
                file_path, response.detections
            )

            return {
                "detections": [d.dict() for d in response.detections],
                "total_detections": response.total_detections,
                "confidence_overlay": overlay,
                "processing_info": response.processing_info.dict(),
            }
        finally:
            self._cleanup(file_path)

    # ------------------------------------------------------------------
    # Verify Extracted Fields
    # ------------------------------------------------------------------
    async def verify(self, file: UploadFile, req: VerificationRequest) -> VerificationResult:
        file_path = self._save_temp_file(file)
        try:
            # Step 1: Extract OCR fields without overlay
            extract_resp = self.extraction_service.extract_single_page(
                file_path=file_path,
                language="en",  # Verification default
                page_number=1,
                custom_fields=req.fields,
            )

            extracted_fields = extract_resp.mapped_fields or {}

            # Step 2: Verify
            verified = self.verification_service.verify(
                submitted_data=req.verification_data,
                extracted_fields=extracted_fields,
            )

            return VerificationResult(
                success=True,
                verified_fields=verified,
                details={"page": 1},
            )
        except Exception as e:
            return VerificationResult(
                success=False,
                verified_fields={},
                details={"error": str(e)},
            )
        finally:
            self._cleanup(file_path)

    # ------------------------------------------------------------------
    # Helper: Save UploadFile
    # ------------------------------------------------------------------
    def _save_temp_file(self, file: UploadFile) -> str:
        file_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        with open(temp_path, "wb") as buffer:
            buffer.write(file.file.read())

        logger.info(f"Saved temp file: {temp_path}")
        return temp_path

    # ------------------------------------------------------------------
    # Helper: Cleanup
    # ------------------------------------------------------------------
    def _cleanup(self, file_path: str):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Removed temp file: {file_path}")
            except Exception:
                logger.warning(f"Failed to remove: {file_path}")


__all__ = ["OCRController"]
