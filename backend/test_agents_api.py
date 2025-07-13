#!/usr/bin/env python3
"""
에이전트 API 테스트
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

def test_agents_api():
    """에이전트 API 테스트"""
    print("\n🧪 에이전트 API 테스트 시작")

    # 1. 에이전트 생성
    create_data = {
        "name": "테스트 에이전트",
        "description": "API 테스트용 에이전트입니다."
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/agents",
        headers=HEADERS,
        json=create_data
    )
    print_response(response, "에이전트 생성")
    assert response.status_code == 201, f"에이전트 생성 실패: {response.status_code} - {response.text}"
    
    agent_id = response.json()["data"]["id"]

    # 2. 에이전트 목록 조회
    response = requests.get(f"{BASE_URL}/api/v1/agents", headers=HEADERS)
    print_response(response, "에이전트 목록 조회")
    assert response.status_code == 200, f"에이전트 목록 조회 실패: {response.status_code} - {response.text}"
    
    # 3. 특정 에이전트 조회
    response = requests.get(
        f"{BASE_URL}/api/v1/agents/{agent_id}",
        headers=HEADERS
    )
    print_response(response, "특정 에이전트 조회")
    assert response.status_code == 200, f"특정 에이전트 조회 실패: {response.status_code} - {response.text}"

    # 4. 에이전트 수정
    update_data = {
        "name": "수정된 테스트 에이전트",
        "description": "API 테스트용 에이전트가 수정되었습니다."
    }
    response = requests.put(
        f"{BASE_URL}/api/v1/agents/{agent_id}",
        headers=HEADERS,
        json=update_data
    )
    print_response(response, "에이전트 수정")
    assert response.status_code == 200, f"에이전트 수정 실패: {response.status_code} - {response.text}"

    # 5. 에이전트 삭제
    response = requests.delete(
        f"{BASE_URL}/api/v1/agents/{agent_id}",
        headers=HEADERS
    )
    print_response(response, "에이전트 삭제")
    assert response.status_code == 204, f"에이전트 삭제 실패: {response.status_code} - {response.text}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 