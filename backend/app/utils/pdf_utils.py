import PyPDF2
from pdf2image import convert_from_path

def is_pdf_file(path):
    return path.lower().endswith(".pdf")

def get_pdf_page_count(path):
    reader = PyPDF2.PdfReader(path)
    return len(reader.pages)

def convert_pdf_to_image(path, page=1, dpi=200):
    return convert_from_path(path, dpi=dpi)[0]