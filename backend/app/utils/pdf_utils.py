import os
import uuid
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image


class PDFUtils:
    """
    Utility class for handling PDF operations:
    - PDF validation
    - Page count
    - Convert single page to image
    - Convert all pages to images
    - Save images temporarily
    """

    @staticmethod
    def is_pdf_file(path: str) -> bool:
        """Check if the given file is a PDF."""
        return path.lower().endswith(".pdf")

    @staticmethod
    def get_pdf_page_count(path: str) -> int:
        """Return number of pages in a PDF file."""
        try:
            reader = PyPDF2.PdfReader(path)
            return len(reader.pages)
        except Exception:
            return 0  # Avoid backend crash

    @staticmethod
    def convert_pdf_to_image(path: str, page_number: int = 1, dpi: int = 200) -> Image.Image:
        """
        Convert a specific PDF page to a PIL image.
        
        page_number is 1-indexed (1 = first page)
        """
        try:
            images = convert_from_path(path, dpi=dpi, first_page=page_number, last_page=page_number)
            return images[0]
        except Exception:
            raise RuntimeError(f"Failed to convert PDF page {page_number} to image")

    @staticmethod
    def convert_pdf_to_images(path: str, dpi: int = 200) -> list:
        """Convert all pages in a PDF to a list of PIL images."""
        try:
            return convert_from_path(path, dpi=dpi)
        except Exception:
            raise RuntimeError("Failed to convert PDF to images")

    @staticmethod
    def save_image_temporarily(image: Image.Image, suffix: str = ".jpg") -> str:
        """
        Save a PIL image temporarily to disk and return the file path.
        Caller must delete after use.
        """
        filename = f"temp_{uuid.uuid4().hex}{suffix}"
        temp_path = os.path.join("uploads", filename)

        # Ensure upload folder exists
        os.makedirs("uploads", exist_ok=True)

        image.save(temp_path)
        return temp_path
