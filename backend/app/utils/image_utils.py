import numpy as np
from PIL import Image


class OCRUtils:
    """
    Utility class for OCR-related operations:
    - Safe float conversion
    - Bounding box normalization
    - Confidence level mapping
    - Deskew placeholder (kept simple because PHOCR handles rotation)
    """

    # ----------------------------
    # SAFE FLOAT CONVERSION
    # ----------------------------
    @staticmethod
    def safe_float_conversion(value):
        """Convert a value to float safely, fallback = 0.0"""
        try:
            return float(value)
        except Exception:
            return 0.0

    # ----------------------------
    # PROCESS BOUNDING BOX
    # ----------------------------
    @staticmethod
    def process_bounding_box(box):
        """
        Normalize bounding boxes into:
        {
            "x1": min_x,
            "y1": min_y,
            "x2": max_x,
            "y2": max_y
        }
        
        Accepts:
        - Four corner points: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        - Flat list/tuple: [x1, y1, x2, y2]
        - Anything else → fallback default box
        """

        # Case 1: Box is list of 4 points
        if (
            isinstance(box, (list, tuple))
            and len(box) >= 4
            and all(isinstance(pt, (list, tuple)) and len(pt) == 2 for pt in box)
        ):
            xs = [OCRUtils.safe_float_conversion(pt[0]) for pt in box]
            ys = [OCRUtils.safe_float_conversion(pt[1]) for pt in box]
            return {
                "x1": min(xs),
                "y1": min(ys),
                "x2": max(xs),
                "y2": max(ys),
            }

        # Case 2: Flat box → 4 numeric values
        if (
            isinstance(box, (list, tuple))
            and len(box) == 4
            and all(isinstance(v, (int, float)) for v in box)
        ):
            x1, y1, x2, y2 = map(float, box)
            return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

        # Invalid → fallback box
        return {"x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0}

    # ----------------------------
    # CONFIDENCE LEVEL MAPPING
    # ----------------------------
    @staticmethod
    def get_confidence_level(c):
        """Map numeric confidence → category label"""
        c = OCRUtils.safe_float_conversion(c)
        if c >= 0.9:
            return "high"
        if c >= 0.7:
            return "medium"
        if c >= 0.5:
            return "low"
        return "very_low"

    # ----------------------------
    # DESKEW IMAGE (placeholder)
    # ----------------------------
    @staticmethod
    def deskew_image(image: Image.Image):
        """
        Placeholder deskew.
        PHOCR already handles text orientation internally.
        So we keep exact same behavior as your original code: return image as is.
        """
        return image
