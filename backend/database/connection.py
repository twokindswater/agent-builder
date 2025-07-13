"""
Database connection configuration
"""

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from config.database import DB_CONFIG
from typing import Generator

# SQLAlchemy 설정
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 생성
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db() -> Generator[Session, None, None]:
    """
    테스트용 데이터베이스 세션 생성
    """
    # 실제 환경에서는 테스트 데이터베이스를 사용해야 하지만,
    # 현재는 개발 단계이므로 동일한 데이터베이스를 사용
    return get_db()

# 데이터베이스 연결 설정
DB_CONN_CONFIG = {
    'dbname': DB_CONFIG['dbname'],
    'user': DB_CONFIG['user'],
    'password': DB_CONFIG['password'],
    'host': DB_CONFIG['host'],
    'port': DB_CONFIG['port'],
    'sslmode': 'require'  # SSL 모드 필수
}

# 연결 풀 생성 (최소 1개, 최대 20개의 연결 유지)
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    **DB_CONN_CONFIG
)

@contextmanager
def get_db_cursor(commit=False):
    """데이터베이스 커서 생성 (연결 풀 사용)"""
    conn = None
    try:
        # 풀에서 연결 가져오기
        conn = pool.getconn()
        cur = conn.cursor()
        yield cur
        if commit:
            conn.commit()
        cur.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            # 연결을 풀로 반환
            pool.putconn(conn)

def close_pool():
    """애플리케이션 종료 시 연결 풀 정리"""
    if pool:
        pool.closeall()

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
                
                -- Mock 사용자 추가 (이미 존재하지 않는 경우)
                INSERT INTO users (id, email)
                VALUES ('00000000-0000-0000-0000-000000000001', 'test@example.com')
                ON CONFLICT (id) DO NOTHING;
            """)
            
            # agents 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id),
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            
            # mcp_servers 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mcp_servers (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id),
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
                    definition JSONB,
                    status TEXT NOT NULL DEFAULT 'active',
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