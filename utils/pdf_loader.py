# utils/pdf_loader.py
# Loads FAQ content from PDF knowledge base

import PyPDF2
import os

def load_pdf_content(pdf_path):
    """
    Load and extract text from PDF FAQ file
    Returns extracted text or empty string if file not found
    """
    if not os.path.exists(pdf_path):
        return ""
    
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception:
        return ""

def get_faq_context(pdf_path):
    """
    Get FAQ content to include in system context
    """
    content = load_pdf_content(pdf_path)
    if content:
        return f"\n\nKnowledge Base FAQs:\n{content}"
    return ""