#!/usr/bin/env python3
"""
워크플로우 API 테스트
"""
import json
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from database.connection import get_db, get_test_db
from models import User, Agent, Workflow

client = TestClient(app)

# 테스트 데이터베이스 의존성 주입
app.dependency_overrides[get_db] = get_test_db

@pytest.fixture
def db():
    """테스트 데이터베이스 세션 픽스처"""
    db = next(get_test_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db: Session):
    """테스트용 사용자 생성 픽스처"""
    user = User(
        id=uuid.uuid4(),
        email=f"test_{uuid.uuid4()}@example.com"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_agent(db: Session, test_user: User):
    """테스트용 에이전트 생성 픽스처"""
    agent = Agent(
        id=uuid.uuid4(),
        user_id=test_user.id,
        name="테스트 에이전트",
        description="테스트용 에이전트입니다.",
        status="active"
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@pytest.fixture
def test_workflow(db: Session, test_agent: Agent):
    """테스트용 워크플로우 생성 픽스처"""
    workflow = Workflow(
        name="테스트 워크플로우",
        description="테스트용 워크플로우입니다.",
        agent_id=test_agent.id,
        definition={
            "nodes": [],
            "edges": []
        }
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

def test_create_workflow(test_agent: Agent):
    """워크플로우 생성 테스트"""
    workflow_data = {
        "name": "새 워크플로우",
        "description": "API 테스트용 새 워크플로우입니다.",
        "agent_id": str(test_agent.id),
        "definition": {
            "nodes": [],
            "edges": []
        }
    }
    
    response = client.post("/api/v1/workflows", json=workflow_data)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == workflow_data["name"]
    assert data["description"] == workflow_data["description"]
    assert data["agent_id"] == workflow_data["agent_id"]

def test_get_workflows(test_workflow: Workflow):
    """워크플로우 목록 조회 테스트"""
    response = client.get("/api/v1/workflows")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert any(w["id"] == str(test_workflow.id) for w in data)

def test_get_workflow(test_workflow: Workflow):
    """특정 워크플로우 조회 테스트"""
    response = client.get(f"/api/v1/workflows/{test_workflow.id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == str(test_workflow.id)
    assert data["name"] == test_workflow.name
    assert data["description"] == test_workflow.description

def test_update_workflow(test_workflow: Workflow):
    """워크플로우 수정 테스트"""
    update_data = {
        "name": "수정된 워크플로우",
        "description": "수정된 설명입니다.",
        "definition": {
            "nodes": [
                {
                    "id": "node1",
                    "type": "start",
                    "position": {"x": 100, "y": 100}
                },
                {
                    "id": "node2",
                    "type": "end",
                    "position": {"x": 300, "y": 100}
                }
            ],
            "edges": [
                {
                    "id": "edge1",
                    "source": "node1",
                    "target": "node2"
                }
            ]
        }
    }
    
    response = client.put(f"/api/v1/workflows/{test_workflow.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["definition"] == update_data["definition"]

def test_execute_workflow(test_workflow: Workflow):
    """워크플로우 실행 테스트"""
    execute_data = {
        "input": {
            "test_key": "test_value"
        }
    }
    
    response = client.post(f"/api/v1/workflows/{test_workflow.id}/execute", json=execute_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "execution_id" in data
    assert data["status"] == "completed"  # 또는 "running", 실제 구현에 따라 다름

def test_delete_workflow(test_workflow: Workflow):
    """워크플로우 삭제 테스트"""
    response = client.delete(f"/api/v1/workflows/{test_workflow.id}")
    assert response.status_code == 204

    # 삭제 확인
    response = client.get(f"/api/v1/workflows/{test_workflow.id}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_get_nonexistent_workflow():
    """존재하지 않는 워크플로우 조회 테스트"""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/workflows/{non_existent_id}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower() 