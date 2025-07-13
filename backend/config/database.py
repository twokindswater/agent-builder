#!/usr/bin/env python3
"""
AI Agent Builder - Database Configuration
데이터베이스 설정 관리
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

# Supabase 데이터베이스 설정 (Session Pooler 사용)
USER = os.getenv("DB_USER", "")
PASSWORD = os.getenv("DB_PASSWORD", "")
HOST = os.getenv("DB_HOST", "")
PORT = os.getenv("DB_PORT", "")
DBNAME = os.getenv("DB_NAME", "postgres")

class DatabaseConfig(BaseModel):
    """데이터베이스 설정"""
    user: str = USER
    password: str = PASSWORD
    host: str = HOST
    port: str = PORT
    dbname: str = DBNAME

# 설정 출력
DB_CONFIG = DatabaseConfig().dict()
print("Database Config loaded:", {k: v if k != 'password' else '****' for k, v in DB_CONFIG.items()})