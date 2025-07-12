"""
MCP related Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class MCPServerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None

class MCPServerCreate(MCPServerBase):
    token: Optional[str] = None

class MCPServerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    token: Optional[str] = None

class MCPServerResponse(MCPServerBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_connected: bool
    last_connected_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class MCPToolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    is_available: bool = True

class MCPToolResponse(MCPToolBase):
    id: uuid.UUID
    server_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class MCPServerWithTools(MCPServerResponse):
    tools: List[MCPToolResponse] = []

class MCPConnectionTestResponse(BaseModel):
    success: bool
    message: str
    tools_count: Optional[int] = None
    error: Optional[str] = None

class MCPToolSyncResponse(BaseModel):
    success: bool
    message: str
    synced_tools: int
    removed_tools: int
    error: Optional[str] = None 