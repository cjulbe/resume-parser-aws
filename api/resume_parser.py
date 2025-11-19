from docx import Document
from pypdf import PdfReader


def parse_resume(file_path):
    data = {"personal": {}, "education": [], "experience": []}
        
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ""

            # To preserve internal formatting
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n" 
    else:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

    # Dummy parser: assumes Harvard template with sections
    lines = text.splitlines()
    section = None
    
    for line in lines:
        line = line.strip()
        lower = line.lower()
        if "education" in lower:
            section = "education"
            continue
        if "experience" in lower:
            section = "experience"
            continue
        if "personal" in lower or "contact" in lower:
            section = "personal"
            continue
        if section:
            if section == "personal":
                key_val = line.split(":", 1)
                if len(key_val) == 2:
                    data["personal"][key_val[0].strip()] = key_val[1].strip()
            else:
                if line:
                    data[section].append(line)
    
    return data
