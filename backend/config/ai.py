#!/usr/bin/env python3
"""
AI Agent Builder - AI Configuration
AI API 설정 관리
"""

import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 파일 로드
load_dotenv()

class AIConfig(BaseModel):
    """AI API 설정"""
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")

# 설정 출력
AI_CONFIG = AIConfig().dict()
print("AI Config loaded:", {k: v if v is None else '****' for k, v in AI_CONFIG.items()}) 