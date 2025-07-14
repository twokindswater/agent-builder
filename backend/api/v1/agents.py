"""
에이전트 API 엔드포인트
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database.connection import get_db
from models import Agent, MCPServer
from schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentListResponse,
    AgentMCPAssign,
    AgentMCPResponse
)
from schemas.common import APIResponse

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("", response_model=APIResponse[List[AgentResponse]])
def get_agents(db: Session = Depends(get_db)):
    """에이전트 목록 조회"""
    try:
        agents = db.query(Agent).all()
        return APIResponse(
            success=True,
            data=[
                AgentResponse(data=agent) for agent in agents
            ],
            message="에이전트 목록을 성공적으로 조회했습니다."
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{agent_id}", response_model=APIResponse[AgentResponse])
def get_agent(agent_id: uuid.UUID, db: Session = Depends(get_db)):
    """에이전트 상세 조회"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return APIResponse(
        success=True,
        data=AgentResponse(data=agent),
        message="에이전트 정보를 성공적으로 조회했습니다."
    )

@router.post("", response_model=AgentResponse, status_code=201)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """에이전트 생성"""
    try:
        db_agent = Agent(
            name=agent.name,
            description=agent.description,
            user_id=agent.user_id,
            model=agent.model,
            instruction=agent.instruction,
            generate_content_config=agent.generate_content_config.dict(),
            output_schema=agent.output_schema,
            output_key=agent.output_key,
            template_type=agent.template_type
        )
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return {"data": db_agent}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: uuid.UUID, agent: AgentUpdate, db: Session = Depends(get_db)):
    """에이전트 수정"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        for key, value in agent.dict(exclude_unset=True).items():
            setattr(db_agent, key, value)
        db.commit()
        db.refresh(db_agent)
        return {"data": db_agent}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{agent_id}", status_code=204)
def delete_agent(agent_id: uuid.UUID, db: Session = Depends(get_db)):
    """에이전트 삭제"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        db.delete(db_agent)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{agent_id}/mcp-tools", response_model=AgentMCPResponse)
def assign_mcp_tools(agent_id: uuid.UUID, assignment: AgentMCPAssign, db: Session = Depends(get_db)):
    """에이전트에 MCP Tool 할당"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # 기존 MCP Tool 연결 모두 제거
        agent.mcp_tools = []
        
        # 새로운 MCP Tool 연결
        mcp_tools = db.query(MCPServer).filter(MCPServer.id.in_(assignment.mcp_ids)).all()
        if len(mcp_tools) != len(assignment.mcp_ids):
            raise HTTPException(status_code=404, detail="Some MCP tools not found")
        
        agent.mcp_tools = mcp_tools
        db.commit()
        db.refresh(agent)
        
        return {
            "data": {
                "agent_id": str(agent.id),
                "mcp_tool_ids": [str(tool.id) for tool in agent.mcp_tools],
                "status": "assigned"
            }
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{agent_id}/mcp-tools", response_model=AgentMCPResponse)
def unassign_mcp_tools(agent_id: uuid.UUID, db: Session = Depends(get_db)):
    """에이전트에서 모든 MCP Tool 해제"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        old_tool_ids = [str(tool.id) for tool in agent.mcp_tools]
        agent.mcp_tools = []
        db.commit()
        db.refresh(agent)
        
        return {
            "data": {
                "agent_id": str(agent.id),
                "mcp_tool_ids": old_tool_ids,
                "status": "unassigned"
            }
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 