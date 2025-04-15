import re
import docx2txt
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        return text
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        return ''

def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group() if match else ''

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3})?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}', text)
    return match.group() if match else ''

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return ''

def extract_skills(text):
    keywords = ['python', 'java', 'sql', 'html', 'css', 'javascript', 'react', 'node', 'excel']
    text = text.lower()
    found = [skill for skill in keywords if skill in text]
    return list(set(found))

def parse_resume(file_path):
    text = extract_text(file_path)
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text)
    }
