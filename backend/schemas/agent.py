"""
Agent related Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    system_prompt: str = Field(..., min_length=1)
    agent_config: Dict[str, Any] = Field(default={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    })
    template_type: Optional[str] = None
    is_active: bool = True

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    system_prompt: Optional[str] = Field(None, min_length=1)
    agent_config: Optional[Dict[str, Any]] = None
    template_type: Optional[str] = None
    is_active: Optional[bool] = None

class AgentResponse(AgentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class AgentTestRequest(BaseModel):
    input_data: Dict[str, Any]
    
class AgentTestResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

class AgentTemplate(BaseModel):
    id: str
    name: str
    description: str
    template_type: str
    default_config: Dict[str, Any]
    system_prompt_template: str

class AgentFromTemplateRequest(BaseModel):
    template_id: str
    name: str
    description: Optional[str] = None
    custom_config: Optional[Dict[str, Any]] = None 