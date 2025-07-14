"""
워크플로우 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType

class Workflow(Base):
    """워크플로우 모델"""
    __tablename__ = "workflows"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUIDType, ForeignKey("agents.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    definition = Column(JSON)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정 (문자열 참조 사용)
    agent = relationship("Agent", back_populates="workflows")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan") 