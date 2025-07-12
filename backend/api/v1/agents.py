"""
Agent API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from schemas.agent import (
    AgentCreate, AgentUpdate, AgentResponse, 
    AgentTestRequest, AgentTestResponse,
    AgentTemplate, AgentFromTemplateRequest
)
from schemas.common import APIResponse, PaginatedResponse
from models.database import Agent
from database.connection import get_db

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/agents", tags=["agents"])

# Agent 템플릿 데이터 (실제로는 데이터베이스나 설정 파일에서 가져와야 함)
AGENT_TEMPLATES = [
    AgentTemplate(
        id="chatbot",
        name="챗봇 Agent",
        description="일반적인 대화형 챗봇 Agent",
        template_type="chatbot",
        default_config={
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000
        },
        system_prompt_template="당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 친절하고 정확하게 답변해주세요."
    ),
    AgentTemplate(
        id="data_analyst",
        name="데이터 분석 Agent",
        description="데이터 분석 및 시각화를 위한 Agent",
        template_type="data_analyst",
        default_config={
            "model": "gpt-4",
            "temperature": 0.3,
            "max_tokens": 2000
        },
        system_prompt_template="당신은 데이터 분석 전문가입니다. 제공된 데이터를 분석하고 인사이트를 제공해주세요."
    ),
    AgentTemplate(
        id="code_generator",
        name="코드 생성 Agent",
        description="코드 생성 및 리뷰를 위한 Agent",
        template_type="code_generator",
        default_config={
            "model": "gpt-4",
            "temperature": 0.2,
            "max_tokens": 3000
        },
        system_prompt_template="당신은 숙련된 프로그래머입니다. 요구사항에 따라 고품질의 코드를 생성하고 설명해주세요."
    )
]

@router.get("/templates", response_model=APIResponse[List[AgentTemplate]])
async def get_agent_templates():
    """사용 가능한 Agent 템플릿 목록 조회"""
    return APIResponse(
        success=True,
        data=AGENT_TEMPLATES,
        message="Agent 템플릿 목록을 성공적으로 조회했습니다."
    )

@router.post("/from-template", response_model=APIResponse[AgentResponse])
async def create_agent_from_template(
    request: AgentFromTemplateRequest,
    db: Session = Depends(get_db)
):
    """템플릿으로부터 Agent 생성"""
    # 템플릿 찾기
    template = next((t for t in AGENT_TEMPLATES if t.id == request.template_id), None)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="템플릿을 찾을 수 없습니다."
        )
    
    # 설정 병합
    config = template.default_config.copy()
    if request.custom_config:
        config.update(request.custom_config)
    
    # Agent 생성
    agent_data = AgentCreate(
        name=request.name,
        description=request.description or template.description,
        system_prompt=template.system_prompt_template,
        model_config=config,
        template_type=template.template_type
    )
    
    db_agent = Agent(
        user_id=MOCK_USER_ID,  # 개발 환경용 mock 사용자 ID 사용
        **agent_data.dict()
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return APIResponse(
        success=True,
        data=AgentResponse.from_orm(db_agent),
        message="템플릿으로부터 Agent가 성공적으로 생성되었습니다."
    )

@router.get("", response_model=APIResponse[List[AgentResponse]])
async def get_agents(
    db: Session = Depends(get_db)
):
    """사용자의 Agent 목록 조회"""
    agents = db.query(Agent).filter(
        Agent.user_id == MOCK_USER_ID  # 개발 환경용 mock 사용자 ID 사용
    ).all()
    
    return APIResponse(
        success=True,
        data=[AgentResponse.from_orm(agent) for agent in agents],
        message="Agent 목록을 성공적으로 조회했습니다."
    )

@router.post("", response_model=APIResponse[AgentResponse])
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    """새 Agent 생성"""
    db_agent = Agent(
        user_id=MOCK_USER_ID,  # 개발 환경용 mock 사용자 ID 사용
        **agent.dict()
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return APIResponse(
        success=True,
        data=AgentResponse.from_orm(db_agent),
        message="Agent가 성공적으로 생성되었습니다."
    )

@router.get("/{agent_id}", response_model=APIResponse[AgentResponse])
async def get_agent(
    agent_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """특정 Agent 상세 조회"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == MOCK_USER_ID  # 개발 환경용 mock 사용자 ID 사용
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent를 찾을 수 없습니다."
        )
    
    return APIResponse(
        success=True,
        data=AgentResponse.from_orm(agent),
        message="Agent 정보를 성공적으로 조회했습니다."
    )

@router.put("/{agent_id}", response_model=APIResponse[AgentResponse])
async def update_agent(
    agent_id: uuid.UUID,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Agent 정보 수정"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == MOCK_USER_ID  # 개발 환경용 mock 사용자 ID 사용
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent를 찾을 수 없습니다."
        )
    
    # 업데이트할 필드만 적용
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    return APIResponse(
        success=True,
        data=AgentResponse.from_orm(agent),
        message="Agent 정보가 성공적으로 수정되었습니다."
    )

@router.delete("/{agent_id}", response_model=APIResponse[dict])
async def delete_agent(
    agent_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Agent 삭제"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == MOCK_USER_ID  # 개발 환경용 mock 사용자 ID 사용
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent를 찾을 수 없습니다."
        )
    
    db.delete(agent)
    db.commit()
    
    return APIResponse(
        success=True,
        data={"deleted_id": str(agent_id)},
        message="Agent가 성공적으로 삭제되었습니다."
    )

@router.post("/{agent_id}/test", response_model=APIResponse[AgentTestResponse])
async def test_agent(
    agent_id: uuid.UUID,
    test_request: AgentTestRequest,
    db: Session = Depends(get_db)
):
    """Agent 테스트 실행"""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.user_id == MOCK_USER_ID  # 개발 환경용 mock 사용자 ID 사용
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent를 찾을 수 없습니다."
        )
    
    # TODO: 실제 ADK Agent 실행 로직 구현
    # 현재는 Mock 응답 반환
    import time
    start_time = time.time()
    
    try:
        # Mock 응답 생성
        mock_result = {
            "agent_id": str(agent_id),
            "agent_name": agent.name,
            "input_received": test_request.input_data,
            "output": "테스트 응답: Agent가 정상적으로 동작합니다.",
            "model_used": agent.model_config.get("model", "gpt-4")
        }
        
        execution_time = time.time() - start_time
        
        return APIResponse(
            success=True,
            data=AgentTestResponse(
                success=True,
                result=mock_result,
                execution_time=execution_time
            ),
            message="Agent 테스트가 성공적으로 실행되었습니다."
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        return APIResponse(
            success=False,
            data=AgentTestResponse(
                success=False,
                error=str(e),
                execution_time=execution_time
            ),
            message="Agent 테스트 실행 중 오류가 발생했습니다."
        ) 