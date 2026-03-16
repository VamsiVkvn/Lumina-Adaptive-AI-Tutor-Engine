import fitz  # PyMuPDF
from fastapi import UploadFile

async def extract_text(file: UploadFile):
    # Read the uploaded file into memory
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def create_chunks(text: str, chunk_size: int = 1000):
    # Simple chunking logic
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
