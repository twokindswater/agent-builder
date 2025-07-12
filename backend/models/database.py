"""
Database models for AI Agent Builder
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    system_prompt = Column(Text, nullable=False)
    model_config = Column(JSON, nullable=False, default={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    })
    template_type = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent_tools = relationship("AgentMCPTool", back_populates="agent")

class MCPServer(Base):
    __tablename__ = "mcp_servers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    encrypted_token = Column(Text)
    description = Column(Text)
    is_connected = Column(Boolean, default=False)
    last_connected_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tools = relationship("MCPTool", back_populates="server")

class MCPTool(Base):
    __tablename__ = "mcp_tools"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    server_id = Column(UUID(as_uuid=True), ForeignKey("mcp_servers.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    input_schema = Column(JSON)
    output_schema = Column(JSON)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    server = relationship("MCPServer", back_populates="tools")
    agent_tools = relationship("AgentMCPTool", back_populates="tool")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    definition = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    executions = relationship("WorkflowExecution", back_populates="workflow")

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"))
    session_id = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    input_data = Column(JSON)
    output_data = Column(JSON)
    execution_logs = Column(JSON, default=[])
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    error_message = Column(Text)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="executions")

class AgentMCPTool(Base):
    __tablename__ = "agent_mcp_tools"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"))
    tool_id = Column(UUID(as_uuid=True), ForeignKey("mcp_tools.id", ondelete="CASCADE"))
    is_enabled = Column(Boolean, default=True)
    tool_config = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="agent_tools")
    tool = relationship("MCPTool", back_populates="agent_tools") 