import logging
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import os
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ExternalOllamaAPI  (Adapter Pattern)
# ---------------------------------------------------------------------------
class ExternalOllamaAPI:
    """
    Handles communication with the external LLM-based extraction API.
    This class abstracts HTTP details and keeps the mapper clean.
    """

    def __init__(self, api_url = "http://127.0.0.1:11434"):
        load_dotenv()
        base_url = os.getenv("NOTEBOOK_URL", "http://127.0.0.1:11434")

        # notebook provides /extract
        self.api_url = f"{base_url}/extract"

        print("LLM API URL being used:", self.api_url)

    def extract_fields(self, text: str, custom_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        payload = {"text": text}
        if custom_fields:
            payload["fields"] = custom_fields

        try:
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true",
            }

            response = requests.post(self.api_url, json=payload, headers=headers, timeout=120)
            if response.status_code == 200:
                return response.json()

            logger.error(f"LLM API returned {response.status_code}: {response.text}")
            return {}

        except Exception as e:
            logger.error(f"LLM API request failed: {e}")
            return {}


# ---------------------------------------------------------------------------
# QwenFieldMapper (uses ExternalOllamaAPI)
# ---------------------------------------------------------------------------
class QwenFieldMapper:
    """
    Converts raw OCR text into structured fields using LLM assistance.
    This class remains very similar to your original logic but refactored OOP.
    """

    def __init__(self, llm_api: ExternalOllamaAPI):
        self.llm = llm_api

    def map_fields(self, text: str, custom_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        if not text.strip():
            logger.warning("No OCR text provided to LLM mapper.")
            return {}

        result = self.llm.extract_fields(text, custom_fields)

        if not isinstance(result, dict):
            logger.error("LLM API returned invalid result format.")
            return {}

        return result


__all__ = [
    "ExternalOllamaAPI",
    "QwenFieldMapper",
]
