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

# Supabase 데이터베이스 설정
DBNAME = os.getenv("DBNAME", "postgres")
USER = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "")
HOST = os.getenv("DB_HOST", "")
PORT = os.getenv("DB_PORT", "5432")

class DatabaseConfig(BaseModel):
    """데이터베이스 설정"""
    dbname: str = DBNAME
    user: str = USER
    password: str = PASSWORD
    host: str = HOST
    port: str = PORT
    echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

# 설정 출력
DB_CONFIG = DatabaseConfig().dict()
print("Database Config loaded:", {k: v if k != 'password' else '****' for k, v in DB_CONFIG.items()})