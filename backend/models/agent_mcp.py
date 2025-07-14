"""
에이전트-MCP 연결 모델
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from database.connection import Base
from models.base import UUIDType

# 에이전트-MCP 연결 테이블
agent_mcp_association = Table(
    'agent_mcp_tools',
    Base.metadata,
    Column('agent_id', UUIDType, ForeignKey('agents.id', ondelete='CASCADE'), primary_key=True),
    Column('mcp_id', UUIDType, ForeignKey('mcp_servers.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
) 