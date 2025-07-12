"""
AI Agent Builder - Configuration
설정 모듈 초기화
"""

from .base import BaseConfig
from .database import DatabaseConfig, DB_CONFIG
from .ai import AIConfig, AI_CONFIG
from .mcp import MCPConfig, MCP_CONFIG
from .security import SecurityConfig, SECURITY_CONFIG

class Config(BaseConfig):
    """통합 설정"""
    database: DatabaseConfig = DatabaseConfig()
    ai: AIConfig = AIConfig()
    mcp: MCPConfig = MCPConfig()
    security: SecurityConfig = SecurityConfig()

# 글로벌 설정 인스턴스
settings = Config()

def get_config() -> Config:
    """현재 환경에 맞는 설정 반환"""
    return settings

def is_development() -> bool:
    """개발 환경인지 확인"""
    return settings.debug

def is_production() -> bool:
    """프로덕션 환경인지 확인"""
    return not settings.debug

# 설정 출력
print("\nFinal Config loaded:", settings.dict()) 