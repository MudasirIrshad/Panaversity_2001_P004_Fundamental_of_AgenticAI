import pytesseract
from PIL import Image

from agents import function_tool
# Give full path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_url: str) :
    """Extract text from an image using Tesseract OCR."""
    text = pytesseract.image_to_string(Image.open(image_url))
    return text

@function_tool
def summary_tool(image_path: str):
    """Extract text from an image and summarize it."""
    print("Called the function")

    text = extract_text(image_path)

    return f"{text} now summarize this text."

