from sqlalchemy import Column, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(Text, nullable=False, unique=True, index=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    documents    = relationship("Document", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"
    
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title      = Column(Text, nullable=False)
    source     = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user       = relationship("User", back_populates="documents")
    chunks     = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"
    
    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content     = Column(Text, nullable=False)
    embedding   = Column(Vector(1536), nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    document    = relationship("Document", back_populates="chunks")