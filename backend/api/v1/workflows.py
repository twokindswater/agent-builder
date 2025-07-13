"""
워크플로우 API 엔드포인트
"""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database.connection import get_db
from models import Workflow
from schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowListResponse,
    WorkflowExecuteRequest,
    WorkflowExecuteResponse
)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])

@router.post("", response_model=WorkflowResponse, status_code=201)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    """워크플로우 생성"""
    try:
        db = next(db)
        db_workflow = Workflow(
            name=workflow.name,
            description=workflow.description,
            agent_id=workflow.agent_id,
            definition=workflow.definition
        )
        db.add(db_workflow)
        db.commit()
        db.refresh(db_workflow)
        return {"data": db_workflow}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=WorkflowListResponse)
def get_workflows(db: Session = Depends(get_db)):
    """워크플로우 목록 조회"""
    db = next(db)
    workflows = db.query(Workflow).all()
    return {"data": workflows}

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: uuid.UUID, db: Session = Depends(get_db)):
    """특정 워크플로우 조회"""
    db = next(db)
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"data": workflow}

@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(workflow_id: uuid.UUID, workflow: WorkflowUpdate, db: Session = Depends(get_db)):
    """워크플로우 수정"""
    db = next(db)
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    try:
        for key, value in workflow.dict(exclude_unset=True).items():
            setattr(db_workflow, key, value)
        db.commit()
        db.refresh(db_workflow)
        return {"data": db_workflow}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{workflow_id}", status_code=204)
def delete_workflow(workflow_id: uuid.UUID, db: Session = Depends(get_db)):
    """워크플로우 삭제"""
    db = next(db)
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    try:
        db.delete(db_workflow)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{workflow_id}/execute", response_model=WorkflowExecuteResponse)
def execute_workflow(workflow_id: uuid.UUID, request: WorkflowExecuteRequest, db: Session = Depends(get_db)):
    """워크플로우 실행"""
    db = next(db)
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # TODO: 실제 워크플로우 실행 로직 구현
    execution_id = uuid.uuid4()
    return {
        "data": {
            "execution_id": execution_id,
            "status": "completed",
            "result": request.input
        }
    } 