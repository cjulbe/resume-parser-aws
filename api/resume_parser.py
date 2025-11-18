from docx import Document
import PyPDF2

def parse_resume(file_path):
    data = {"personal": {}, "education": [], "experience": []}
    
    print("DEBUG: Parsing file:", file_path)
    
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""

            # To preserve internal formatting
            for i, page in reader.pages:
                extracted = page.extract_text()
                print(f"DEBUG: Extracted from page {i}:", repr(extracted))
                if extracted:
                    text += extracted + "\n" 
    else:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

    print("DEBUG: FINAL TEXT =")
    print("----------------------------------------------------------")
    print(text)
    print("----------------------------------------------------------")

    # Dummy parser: assumes Harvard template with sections
    lines = text.splitlines()
    section = None
    
    for line in lines:
        line = line.strip()
        lower = line.lower()
        if "Education" in lower:
            section = "education"
            continue
        if "Experience" in lower:
            section = "experience"
            continue
        if "Personal" in lower or "Contact" in lower:
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
