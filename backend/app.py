#!/usr/bin/env python3
"""
AI Agent Builder - Backend Application
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="AI Agent Builder API",
    description="AI Agent와 MCP를 시각적으로 생성하고 워크플로우를 구성하는 서비스",
    version="1.0.0"
)

# CORS 설정 - 프론트엔드에서 API 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 응답 모델 정의
class HealthResponse(BaseModel):
    status: str
    service: str

class InfoResponse(BaseModel):
    message: str
    status: str
    version: str

class APIInfoResponse(BaseModel):
    api_version: str
    service: str
    endpoints: Dict[str, str]

# 기본 라우트 - Hello World API 엔드포인트
@app.get("/", response_model=InfoResponse)
async def hello_world():
    """기본 Hello World 엔드포인트"""
    return InfoResponse(
        message="Hello World from AI Agent Builder API!",
        status="success",
        version="1.0.0"
    )

# 헬스체크 엔드포인트
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """애플리케이션 상태 확인 엔드포인트"""
    return HealthResponse(
        status="healthy",
        service="AI Agent Builder Backend"
    )

# API 버전 정보
@app.get("/api/v1/info", response_model=APIInfoResponse)
async def api_info():
    """API 버전 및 정보 엔드포인트"""
    return APIInfoResponse(
        api_version="v1",
        service="AI Agent Builder",
        endpoints={
            "agents": "/api/v1/agents",
            "workflows": "/api/v1/workflows",
            "mcp": "/api/v1/mcp"
        }
    )

# 애플리케이션 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행되는 이벤트"""
    print("🚀 AI Agent Builder Backend 시작됨")
    print(f"🌐 API 문서: http://localhost:8000/docs")
    print(f"🔍 ReDoc: http://localhost:8000/redoc")

# 애플리케이션 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행되는 이벤트"""
    print("🛑 AI Agent Builder Backend 종료됨")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 