"""
Text Extraction Service
Extracts text from PDF, DOCX, and TXT files
"""
import PyMuPDF  # pymupdf
import docx
from typing import Optional


def extract_text(file_path: str, file_type: str) -> Optional[str]:
    """
    Extract text from document

    Args:
        file_path: Path to the file
        file_type: File extension (pdf, docx, txt)

    Returns:
        Extracted text or None
    """

    try:
        if file_type == "pdf":
            return extract_pdf(file_path)
        elif file_type == "docx":
            return extract_docx(file_path)
        elif file_type == "txt":
            return extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    except Exception as e:
        raise Exception(f"Error extracting text from {file_type}: {str(e)}")


def extract_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF"""

    text = []

    with PyMuPDF.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text())

    return "\n\n".join(text).strip()


def extract_docx(file_path: str) -> str:
    """Extract text from DOCX using python-docx"""

    doc = docx.Document(file_path)

    text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n\n".join(text).strip()


def extract_txt(file_path: str) -> str:
    """Extract text from TXT file"""

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for analysis

    Args:
        text: Full text to split
        chunk_size: Number of words per chunk
        overlap: Number of overlapping words between chunks

    Returns:
        List of text chunks
    """

    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks
