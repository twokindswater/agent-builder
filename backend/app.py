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

# API 라우터 임포트
from api.v1 import agents, mcp, workflows

# 환경 변수 로드
load_dotenv()

# 개발 환경 설정
os.environ["ENVIRONMENT"] = "development"

# FastAPI 앱 생성
app = FastAPI(
    title="AI Agent Builder API",
    description="AI Agent와 MCP를 시각적으로 생성하고 워크플로우를 구성하는 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
    supabase_url: str

class InfoResponse(BaseModel):
    message: str
    status: str
    version: str

class APIInfoResponse(BaseModel):
    api_version: str
    service: str
    endpoints: Dict[str, str]

# API 라우터 등록
app.include_router(agents.router, prefix="/api/v1")
app.include_router(mcp.router, prefix="/api/v1")
app.include_router(workflows.router, prefix="/api/v1")

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
    """서비스 상태 확인"""
    return HealthResponse(
        status="healthy",
        service="AI Agent Builder API",
        supabase_url=SUPABASE_URL
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
            "agent_templates": "/api/v1/agents/templates",
            "mcp_servers": "/api/v1/mcp-servers",
            "mcp_tools": "/api/v1/mcp-servers/tools/all",
            "workflows": "/api/v1/workflows",
            "workflow_executions": "/api/v1/workflows/executions"
        }
    )

# 애플리케이션 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행되는 이벤트"""
    print("🚀 AI Agent Builder Backend 시작됨")
    print(f"🌐 API 문서: http://localhost:8000/docs")
    print(f"🔍 ReDoc: http://localhost:8000/redoc")
    print("📡 사용 가능한 엔드포인트:")
    print("  - GET  /api/v1/agents (Agent 목록)")
    print("  - POST /api/v1/agents (Agent 생성)")
    print("  - GET  /api/v1/agents/templates (Agent 템플릿)")
    print("  - GET  /api/v1/mcp-servers (MCP 서버 목록)")
    print("  - POST /api/v1/mcp-servers (MCP 서버 추가)")
    print("  - GET  /api/v1/workflows (워크플로우 목록)")
    print("  - POST /api/v1/workflows (워크플로우 생성)")
    
    # 데이터베이스 테이블 생성 (개발 환경에서만)
    if os.getenv("ENVIRONMENT") == "development":
        try:
            from database.connection import create_tables
            create_tables()
            print("✅ 데이터베이스 테이블이 생성되었습니다.")
        except Exception as e:
            print(f"⚠️  데이터베이스 테이블 생성 실패: {e}")

# 애플리케이션 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행되는 이벤트"""
    print("🛑 AI Agent Builder Backend 종료됨")

# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리기"""
    print(f"❌ 예외 발생: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다.",
                "details": str(exc) if os.getenv("ENVIRONMENT") == "development" else None
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 