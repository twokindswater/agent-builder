"""
사용자 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType

class User(Base):
    """사용자 모델"""
    __tablename__ = "users"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    mcp_servers = relationship("MCPServer", back_populates="user", cascade="all, delete-orphan") 