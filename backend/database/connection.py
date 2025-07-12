"""
Database connection configuration
"""

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from config.database import DB_CONFIG

# psycopg2용 설정에서 echo 옵션 제거
DB_CONN_CONFIG = {k: v for k, v in DB_CONFIG.items() if k != 'echo'}

@contextmanager
def get_db_connection():
    """데이터베이스 연결 생성"""
    connection = None
    try:
        connection = psycopg2.connect(**DB_CONN_CONFIG)
        yield connection
    finally:
        if connection is not None:
            connection.close()

@contextmanager
def get_db_cursor(commit=False):
    """데이터베이스 커서 생성"""
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**DB_CONN_CONFIG)
        cursor = connection.cursor()
        yield cursor
        if commit:
            connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# SQLAlchemy 설정 (ORM 사용시)
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(DATABASE_URL, echo=DB_CONFIG.get('echo', False))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """SQLAlchemy 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """데이터베이스 연결 테스트"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT NOW();")
            result = cursor.fetchone()
            print("데이터베이스 연결 성공!")
            print("현재 시간:", result[0])
            return True
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        return False

def create_tables():
    """데이터베이스 테이블 생성"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # users 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            
            # agents 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id),
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            
            # mcp_servers 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mcp_servers (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    api_key TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            # mcp_tools 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mcp_tools (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    server_id UUID NOT NULL REFERENCES mcp_servers(id),
                    name TEXT NOT NULL,
                    description TEXT,
                    parameters JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            # workflows 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workflows (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    agent_id UUID NOT NULL REFERENCES agents(id),
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            # workflow_executions 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workflow_executions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    workflow_id UUID NOT NULL REFERENCES workflows(id),
                    status TEXT NOT NULL,
                    result JSONB,
                    started_at TIMESTAMPTZ DEFAULT NOW(),
                    completed_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            
            print("테이블 생성 완료!")
            return True
    except Exception as e:
        print(f"테이블 생성 실패: {e}")
        return False

def drop_tables():
    """데이터베이스 테이블 삭제 (개발용)"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                DROP TABLE IF EXISTS 
                    workflow_executions,
                    workflows,
                    mcp_tools,
                    mcp_servers,
                    agents,
                    users
                CASCADE;
            """)
            print("테이블 삭제 완료!")
            return True
    except Exception as e:
        print(f"테이블 삭제 실패: {e}")
        return False 