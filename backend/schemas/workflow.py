"""
Workflow related Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class WorkflowBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Dict[str, Any] = Field(..., description="Workflow node and connection definition")
    version: int = 1
    is_active: bool = True

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None
    version: Optional[int] = None
    is_active: Optional[bool] = None

class WorkflowResponse(WorkflowBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class WorkflowExecutionBase(BaseModel):
    session_id: str
    status: str = "pending"
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    execution_logs: List[Dict[str, Any]] = []
    error_message: Optional[str] = None

class WorkflowExecutionCreate(BaseModel):
    input_data: Dict[str, Any]

class WorkflowExecutionResponse(WorkflowExecutionBase):
    id: uuid.UUID
    workflow_id: uuid.UUID
    started_at: datetime
    finished_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class WorkflowExecutionWithWorkflow(WorkflowExecutionResponse):
    workflow: WorkflowResponse

class WorkflowExecuteRequest(BaseModel):
    input_data: Dict[str, Any]

class WorkflowExecuteResponse(BaseModel):
    success: bool
    execution_id: uuid.UUID
    message: str 