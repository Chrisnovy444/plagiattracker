"""
SQLAlchemy models for PLAGIATTRACKER
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database import Base


class PlanType(str, enum.Enum):
    """Subscription plan types"""
    TRIAL = "trial"
    STUDENT = "student"
    TEACHER = "teacher"
    RESEARCHER = "researcher"
    INSTITUTION = "institution"


class CodeStatus(str, enum.Enum):
    """Activation code statuses"""
    ACTIVE = "active"
    USED = "used"
    EXPIRED = "expired"
    REVOKED = "revoked"


class DocumentStatus(str, enum.Enum):
    """Document processing statuses"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))

    # Subscription info
    plan_type = Column(Enum(PlanType), default=PlanType.TRIAL)
    analyses_remaining = Column(Integer, default=3)
    analyses_limit = Column(Integer, default=3)
    subscription_expires_at = Column(DateTime, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # User settings (API keys stored encrypted)
    settings = Column(JSON, default={})

    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    activation_codes = relationship("ActivationCode", back_populates="user")


class ActivationCode(Base):
    """Activation code model"""
    __tablename__ = "activation_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, index=True, nullable=False)

    # Plan details
    plan_type = Column(Enum(PlanType), nullable=False)
    analyses_limit = Column(Integer, nullable=False)
    validity_days = Column(Integer, nullable=False)

    # Status
    status = Column(Enum(CodeStatus), default=CodeStatus.ACTIVE, index=True)

    # Usage tracking
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    activated_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(255))  # Admin user who generated it
    notes = Column(Text)  # Admin notes

    # Relationships
    user = relationship("User", back_populates="activation_codes")


class Document(Base):
    """Document model"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # File info
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer)  # bytes
    file_type = Column(String(50))  # pdf, docx, txt
    file_path = Column(String(500))  # Storage path

    # Processing
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADED, index=True)
    extracted_text = Column(Text)
    word_count = Column(Integer)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Auto-delete after 30 days (GDPR compliance)
    delete_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="documents")
    report = relationship("Report", back_populates="document", uselist=False, cascade="all, delete-orphan")


class Report(Base):
    """Analysis report model"""
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), unique=True, nullable=False)

    # Plagiarism scores
    plagiarism_score = Column(Float, default=0.0)  # 0-100
    plagiarism_level = Column(String(20))  # low, medium, high
    sources_found = Column(JSON, default=[])  # List of sources

    # AI detection scores
    ai_score = Column(Float, default=0.0)  # 0-100
    ai_level = Column(String(20))  # low, medium, high
    ai_details = Column(JSON, default={})  # Per-section analysis

    # Detailed findings
    plagiarism_passages = Column(JSON, default=[])  # Highlighted passages
    ai_passages = Column(JSON, default=[])  # AI-detected passages

    # Corrections (if requested)
    corrections_applied = Column(Boolean, default=False)
    corrections = Column(JSON, default={})

    # Report generation
    pdf_path = Column(String(500), nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)  # seconds

    # Cache key for API responses
    cache_key = Column(String(64), index=True)

    # Relationships
    document = relationship("Document", back_populates="report")


class AuditLog(Base):
    """Audit log for tracking all actions"""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Action details
    action = Column(String(100), index=True)  # upload, analyze, activate_code, etc.
    resource_type = Column(String(50))  # document, code, user
    resource_id = Column(UUID(as_uuid=True), nullable=True)

    # Request details
    ip_address = Column(String(50))
    user_agent = Column(String(500))

    # Result
    status = Column(String(20))  # success, failure
    error_message = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON, default={})


# Indexes for performance
from sqlalchemy import Index

Index("idx_documents_user_created", Document.user_id, Document.created_at.desc())
Index("idx_documents_status", Document.status)
Index("idx_codes_status_plan", ActivationCode.status, ActivationCode.plan_type)
Index("idx_audit_user_action", AuditLog.user_id, AuditLog.action)
