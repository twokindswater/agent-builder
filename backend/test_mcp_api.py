#!/usr/bin/env python3
"""
MCP API 테스트
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app
from models import MCPServer

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
def test_mcp_server():
    """테스트용 MCP 서버 생성"""
    db = TestingSessionLocal()
    server = MCPServer(
        name="테스트 MCP 서버",
        url="http://localhost:3000",
        api_key="test_api_key",
        description="API 테스트용 MCP 서버입니다."
    )
    db.add(server)
    db.commit()
    db.refresh(server)
    db.close()
    return server

def test_create_mcp_server():
    """MCP 서버 생성 테스트"""
    create_data = {
        "name": "테스트 MCP 서버",
        "url": "http://localhost:3000",
        "api_key": "test_api_key",
        "description": "API 테스트용 MCP 서버입니다."
    }
    response = client.post("/api/v1/mcp-servers", json=create_data)
    print("\nResponse:", response.json())  # 응답 내용 출력
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == create_data["name"]
    assert data["url"] == create_data["url"]
    assert data["description"] == create_data["description"]

def test_get_mcp_servers(test_mcp_server):
    """MCP 서버 목록 조회 테스트"""
    response = client.get("/api/v1/mcp-servers")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["name"] == test_mcp_server.name

def test_get_mcp_server(test_mcp_server):
    """특정 MCP 서버 조회 테스트"""
    response = client.get(f"/api/v1/mcp-servers/{test_mcp_server.id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == test_mcp_server.name

def test_update_mcp_server(test_mcp_server):
    """MCP 서버 수정 테스트"""
    update_data = {
        "name": "수정된 테스트 MCP 서버",
        "url": "http://localhost:3000",
        "api_key": "updated_test_api_key",
        "description": "API 테스트용 MCP 서버가 수정되었습니다."
    }
    response = client.put(
        f"/api/v1/mcp-servers/{test_mcp_server.id}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

def test_test_mcp_server_connection(test_mcp_server):
    """MCP 서버 연결 테스트"""
    response = client.post(f"/api/v1/mcp-servers/{test_mcp_server.id}/test")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_sync_mcp_server_tools(test_mcp_server):
    """MCP 서버 도구 동기화 테스트"""
    response = client.post(f"/api/v1/mcp-servers/{test_mcp_server.id}/sync")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "synced_tools" in data
    assert "removed_tools" in data
    assert data["synced_tools"] > 0

def test_delete_mcp_server(test_mcp_server):
    """MCP 서버 삭제 테스트"""
    response = client.delete(f"/api/v1/mcp-servers/{test_mcp_server.id}")
    assert response.status_code == 204

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 