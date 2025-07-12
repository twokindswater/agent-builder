#!/usr/bin/env python3
"""
AI Agent Builder - Base Configuration
기본 설정 클래스 정의
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

class BaseConfig(BaseModel):
    """기본 설정"""
    app_name: str = "AI Agent Builder"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 서버 설정
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # CORS 설정
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    class Config:
        """Pydantic 설정"""
        case_sensitive = True

# 설정 출력
print("Base Config loaded:", BaseConfig().dict()) 