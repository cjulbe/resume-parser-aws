from docx import Document
from pypdf import PdfReader


def parse_resume(file_path):
    data = {
    "personal": {},
    "education": [],
    "experience": [],
    "skills": [],
    "projects": []
}
        
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f, strict=False)
            text = ""

            # To preserve internal formatting
            for page in reader.pages:
                extracted = page.extract_text() or ""
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
        if "skills" in lower:
            section = "skills"
            continue
        if "projects" in lower:
            section = "projects"
            continue
        if section:
            if section == "personal":
                # Split the long line into parts
                tokens = line.split()

                # Example fields:
                # ["Name:", "Carlota", "Email:", "carlota@example.com", "Phone:", "+1", "123-456-7890", ...]

                current_key = None
                for token in tokens:
                    if token.endswith(":"):  # New field => key
                        current_key = token[:-1].lower()
                        data["personal"][current_key] = ""
                    else:
                        if current_key:
                            # Add token to the active key
                            if data["personal"][current_key]:
                                data["personal"][current_key] += " " + token
                            else:
                                data["personal"][current_key] = token
            else:
                if line:
                    data[section].append(line)
    
    return data
