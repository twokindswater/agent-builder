#!/usr/bin/env python3
"""
AI Agent Builder - Configuration
환경 변수 및 애플리케이션 설정 관리
"""

import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

class DatabaseConfig(BaseModel):
    """데이터베이스 설정"""
    url: str = os.getenv("DATABASE_URL", "sqlite:///./agent_builder.db")
    echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

class AIConfig(BaseModel):
    """AI API 설정"""
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")

class MCPConfig(BaseModel):
    """MCP 설정"""
    default_timeout: int = int(os.getenv("MCP_TIMEOUT", "30"))
    max_connections: int = int(os.getenv("MCP_MAX_CONNECTIONS", "10"))

class SecurityConfig(BaseModel):
    """보안 설정"""
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class Config(BaseModel):
    """애플리케이션 전체 설정"""
    # 기본 설정
    app_name: str = "AI Agent Builder"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 서버 설정
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # 세부 설정
    database: DatabaseConfig = DatabaseConfig()
    ai: AIConfig = AIConfig()
    mcp: MCPConfig = MCPConfig()
    security: SecurityConfig = SecurityConfig()
    
    # CORS 설정
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    class Config:
        """Pydantic 설정"""
        case_sensitive = True

# 글로벌 설정 인스턴스
settings = Config()

# 환경별 설정 확인
def get_config() -> Config:
    """현재 환경에 맞는 설정 반환"""
    return settings

def is_development() -> bool:
    """개발 환경인지 확인"""
    return settings.debug

def is_production() -> bool:
    """프로덕션 환경인지 확인"""
    return not settings.debug 