#!/usr/bin/env python3
"""
MCP API 테스트
"""

import requests
import json
from datetime import datetime
import pytest

# API 기본 설정
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json"
}

def print_response(response: requests.Response, message: str):
    """응답 결과 출력"""
    print(f"\n=== {message} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("Response:", response.text)

def test_mcp_api():
    """MCP API 테스트"""
    print("\n🧪 MCP API 테스트 시작")

    # 1. MCP 서버 생성
    create_data = {
        "name": "테스트 MCP 서버",
        "url": "http://localhost:3000",
        "api_key": "test_api_key",
        "description": "API 테스트용 MCP 서버입니다."
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/mcp-servers",
        headers=HEADERS,
        json=create_data
    )
    print_response(response, "MCP 서버 생성")
    assert response.status_code == 201, f"MCP 서버 생성 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "data" in response_data, "응답에 data 필드가 없습니다"
    assert "id" in response_data["data"], "응답에 id 필드가 없습니다"
    mcp_server_id = response_data["data"]["id"]

    # 2. MCP 서버 목록 조회
    response = requests.get(f"{BASE_URL}/api/v1/mcp-servers", headers=HEADERS)
    print_response(response, "MCP 서버 목록 조회")
    assert response.status_code == 200, f"MCP 서버 목록 조회 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "data" in response_data, "응답에 data 필드가 없습니다"
    assert isinstance(response_data["data"], list), "data 필드가 리스트가 아닙니다"

    # 3. 특정 MCP 서버 조회
    response = requests.get(
        f"{BASE_URL}/api/v1/mcp-servers/{mcp_server_id}",
        headers=HEADERS
    )
    print_response(response, "특정 MCP 서버 조회")
    assert response.status_code == 200, f"특정 MCP 서버 조회 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "data" in response_data, "응답에 data 필드가 없습니다"
    assert response_data["data"]["id"] == mcp_server_id, "조회된 서버 ID가 일치하지 않습니다"

    # 4. MCP 서버 수정
    update_data = {
        "name": "수정된 테스트 MCP 서버",
        "url": "http://localhost:3000",
        "api_key": "updated_test_api_key",
        "description": "API 테스트용 MCP 서버가 수정되었습니다."
    }
    response = requests.put(
        f"{BASE_URL}/api/v1/mcp-servers/{mcp_server_id}",
        headers=HEADERS,
        json=update_data
    )
    print_response(response, "MCP 서버 수정")
    assert response.status_code == 200, f"MCP 서버 수정 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "data" in response_data, "응답에 data 필드가 없습니다"
    assert response_data["data"]["name"] == update_data["name"], "서버 이름이 올바르게 수정되지 않았습니다"

    # 5. MCP 서버 연결 테스트
    response = requests.post(
        f"{BASE_URL}/api/v1/mcp-servers/{mcp_server_id}/test",
        headers=HEADERS
    )
    print_response(response, "MCP 서버 연결 테스트")
    assert response.status_code == 200, f"MCP 서버 연결 테스트 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "success" in response_data, "응답에 success 필드가 없습니다"

    # 6. MCP 서버 도구 동기화
    response = requests.post(
        f"{BASE_URL}/api/v1/mcp-servers/{mcp_server_id}/sync",
        headers=HEADERS
    )
    print_response(response, "MCP 서버 도구 동기화")
    assert response.status_code == 200, f"MCP 서버 도구 동기화 실패: {response.status_code} - {response.text}"
    
    response_data = response.json()
    assert "data" in response_data, "응답에 data 필드가 없습니다"
    assert "synced_tools" in response_data["data"], "응답에 synced_tools 필드가 없습니다"
    assert "removed_tools" in response_data["data"], "응답에 removed_tools 필드가 없습니다"
    assert response_data["data"]["synced_tools"] > 0, "동기화된 도구가 없습니다"

    # 7. MCP 서버 삭제
    response = requests.delete(
        f"{BASE_URL}/api/v1/mcp-servers/{mcp_server_id}",
        headers=HEADERS
    )
    print_response(response, "MCP 서버 삭제")
    assert response.status_code == 204, f"MCP 서버 삭제 실패: {response.status_code} - {response.text}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 