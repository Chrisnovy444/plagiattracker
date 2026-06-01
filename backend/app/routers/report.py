"""
Report Router
Generates and retrieves plagiarism detection reports
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
import asyncio

from app.database import get_db
from app.models import User, Document, Report, DocumentStatus
from app.services.extractor import chunk_text
from app.services.plagiat_engine import detect_plagiarism
from app.services.ai_detector import detect_ai_content
from app.services.corrector import generate_correction_report
from app.services.sources.arxiv import search_arxiv
from app.services.sources.openalex import search_openalex
from app.services.sources.crossref import search_crossref
from app.services.sources.semantic_scholar import search_semantic_scholar
from app.services.sources.pubmed import search_pubmed
from app.services.sources.web_scraper import search_web

router = APIRouter()


async def analyze_document(document_id: str, db: Session):
    """Background task to analyze document"""

    document = db.query(Document).filter(Document.id == uuid.UUID(document_id)).first()
    if not document:
        return

    try:
        text = document.extracted_text

        # Extract keywords for search (first 100 words)
        keywords = " ".join(text.split()[:100])

        # Search all sources in parallel (5 academic APIs + web)
        arxiv_results, openalex_results, crossref_results, semantic_results, pubmed_results, web_results = await asyncio.gather(
            search_arxiv(keywords, max_results=3),
            search_openalex(keywords, max_results=3),
            search_crossref(keywords, max_results=3),
            search_semantic_scholar(keywords, max_results=3),
            search_pubmed(keywords, max_results=3),
            search_web(keywords, max_results=2),
            return_exceptions=True
        )

        # Combine all sources (filter out exceptions)
        all_sources = []
        for result in [arxiv_results, openalex_results, crossref_results, semantic_results, pubmed_results, web_results]:
            if isinstance(result, list):
                all_sources.extend(result)
            elif isinstance(result, Exception):
                print(f"Source search error: {result}")

        # Detect plagiarism
        plagiarism_result = detect_plagiarism(text, all_sources)

        # Detect AI content
        ai_result = detect_ai_content(text)

        # Generate corrections
        correction_report = generate_correction_report(
            plagiarism_result["matches"],
            ai_result
        )

        # Create report with highlighted passages
        report = Report(
            document_id=document.id,
            plagiarism_score=plagiarism_result["plagiarism_score"],
            plagiarism_level=plagiarism_result["plagiarism_level"],
            sources_found=plagiarism_result["matches"],
            ai_score=ai_result["ai_score"],
            ai_level=ai_result["ai_level"],
            ai_details=ai_result,
            plagiarism_passages=plagiarism_result.get("highlighted_passages", []),
            ai_passages=ai_result.get("highlighted_ai_passages", []),
            corrections=correction_report,
            processing_time=1.0  # Simplified
        )

        db.add(report)
        document.status = DocumentStatus.COMPLETED.value
        db.commit()

    except Exception as e:
        document.status = DocumentStatus.FAILED.value
        document.error_message = str(e)
        db.commit()


@router.post("/analyze/{document_id}")
async def analyze(
    document_id: str,
    email: EmailStr,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start analysis for a document"""

    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get document
    document = db.query(Document).filter(
        Document.id == uuid.UUID(document_id),
        Document.user_id == user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.status != DocumentStatus.PROCESSING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document is {document.status}"
        )

    # Start background analysis
    background_tasks.add_task(analyze_document, document_id, db)

    return {
        "message": "Analysis started",
        "document_id": document_id,
        "status": "processing"
    }


@router.get("/report/{document_id}")
def get_report(
    document_id: str,
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """Get analysis report for a document"""

    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get document
    document = db.query(Document).filter(
        Document.id == uuid.UUID(document_id),
        Document.user_id == user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Get report
    report = db.query(Report).filter(Report.document_id == document.id).first()

    if not report:
        return {
            "status": document.status,
            "message": "Report not ready yet" if document.status == DocumentStatus.PROCESSING.value else "Report not found"
        }

    return {
        "document_id": str(document.id),
        "filename": document.original_filename,
        "word_count": document.word_count,
        "plagiarism": {
            "score": report.plagiarism_score,
            "level": report.plagiarism_level,
            "sources": report.sources_found,
            "highlighted_passages": report.plagiarism_passages
        },
        "ai_detection": {
            "score": report.ai_score,
            "level": report.ai_level,
            "details": report.ai_details,
            "highlighted_passages": report.ai_passages
        },
        "corrections": report.corrections,
        "created_at": report.created_at,
        "processing_time": report.processing_time
    }
