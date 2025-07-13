"""
Agent API endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime

from schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from schemas.common import APIResponse
from database.connection import get_db_cursor

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("", response_model=APIResponse[List[AgentResponse]])
async def get_agents():
    """사용자의 에이전트 목록 조회"""
    try:
        with get_db_cursor() as cur:
            cur.execute("""
                SELECT id, name, description, status, created_at, updated_at
                FROM agents
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (MOCK_USER_ID,))
            agents = cur.fetchall()
            
            return {
                "success": True,
                "data": [
                    {
                        "id": str(agent[0]),
                        "name": agent[1],
                        "description": agent[2],
                        "status": agent[3],
                        "created_at": agent[4],
                        "updated_at": agent[5]
                    }
                    for agent in agents
                ]
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch agents: {str(e)}"
        )

@router.post("", response_model=APIResponse[AgentResponse])
async def create_agent(agent: AgentCreate):
    """새로운 에이전트 생성"""
    try:
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        with get_db_cursor() as cur:
            cur.execute("""
                INSERT INTO agents (id, user_id, name, description, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, status, created_at, updated_at
            """, (
                agent_id,
                MOCK_USER_ID,
                agent.name,
                agent.description,
                "active",
                now,
                now
            ))
            
            new_agent = cur.fetchone()
            
            return {
                "success": True,
                "data": {
                    "id": str(new_agent[0]),
                    "name": new_agent[1],
                    "description": new_agent[2],
                    "status": new_agent[3],
                    "created_at": new_agent[4],
                    "updated_at": new_agent[5]
                }
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )

@router.get("/{agent_id}", response_model=APIResponse[AgentResponse])
async def get_agent(agent_id: str):
    """특정 에이전트 조회"""
    try:
        with get_db_cursor() as cur:
            cur.execute("""
                SELECT id, name, description, status, created_at, updated_at
                FROM agents
                WHERE id = %s AND user_id = %s
            """, (agent_id, MOCK_USER_ID))
            
            agent = cur.fetchone()
            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent with id {agent_id} not found"
                )
            
            return {
                "success": True,
                "data": {
                    "id": str(agent[0]),
                    "name": agent[1],
                    "description": agent[2],
                    "status": agent[3],
                    "created_at": agent[4],
                    "updated_at": agent[5]
                }
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch agent: {str(e)}"
        )

@router.put("/{agent_id}", response_model=APIResponse[AgentResponse])
async def update_agent(agent_id: str, agent: AgentUpdate):
    """에이전트 정보 업데이트"""
    try:
        with get_db_cursor() as cur:
            # 먼저 에이전트가 존재하는지 확인
            cur.execute("""
                SELECT id FROM agents
                WHERE id = %s AND user_id = %s
            """, (agent_id, MOCK_USER_ID))
            
            if not cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent with id {agent_id} not found"
                )
            
            # 에이전트 정보 업데이트
            cur.execute("""
                UPDATE agents
                SET name = %s,
                    description = %s,
                    updated_at = %s
                WHERE id = %s AND user_id = %s
                RETURNING id, name, description, status, created_at, updated_at
            """, (
                agent.name,
                agent.description,
                datetime.utcnow(),
                agent_id,
                MOCK_USER_ID
            ))
            
            updated_agent = cur.fetchone()
            
            return {
                "success": True,
                "data": {
                    "id": str(updated_agent[0]),
                    "name": updated_agent[1],
                    "description": updated_agent[2],
                    "status": updated_agent[3],
                    "created_at": updated_agent[4],
                    "updated_at": updated_agent[5]
                }
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent: {str(e)}"
        )

@router.delete("/{agent_id}", response_model=APIResponse[None])
async def delete_agent(agent_id: str):
    """에이전트 삭제"""
    try:
        with get_db_cursor() as cur:
            # 먼저 에이전트가 존재하는지 확인
            cur.execute("""
                SELECT id FROM agents
                WHERE id = %s AND user_id = %s
            """, (agent_id, MOCK_USER_ID))
            
            if not cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent with id {agent_id} not found"
                )
            
            # 에이전트 삭제
            cur.execute("""
                DELETE FROM agents
                WHERE id = %s AND user_id = %s
            """, (agent_id, MOCK_USER_ID))
            
            return {
                "success": True,
                "data": None
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent: {str(e)}"
        ) 