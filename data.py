import os
import pdfplumber

def load_text(path):
    file_extension = os.path.splitext(path)[1].lower()

    if file_extension == ".pdf":
        texts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                texts.append(page.extract_text() or "")
        return "\n".join(texts)
    
    elif file_extension == ".txt":
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Only PDF and TXT are supported.")

