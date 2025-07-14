#!/usr/bin/env python3
"""
에이전트 API 테스트
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app
from models import User, Agent, MCPServer

# 테스트 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    """테스트용 데이터베이스 세션"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db
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
    db = TestingSessionLocal()
    user = User(name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture
def test_agent(test_user):
    """테스트용 에이전트 생성"""
    db = TestingSessionLocal()
    agent = Agent(name="Test Agent", user_id=test_user.id)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    db.close()
    return agent

@pytest.fixture
def test_mcp_servers():
    """테스트용 MCP 서버 생성"""
    db = TestingSessionLocal()
    servers = [
        MCPServer(
            name=f"Test MCP Server {i}",
            url=f"http://test-mcp-{i}.example.com",
            api_key=f"test-key-{i}"
        )
        for i in range(3)
    ]
    for server in servers:
        db.add(server)
    db.commit()
    for server in servers:
        db.refresh(server)
    db.close()
    return servers

def test_create_agent(test_user):
    """에이전트 생성 테스트"""
    response = client.post(
        "/api/v1/agents",
        json={
            "name": "Test Agent",
            "description": "Test Description",
            "user_id": str(test_user.id)
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test Agent"
    assert data["description"] == "Test Description"
    assert data["user_id"] == str(test_user.id)

def test_get_agents(test_agent):
    """에이전트 목록 조회 테스트"""
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["name"] == test_agent.name

def test_get_agent(test_agent):
    """특정 에이전트 조회 테스트"""
    response = client.get(f"/api/v1/agents/{test_agent.id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == test_agent.name

def test_update_agent(test_agent):
    """에이전트 수정 테스트"""
    response = client.put(
        f"/api/v1/agents/{test_agent.id}",
        json={
            "name": "Updated Agent",
            "description": "Updated Description"
        }
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Updated Agent"
    assert data["description"] == "Updated Description"

def test_delete_agent(test_agent):
    """에이전트 삭제 테스트"""
    response = client.delete(f"/api/v1/agents/{test_agent.id}")
    assert response.status_code == 204

def test_assign_mcp_tools(test_agent, test_mcp_servers):
    """에이전트에 MCP Tool 할당 테스트"""
    mcp_ids = [str(server.id) for server in test_mcp_servers]
    response = client.post(
        f"/api/v1/agents/{test_agent.id}/mcp-tools",
        json={"mcp_ids": mcp_ids}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["agent_id"] == str(test_agent.id)
    assert len(data["mcp_tool_ids"]) == len(mcp_ids)
    assert set(data["mcp_tool_ids"]) == set(mcp_ids)
    assert data["status"] == "assigned"

def test_assign_nonexistent_mcp_tools(test_agent):
    """존재하지 않는 MCP Tool 할당 테스트"""
    response = client.post(
        f"/api/v1/agents/{test_agent.id}/mcp-tools",
        json={"mcp_ids": [str(uuid.uuid4())]}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Some MCP tools not found"

def test_unassign_mcp_tools(test_agent, test_mcp_servers):
    """에이전트에서 MCP Tool 해제 테스트"""
    # 먼저 MCP Tool 할당
    mcp_ids = [str(server.id) for server in test_mcp_servers]
    client.post(
        f"/api/v1/agents/{test_agent.id}/mcp-tools",
        json={"mcp_ids": mcp_ids}
    )
    
    # MCP Tool 해제
    response = client.delete(f"/api/v1/agents/{test_agent.id}/mcp-tools")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["agent_id"] == str(test_agent.id)
    assert len(data["mcp_tool_ids"]) == len(mcp_ids)
    assert set(data["mcp_tool_ids"]) == set(mcp_ids)
    assert data["status"] == "unassigned"

def test_unassign_mcp_tools_when_none_assigned(test_agent):
    """MCP Tool이 할당되지 않은 에이전트에서 해제 테스트"""
    response = client.delete(f"/api/v1/agents/{test_agent.id}/mcp-tools")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["agent_id"] == str(test_agent.id)
    assert len(data["mcp_tool_ids"]) == 0
    assert data["status"] == "unassigned" 