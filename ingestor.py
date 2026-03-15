import fitz  # PyMuPDF

def process_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # Split by double newlines or a fixed character count to create chunks
    # This satisfies the "Manageable segments/chunks" requirement
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    return chunks
