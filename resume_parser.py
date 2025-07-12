import pdfplumber

def extract_info_from_resume(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Simple keyword extraction logic — customize this further
    keywords = extract_keywords(text)

    resume_data = {
        "keywords": keywords,
        "raw_text": text
    }

    return resume_data

def extract_keywords(text):
    # Dummy keyword extractor (replace with real NLP if needed)
    skills_list = ["Python", "Java", "Machine Learning", "SQL", "C++", "React", "Flask", "TensorFlow"]
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found
