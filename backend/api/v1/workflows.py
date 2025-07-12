"""
Workflow API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from schemas.workflow import (
    WorkflowCreate, WorkflowUpdate, WorkflowResponse,
    WorkflowExecutionResponse, WorkflowExecuteRequest, WorkflowExecuteResponse
)
from schemas.common import APIResponse
from models.database import Workflow, WorkflowExecution
from database.connection import get_db

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.get("", response_model=APIResponse[List[WorkflowResponse]])
async def get_workflows(
    db: Session = Depends(get_db)
):
    """사용자의 워크플로우 목록 조회"""
    workflows = db.query(Workflow).filter(
        Workflow.user_id == MOCK_USER_ID
    ).all()
    
    return APIResponse(
        success=True,
        data=[WorkflowResponse.from_orm(workflow) for workflow in workflows],
        message="워크플로우 목록을 성공적으로 조회했습니다."
    )

@router.post("", response_model=APIResponse[WorkflowResponse])
async def create_workflow(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db)
):
    """새 워크플로우 생성"""
    db_workflow = Workflow(
        user_id=MOCK_USER_ID,
        **workflow.dict()
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    return APIResponse(
        success=True,
        data=WorkflowResponse.from_orm(db_workflow),
        message="워크플로우가 성공적으로 생성되었습니다."
    )

@router.get("/{workflow_id}", response_model=APIResponse[WorkflowResponse])
async def get_workflow(
    workflow_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """특정 워크플로우 상세 조회"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="워크플로우를 찾을 수 없습니다."
        )
    
    return APIResponse(
        success=True,
        data=WorkflowResponse.from_orm(workflow),
        message="워크플로우 정보를 성공적으로 조회했습니다."
    )

@router.put("/{workflow_id}", response_model=APIResponse[WorkflowResponse])
async def update_workflow(
    workflow_id: uuid.UUID,
    workflow_update: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """워크플로우 정보 수정"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="워크플로우를 찾을 수 없습니다."
        )
    
    # 업데이트할 필드만 적용
    update_data = workflow_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workflow, field, value)
    
    db.commit()
    db.refresh(workflow)
    
    return APIResponse(
        success=True,
        data=WorkflowResponse.from_orm(workflow),
        message="워크플로우 정보가 성공적으로 수정되었습니다."
    )

@router.delete("/{workflow_id}", response_model=APIResponse[dict])
async def delete_workflow(
    workflow_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """워크플로우 삭제"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="워크플로우를 찾을 수 없습니다."
        )
    
    db.delete(workflow)
    db.commit()
    
    return APIResponse(
        success=True,
        data={"deleted_id": str(workflow_id)},
        message="워크플로우가 성공적으로 삭제되었습니다."
    )

@router.post("/{workflow_id}/execute", response_model=APIResponse[WorkflowExecuteResponse])
async def execute_workflow(
    workflow_id: uuid.UUID,
    execute_request: WorkflowExecuteRequest,
    db: Session = Depends(get_db)
):
    """워크플로우 실행"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="워크플로우를 찾을 수 없습니다."
        )
    
    if not workflow.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 워크플로우는 실행할 수 없습니다."
        )
    
    # 실행 기록 생성
    execution = WorkflowExecution(
        workflow_id=workflow_id,
        session_id=f"session_{uuid.uuid4()}",
        status="pending",
        input_data=execute_request.input_data
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # TODO: 실제 워크플로우 실행 로직 구현 (Celery 태스크)
    # 현재는 Mock 응답 반환
    try:
        # Mock 실행 시작
        execution.status = "running"
        db.commit()
        
        # 실제로는 Celery 태스크로 비동기 실행
        # execute_workflow_task.delay(workflow_id, execution.id, execute_request.input_data)
        
        return APIResponse(
            success=True,
            data=WorkflowExecuteResponse(
                success=True,
                execution_id=execution.id,
                message="워크플로우 실행이 시작되었습니다."
            ),
            message="워크플로우 실행이 성공적으로 시작되었습니다."
        )
        
    except Exception as e:
        execution.status = "failed"
        execution.error_message = str(e)
        db.commit()
        
        return APIResponse(
            success=False,
            data=WorkflowExecuteResponse(
                success=False,
                execution_id=execution.id,
                message=f"워크플로우 실행 중 오류가 발생했습니다: {str(e)}"
            ),
            message="워크플로우 실행이 실패했습니다."
        )

@router.get("/{workflow_id}/executions", response_model=APIResponse[List[WorkflowExecutionResponse]])
async def get_workflow_executions(
    workflow_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """워크플로우 실행 기록 조회"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="워크플로우를 찾을 수 없습니다."
        )
    
    executions = db.query(WorkflowExecution).filter(
        WorkflowExecution.workflow_id == workflow_id
    ).order_by(WorkflowExecution.started_at.desc()).all()
    
    return APIResponse(
        success=True,
        data=[WorkflowExecutionResponse.from_orm(execution) for execution in executions],
        message="워크플로우 실행 기록을 성공적으로 조회했습니다."
    )

# 특정 실행 상세 조회
@router.get("/executions/{execution_id}", response_model=APIResponse[WorkflowExecutionResponse])
async def get_execution(
    execution_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """특정 실행 상세 조회"""
    execution = db.query(WorkflowExecution).join(Workflow).filter(
        WorkflowExecution.id == execution_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="실행 기록을 찾을 수 없습니다."
        )
    
    return APIResponse(
        success=True,
        data=WorkflowExecutionResponse.from_orm(execution),
        message="실행 기록을 성공적으로 조회했습니다."
    )

# 실행 취소
@router.post("/executions/{execution_id}/cancel", response_model=APIResponse[dict])
async def cancel_execution(
    execution_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """실행 취소"""
    execution = db.query(WorkflowExecution).join(Workflow).filter(
        WorkflowExecution.id == execution_id,
        Workflow.user_id == MOCK_USER_ID
    ).first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="실행 기록을 찾을 수 없습니다."
        )
    
    if execution.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 완료되거나 취소된 실행은 취소할 수 없습니다."
        )
    
    # TODO: 실제 실행 취소 로직 구현 (Celery 태스크 취소)
    execution.status = "cancelled"
    execution.finished_at = db.func.now()
    db.commit()
    
    return APIResponse(
        success=True,
        data={"execution_id": str(execution_id), "status": "cancelled"},
        message="실행이 성공적으로 취소되었습니다."
    ) 