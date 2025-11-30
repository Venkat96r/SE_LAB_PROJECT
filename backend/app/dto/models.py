from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Detection(BaseModel):
    """Represents a single text detection region produced by OCR.

    polygon: original polygon coordinates returned by the OCR engine (list of floats or nested lists)
    bbox: normalized bounding-box dict with keys x1,y1,x2,y2 (floats)
    text: the detected text string
    confidence: numeric confidence score (0.0 - 1.0)
    confidence_level: one of ('very_low','low','medium','high')
    """
    polygon: Optional[List[Any]] = Field(default_factory=list)
    bbox: Dict[str, float] = Field(default_factory=lambda: {"x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0})
    text: str = ""
    confidence: float = 0.0
    confidence_level: str = "very_low"


class OCRRequest(BaseModel):
    """DTO representing incoming OCR request parameters.

    document: not included here because FastAPI receives UploadFile separately; this DTO holds
    metadata used by controller/service layer.
    """
    include_detection: bool = False
    page_number: int = 1
    language: str = "en"
    fields: Optional[List[str]] = None  # custom fields to extract


class ExtractionProcessingInfo(BaseModel):
    language: str = "en"
    elapsed_time: float = 0.0
    page_number: int = 1
    is_pdf: bool = False
    custom_fields_used: int = 0


class ExtractionPageResult(BaseModel):
    page_number: int
    text: Optional[str] = ""
    detections: List[Detection] = Field(default_factory=list)
    mapped_fields: Optional[Dict[str, Any]] = None
    processing_info: Optional[ExtractionProcessingInfo] = None


class ExtractionResponse(BaseModel):
    """Top-level extraction response returned by /extract or /extract/pdf/all endpoints.

    When a single page is requested, pages will contain one entry keyed by page number.
    For multi-page extraction, pages contains entries for each processed page.
    """
    mapped_fields: Optional[Dict[str, Any]] = None
    detections: List[Detection] = Field(default_factory=list)
    total_detections: int = 0
    confidence_overlay: Optional[str] = None  # base64 PNG
    has_detection_data: bool = False
    processing_info: Optional[ExtractionProcessingInfo] = None
    pages: Optional[Dict[str, ExtractionPageResult]] = None
    is_pdf: bool = False


class VerificationRequest(BaseModel):
    """Structure used by verify endpoint for submitted verification data."""
    verification_data: Dict[str, Any]
    fields: Optional[List[str]] = None


class VerificationResult(BaseModel):
    success: bool = True
    verified_fields: Dict[str, Any] = Field(default_factory=dict)
    details: Optional[Dict[str, Any]] = None


# Convenience exports
__all__ = [
    "Detection",
    "OCRRequest",
    "ExtractionResponse",
    "ExtractionPageResult",
    "ExtractionProcessingInfo",
    "VerificationRequest",
    "VerificationResult",
]
