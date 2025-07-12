#!/usr/bin/env python3
"""
AI Agent Builder - MCP Configuration
MCP 설정 관리
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

class MCPConfig(BaseModel):
    """MCP 설정"""
    default_timeout: int = int(os.getenv("MCP_TIMEOUT", "30"))
    max_connections: int = int(os.getenv("MCP_MAX_CONNECTIONS", "10"))

# 설정 출력
MCP_CONFIG = MCPConfig().dict()
print("MCP Config loaded:", MCP_CONFIG) 