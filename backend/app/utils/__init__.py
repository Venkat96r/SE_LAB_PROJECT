import os

def is_pdf_file(filename: str) -> bool:
    """Check if the given filename is a PDF file by extension."""
    return os.path.splitext(filename)[1].lower() == ".pdf"

# Placeholder implementations for other expected utils

def convert_pdf_to_image(pdf_path: str):
    raise NotImplementedError("convert_pdf_to_image is not implemented.")

def convert_pdf_to_images(pdf_path: str):
    raise NotImplementedError("convert_pdf_to_images is not implemented.")

def save_image_temporarily(image):
    raise NotImplementedError("save_image_temporarily is not implemented.")
