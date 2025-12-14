import re


class TextFieldExtractor:
    """
    Utility class for extracting structured text fields from OCR output.
    Provides:
    - Email extraction
    - Phone extraction
    - Age extraction
    - Normalization helpers
    """

    # ----------------------------
    # EMAIL
    # ----------------------------
    @staticmethod
    def extract_email(text: str):
        """Extracts the first valid email from OCR text."""
        if not text:
            return None

        regex = r"[\w\.-]+@[\w\.-]+\.\w+"
        match = re.search(regex, text)
        return match.group(0).strip() if match else None

    # ----------------------------
    # PHONE NUMBER
    # ----------------------------
    @staticmethod
    def extract_phone(text: str):
        """
        Extract phone numbers in formats:
        - +91 9876543210
        - (123) 456-7890
        - 987-654-3210
        - 9876543210
        """
        if not text:
            return None

        regex = r"(\+?\d[\d\s\-\(\)]{6,}\d)"
        match = re.search(regex, text)
        return match.group(1).strip() if match else None

    # ----------------------------
    # AGE
    # ----------------------------
    @staticmethod
    def extract_age(text: str):
        """
        Extracts numbers likely to represent age (1–3 digits).
        Handles formats like:
        - "Age: 25"
        - "25 yrs"
        - "25 y/o"
        """
        if not text:
            return None

        regex = r"\b(\d{1,3})\b"
        match = re.search(regex, text)
        return match.group(1) if match else None

    # ----------------------------
    # NORMALIZATION
    # ----------------------------
    @staticmethod
    def normalize_value(value: str):
        """
        Clean extra punctuation, trailing spaces, and OCR artifacts.
        """
        if not value:
            return value
        return value.strip(" \t\n\r:;,.-")
