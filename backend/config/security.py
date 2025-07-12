#!/usr/bin/env python3
"""
AI Agent Builder - Security Configuration
보안 설정 관리
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

class SecurityConfig(BaseModel):
    """보안 설정"""
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 설정 출력
SECURITY_CONFIG = SecurityConfig().dict()
print("Security Config loaded:", {k: v if k != 'secret_key' else '****' for k, v in SECURITY_CONFIG.items()}) 