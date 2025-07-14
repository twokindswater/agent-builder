"""
에이전트 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType
from models.agent_mcp import agent_mcp_association

class Agent(Base):
    """에이전트 모델"""
    __tablename__ = "agents"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    model = Column(String, nullable=False, default="gpt-4")
    instruction = Column(String, nullable=False)
    generate_content_config = Column(JSON, nullable=False, default={"temperature": 0.7, "max_output_tokens": 1000})
    output_schema = Column(JSON)
    output_key = Column(String)
    template_type = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    user = relationship("User", back_populates="agents")
    workflows = relationship("Workflow", back_populates="agent", cascade="all, delete-orphan")
    
    # MCP Tool 관계 설정
    mcp_tools = relationship(
        "MCPServer",
        secondary=agent_mcp_association,
        back_populates="agents",
        cascade="all, delete"
    ) 