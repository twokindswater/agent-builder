"""
Authentication middleware for Supabase JWT tokens
"""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
from typing import Optional
from config.supabase import supabase, SUPABASE_URL, SUPABASE_ANON_KEY

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Supabase JWT 토큰 검증"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 인증 정보입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 개발 환경에서는 토큰 검증 생략
        if os.getenv("ENVIRONMENT") == "development":
            return {
                "sub": "00000000-0000-0000-0000-000000000001",  # Mock 사용자 ID
                "email": "test@example.com",
                "role": "authenticated"
            }
        
        # Supabase 토큰 검증
        user = supabase.auth.get_user(credentials.credentials)
        if not user:
            raise credentials_exception
            
        return {
            "sub": user.id,
            "email": user.email,
            "role": "authenticated"
        }
        
    except Exception as e:
        raise credentials_exception

def get_current_user(token_data: dict = Depends(verify_token)) -> str:
    """현재 인증된 사용자의 ID 반환"""
    return token_data["sub"] 