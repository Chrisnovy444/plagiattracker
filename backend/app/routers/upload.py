"""
Document Upload Router
Handles file upload and text extraction
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import uuid
import os

from app.database import get_db
from app.models import User, Document, DocumentStatus
from app.config import settings
from app.services.extractor import extract_text

router = APIRouter()


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    file_size: int
    status: str
    message: str


def check_user_analyses(user: User) -> bool:
    """Check if user has remaining analyses"""
    if user.analyses_limit == -1:  # Unlimited
        return True

    # Check expiration
    if user.subscription_expires_at and user.subscription_expires_at < datetime.utcnow():
        return False

    return user.analyses_remaining > 0


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    email: EmailStr,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document for plagiarism detection"""

    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check analyses remaining
    if not check_user_analyses(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "No analyses remaining",
                "analyses_remaining": user.analyses_remaining,
                "subscription_expires_at": user.subscription_expires_at,
                "contact": {
                    "email": settings.SUPPORT_EMAIL,
                    "phone": settings.PARTNER_PHONE
                }
            }
        )

    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Validate file size
    content = await file.read()
    file_size = len(content)
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum: {settings.MAX_UPLOAD_SIZE_MB} MB"
        )

    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Save file
    with open(file_path, "wb") as f:
        f.write(content)

    # Create document record
    document = Document(
        user_id=user.id,
        filename=filename,
        original_filename=file.filename,
        file_size=file_size,
        file_type=file_ext,
        file_path=file_path,
        status=DocumentStatus.UPLOADED,
        delete_at=datetime.utcnow() + timedelta(days=30)  # GDPR: delete after 30 days
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Extract text (async task in production, sync for MVP)
    try:
        extracted_text = extract_text(file_path, file_ext)

        if not extracted_text or len(extracted_text) < settings.MIN_TEXT_LENGTH:
            document.status = DocumentStatus.FAILED
            document.error_message = "Could not extract enough text from document"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document contains insufficient text for analysis"
            )

        # Update document with extracted text
        document.extracted_text = extracted_text
        document.word_count = len(extracted_text.split())
        document.status = DocumentStatus.PROCESSING
        document.processed_at = datetime.utcnow()

        # Decrement user analyses
        if user.analyses_limit != -1:  # Not unlimited
            user.analyses_remaining -= 1

        db.commit()
        db.refresh(document)

        return {
            "document_id": str(document.id),
            "filename": document.original_filename,
            "file_size": document.file_size,
            "status": document.status.value,
            "message": "Document uploaded and processing started"
        }

    except Exception as e:
        document.status = DocumentStatus.FAILED
        document.error_message = str(e)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )


@router.get("/document/{document_id}")
def get_document(
    document_id: str,
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """Get document status"""

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

    return {
        "id": str(document.id),
        "filename": document.original_filename,
        "status": document.status.value,
        "word_count": document.word_count,
        "processed_at": document.processed_at,
        "error_message": document.error_message
    }
