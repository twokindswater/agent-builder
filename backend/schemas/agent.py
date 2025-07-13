"""
Agent related schemas
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgentBase(BaseModel):
    """기본 에이전트 스키마"""
    name: str
    description: Optional[str] = None

class AgentCreate(AgentBase):
    """에이전트 생성 스키마"""
    pass

class AgentUpdate(AgentBase):
    """에이전트 업데이트 스키마"""
    pass

class AgentResponse(AgentBase):
    """에이전트 응답 스키마"""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime 