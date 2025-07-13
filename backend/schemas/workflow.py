"""
워크플로우 스키마
"""
import uuid
from datetime import datetime
from typing import Dict, Optional, List, Any
from pydantic import BaseModel, UUID4

class WorkflowBase(BaseModel):
    """워크플로우 기본 스키마"""
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any]

class WorkflowCreate(WorkflowBase):
    """워크플로우 생성 스키마"""
    agent_id: UUID4

class WorkflowUpdate(WorkflowBase):
    """워크플로우 수정 스키마"""
    name: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None

class WorkflowDB(WorkflowBase):
    """워크플로우 DB 스키마"""
    id: UUID4
    agent_id: UUID4
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkflowResponse(BaseModel):
    """워크플로우 응답 스키마"""
    data: WorkflowDB

class WorkflowListResponse(BaseModel):
    """워크플로우 목록 응답 스키마"""
    data: List[WorkflowDB]

class WorkflowExecuteRequest(BaseModel):
    """워크플로우 실행 요청 스키마"""
    input: Dict[str, Any]

class WorkflowExecuteResponse(BaseModel):
    """워크플로우 실행 응답 스키마"""
    data: Dict[str, Any] 