"""
워크플로우 실행 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType

class WorkflowExecution(Base):
    """워크플로우 실행 모델"""
    __tablename__ = "workflow_executions"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUIDType, ForeignKey("workflows.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정 (문자열 참조 사용)
    workflow = relationship("Workflow", back_populates="executions") 