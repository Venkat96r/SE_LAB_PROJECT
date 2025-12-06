import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json

# OCR engine
from phocr import PHOCR

# Controller
from app.api.ocr_controller import OCRController

# Services
from app.services.services import (
    ExtractionService,
    VerificationService,
    PreprocessingService,
    QualityService,
)

# OCR module factory
from app.ocr_modules.modules import ExtractionModuleFactory

# LLM integration
from app.llm_integration.llm import ExternalOllamaAPI, QwenFieldMapper

# DTOs
from app.dto.models import OCRRequest, VerificationRequest, ExtractionResponse, VerificationResult


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# FastAPI initialization
# -----------------------------------------------------------------------------
app = FastAPI(title="Multilingual OCR Extraction & Verification API - OOP Version")

origins = [
    "http://127.0.0.1:5500", "http://localhost:5500",
    "http://127.0.0.1:3000", "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# DEPENDENCY INJECTION (Manual — Option A)
# =============================================================================

# Shared PHOCR engine
phocr_engine = PHOCR()

# Build OCR module factory
module_factory = ExtractionModuleFactory()
module_factory.register('en', phocr_engine)
module_factory.register('ch', phocr_engine)
module_factory.register('ja', phocr_engine)
module_factory.register('ko', phocr_engine)

# Instantiate services
preprocessor = PreprocessingService()
quality_service = QualityService()

# LLM API + Mapper
llm_api = ExternalOllamaAPI(api_url="http://127.0.0.1:8001/extract")
field_mapper = QwenFieldMapper(llm_api)

# Core extraction and verification services
extraction_service = ExtractionService(
    module_factory=module_factory,
    preprocessor=preprocessor,
    quality_service=quality_service,
    field_mapper=field_mapper,
)

verification_service = VerificationService()

# Controller
controller = OCRController(
    extraction_service=extraction_service,
    verification_service=verification_service,
)


# =============================================================================
# FASTAPI ENDPOINTS → Controller Delegation
# =============================================================================

@app.post("/extract", response_model=ExtractionResponse)
async def extract(
    document: UploadFile = File(...),
    include_detection: str = Form(default="false"),
    page_number: int = Form(default=1),
    language: str = Form(default="en"),
    fields: str = Form(default="")
):
    """Single-page OCR extraction."""
    custom_fields = json.loads(fields) if fields.strip() else None

    req = OCRRequest(
        include_detection=(include_detection.lower() == "true"),
        page_number=page_number,
        language=language.lower(),
        fields=custom_fields
    )
    return await controller.extract(document, req)


@app.post("/extract/pdf/all", response_model=ExtractionResponse)
async def extract_pdf_all(
    document: UploadFile = File(...),
    language: str = Form(default="en"),
    fields: str = Form(default="")
):
    """Multi-page PDF extraction."""
    custom_fields = json.loads(fields) if fields.strip() else None

    req = OCRRequest(
        include_detection=False,
        page_number=1,
        language=language.lower(),
        fields=custom_fields
    )
    return await controller.extract_all_pages(document, req)


@app.post("/detect")
async def detect(
    document: UploadFile = File(...),
    page_number: int = Form(default=1),
    language: str = Form(default="en"),
    fields: str = Form(default="")
):
    """Detect regions + confidence overlay."""
    custom_fields = json.loads(fields) if fields.strip() else None

    req = OCRRequest(
        include_detection=True,
        page_number=page_number,
        language=language.lower(),
        fields=custom_fields
    )
    return await controller.detect(document, req)


@app.post("/verify", response_model=VerificationResult)
async def verify(
    document: UploadFile = File(...),
    verification_data: str = Form(...),
    fields: str = Form(default="")
):
    """Field verification."""
    custom_fields = json.loads(fields) if fields.strip() else None

    req = VerificationRequest(
        verification_data=json.loads(verification_data),
        fields=custom_fields
    )
    return await controller.verify(document, req)


@app.get("/health")
async def health():
    """Health-check endpoint."""
    return {
        "status": "healthy",
        "modules": ["extraction", "verification", "quality", "llm_mapper"],
        "languages_supported": ["en", "ch", "ja", "ko"],
        "engines": "PHOCR (shared for all languages)"
    }


# =============================================================================
# Root Endpoint
# =============================================================================
@app.get("/")
async def root():
    return {
        "message": "OCR Extraction API (OOP Architecture)",
        "version": "5.0",
        "features": [
            "OCR extraction",
            "PDF multipage support",
            "Verification",
            "LLM field mapping",
            "Confidence overlays",
        ]
    }
