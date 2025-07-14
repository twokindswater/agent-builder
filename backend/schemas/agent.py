"""
에이전트 스키마
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, UUID4, Field

from schemas.mcp import MCPServerResponse

class GenerateContentConfig(BaseModel):
    """모델 생성 설정 스키마"""
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_output_tokens: int = Field(1000, gt=0)

class AgentBase(BaseModel):
    """에이전트 기본 스키마"""
    name: str
    description: Optional[str] = None
    model: str = "gpt-4"
    instruction: str
    generate_content_config: GenerateContentConfig = Field(default_factory=lambda: GenerateContentConfig())
    output_schema: Optional[Dict[str, Any]] = None
    output_key: Optional[str] = None
    template_type: Optional[str] = None

class AgentCreate(AgentBase):
    """에이전트 생성 스키마"""
    user_id: UUID4

class AgentUpdate(AgentBase):
    """에이전트 수정 스키마"""
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    instruction: Optional[str] = None
    generate_content_config: Optional[GenerateContentConfig] = None
    output_schema: Optional[Dict[str, Any]] = None
    output_key: Optional[str] = None
    template_type: Optional[str] = None

class AgentDB(AgentBase):
    """에이전트 DB 스키마"""
    id: UUID4
    user_id: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime
    mcp_tools: List[MCPServerResponse] = []

    class Config:
        from_attributes = True

class AgentResponse(BaseModel):
    """에이전트 응답 스키마"""
    data: AgentDB

class AgentListResponse(BaseModel):
    """에이전트 목록 응답 스키마"""
    data: List[AgentDB]

class AgentMCPAssign(BaseModel):
    """에이전트 MCP Tool 할당 스키마"""
    mcp_ids: List[UUID4]

class AgentMCPResponse(BaseModel):
    """에이전트 MCP Tool 응답 스키마"""
    data: dict 