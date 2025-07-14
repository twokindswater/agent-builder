"""
MCP 서버 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType
from models.agent_mcp import agent_mcp_association

class MCPServer(Base):
    """MCP 서버 모델"""
    __tablename__ = "mcp_servers"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    user = relationship("User", back_populates="mcp_servers")
    agents = relationship(
        "Agent",
        secondary=agent_mcp_association,
        back_populates="mcp_tools",
        cascade="all, delete"
    ) 