#!/usr/bin/env python3
"""
워크플로우 API 테스트
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app
from models import User, Agent, Workflow

# 테스트 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """테스트용 데이터베이스 세션"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """테스트 데이터베이스 설정"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    """테스트용 사용자 생성"""
    db = next(override_get_db())
    user = User(name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_agent(test_user):
    """테스트용 에이전트 생성"""
    db = next(override_get_db())
    agent = Agent(name="Test Agent", user_id=test_user.id)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@pytest.fixture
def test_workflow(test_agent):
    """테스트용 워크플로우 생성"""
    db = next(override_get_db())
    workflow = Workflow(
        name="Test Workflow",
        description="Test Description",
        agent_id=test_agent.id,
        definition={"test": "data"}
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

def test_create_workflow(test_agent):
    """워크플로우 생성 테스트"""
    response = client.post(
        "/api/v1/workflows",
        json={
            "name": "Test Workflow",
            "description": "Test Description",
            "agent_id": str(test_agent.id),
            "definition": {"test": "data"}
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test Workflow"
    assert data["description"] == "Test Description"
    assert data["agent_id"] == str(test_agent.id)

def test_get_workflows(test_workflow):
    """워크플로우 목록 조회 테스트"""
    response = client.get("/api/v1/workflows")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["name"] == test_workflow.name

def test_get_workflow(test_workflow):
    """특정 워크플로우 조회 테스트"""
    response = client.get(f"/api/v1/workflows/{test_workflow.id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == test_workflow.name

def test_update_workflow(test_workflow):
    """워크플로우 수정 테스트"""
    response = client.put(
        f"/api/v1/workflows/{test_workflow.id}",
        json={
            "name": "Updated Workflow",
            "description": "Updated Description",
            "definition": {"updated": "data"}
        }
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Updated Workflow"
    assert data["description"] == "Updated Description"

def test_delete_workflow(test_workflow):
    """워크플로우 삭제 테스트"""
    response = client.delete(f"/api/v1/workflows/{test_workflow.id}")
    assert response.status_code == 204

def test_execute_workflow(test_workflow):
    """워크플로우 실행 테스트"""
    response = client.post(
        f"/api/v1/workflows/{test_workflow.id}/execute",
        json={"input": {"test": "data"}}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "execution_id" in data
    assert data["status"] == "completed"

def test_assign_agent(test_workflow, test_user):
    """워크플로우에 에이전트 할당 테스트"""
    # 새로운 에이전트 생성
    db = next(override_get_db())
    new_agent = Agent(name="New Agent", user_id=test_user.id)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    response = client.post(
        f"/api/v1/workflows/{test_workflow.id}/assign-agent",
        json={"agent_id": str(new_agent.id)}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["agent_id"] == str(new_agent.id)
    assert data["status"] == "assigned"

def test_assign_agent_not_found(test_workflow):
    """존재하지 않는 에이전트 할당 테스트"""
    response = client.post(
        f"/api/v1/workflows/{test_workflow.id}/assign-agent",
        json={"agent_id": str(uuid.uuid4())}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Agent not found"

def test_unassign_agent(test_workflow):
    """워크플로우에서 에이전트 해제 테스트"""
    response = client.delete(f"/api/v1/workflows/{test_workflow.id}/unassign-agent")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "unassigned"

def test_unassign_agent_not_assigned(test_workflow):
    """에이전트가 할당되지 않은 워크플로우에서 해제 시도 테스트"""
    # 먼저 에이전트 해제
    client.delete(f"/api/v1/workflows/{test_workflow.id}/unassign-agent")
    
    # 다시 해제 시도
    response = client.delete(f"/api/v1/workflows/{test_workflow.id}/unassign-agent")
    assert response.status_code == 400
    assert response.json()["detail"] == "No agent assigned to this workflow" 