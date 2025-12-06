from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from PIL import Image
import numpy as np

# Import existing utilities (these are adapters to your existing functions)
from app.utils import is_pdf_file


class BaseExtractionModule(ABC):
    """Abstract base class for language-specific OCR extraction modules.

    Each concrete module must implement `extract` which accepts a PIL Image and returns
    a standardized dict with keys: txts (list), scores (list), boxes (list), lang_type (str), elapse (float)
    This preserves compatibility with the existing `engine(image)` result used elsewhere.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract(self, image: Image.Image) -> Dict[str, Any]:
        """Run OCR on the provided PIL image and return a result-like dict/object.

        The returned object should mirror the fields expected by the rest of the codebase
        (txts, scores, boxes, lang_type, elapse).
        """
        raise NotImplementedError


class LatinExtractionModule(BaseExtractionModule):
    """Extraction module for Latin-script languages (English, etc.)

    This module is a thin adapter around the PHOCR or other engine configured for Latin.
    """

    def __init__(self, engine):
        super().__init__("latin")
        self.engine = engine

    def extract(self, image: Image.Image) -> Dict[str, Any]:
        # Delegates to the provided engine and returns a normalized structure
        result = self.engine(image)
        return {
            "txts": list(result.txts) if hasattr(result, 'txts') else [],
            "scores": list(result.scores) if hasattr(result, 'scores') else [],
            "boxes": result.boxes.tolist() if hasattr(result, 'boxes') and result.boxes is not None else [],
            "lang_type": getattr(result, 'lang_type', 'en'),
            "elapse": getattr(result, 'elapse', 0.0),
            "raw": result
        }


class ChineseExtractionModule(BaseExtractionModule):
    def __init__(self, engine):
        super().__init__("ch")
        self.engine = engine

    def extract(self, image: Image.Image) -> Dict[str, Any]:
        result = self.engine(image)
        return {
            "txts": list(result.txts) if hasattr(result, 'txts') else [],
            "scores": list(result.scores) if hasattr(result, 'scores') else [],
            "boxes": result.boxes.tolist() if hasattr(result, 'boxes') and result.boxes is not None else [],
            "lang_type": getattr(result, 'lang_type', 'ch'),
            "elapse": getattr(result, 'elapse', 0.0),
            "raw": result
        }


class JapaneseExtractionModule(BaseExtractionModule):
    def __init__(self, engine):
        super().__init__("ja")
        self.engine = engine

    def extract(self, image: Image.Image) -> Dict[str, Any]:
        result = self.engine(image)
        return {
            "txts": list(result.txts) if hasattr(result, 'txts') else [],
            "scores": list(result.scores) if hasattr(result, 'scores') else [],
            "boxes": result.boxes.tolist() if hasattr(result, 'boxes') and result.boxes is not None else [],
            "lang_type": getattr(result, 'lang_type', 'ja'),
            "elapse": getattr(result, 'elapse', 0.0),
            "raw": result
        }


class KoreanExtractionModule(BaseExtractionModule):
    def __init__(self, engine):
        super().__init__("ko")
        self.engine = engine

    def extract(self, image: Image.Image) -> Dict[str, Any]:
        result = self.engine(image)
        return {
            "txts": list(result.txts) if hasattr(result, 'txts') else [],
            "scores": list(result.scores) if hasattr(result, 'scores') else [],
            "boxes": result.boxes.tolist() if hasattr(result, 'boxes') and result.boxes is not None else [],
            "lang_type": getattr(result, 'lang_type', 'ko'),
            "elapse": getattr(result, 'elapse', 0.0),
            "raw": result
        }


class ExtractionModuleFactory:
    """Factory to provide the correct extraction module for a language code."""

    def __init__(self, engine_map: Optional[Dict[str, Any]] = None):
        # engine_map: mapping from lang code -> engine instance
        self.engine_map = engine_map or {}

    def register(self, lang: str, engine: Any):
        self.engine_map[lang] = engine

    def get_module(self, lang: str) -> BaseExtractionModule:
        lang = (lang or "").lower()
        if lang in ("en", "en_us", "en_gb", "latin"):
            return LatinExtractionModule(self.engine_map.get('en'))
        if lang in ("ch", "zh", "zh_cn", "chinese"):
            return ChineseExtractionModule(self.engine_map.get('ch'))
        if lang in ("ja", "jp", "japanese"):
            return JapaneseExtractionModule(self.engine_map.get('ja'))
        if lang in ("ko", "kr", "korean"):
            return KoreanExtractionModule(self.engine_map.get('ko'))
        # default
        return LatinExtractionModule(self.engine_map.get('en'))


__all__ = [
    "BaseExtractionModule",
    "LatinExtractionModule",
    "ChineseExtractionModule",
    "JapaneseExtractionModule",
    "KoreanExtractionModule",
    "ExtractionModuleFactory",
]
