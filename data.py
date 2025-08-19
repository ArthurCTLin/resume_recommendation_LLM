import os
import fitz  # PyMuPDF

def load_text(path):
    file_extension = os.path.splitext(path)[1].lower()

    if file_extension == ".pdf":
        doc = fitz.open(path)
        texts = []
        for page in doc:
            texts.append(page.get_text())
        return "\n".join(texts)    
    elif file_extension == ".txt":
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Only PDF and TXT are supported.")

