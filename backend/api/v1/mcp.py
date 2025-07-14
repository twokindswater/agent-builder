"""
MCP (Model Context Protocol) API endpoints
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from schemas.mcp import (
    MCPServerCreate, MCPServerUpdate, MCPServerResponse, 
    MCPServerWithTools, MCPToolResponse,
    MCPConnectionTestResponse, MCPToolSyncResponse
)
from schemas.common import APIResponse
from database.connection import get_db
from models import MCPServer

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/mcp-servers", tags=["mcp"])

@router.get("", response_model=APIResponse[List[MCPServerResponse]])
async def get_mcp_servers(db: Session = Depends(get_db)):
    """사용자의 MCP 서버 목록 조회"""
    try:
        servers = db.query(MCPServer).all()
        server_responses = [MCPServerResponse.model_validate(server) for server in servers]
        return APIResponse(
            success=True,
            data=server_responses,
            message="MCP 서버 목록을 성공적으로 조회했습니다."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{server_id}", response_model=APIResponse[MCPServerResponse])
async def get_mcp_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    """특정 MCP 서버 조회"""
    try:
        server = db.query(MCPServer).filter(MCPServer.id == server_id).first()
        if not server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MCP 서버를 찾을 수 없습니다."
            )
        server_response = MCPServerResponse.model_validate(server)
        return APIResponse(
            success=True,
            data=server_response,
            message="MCP 서버 정보를 성공적으로 조회했습니다."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("", response_model=APIResponse[MCPServerResponse])
async def create_mcp_server(server: MCPServerCreate, db: Session = Depends(get_db)):
    """새로운 MCP 서버 등록"""
    try:
        new_server = MCPServer(
            name=server.name,
            url=server.url,
            api_key=server.api_key,
            description=server.description,
            user_id=server.user_id
        )
        db.add(new_server)
        db.commit()
        db.refresh(new_server)
        
        # SQLAlchemy 모델을 Pydantic 모델로 변환
        server_response = MCPServerResponse.model_validate(new_server)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "data": server_response.model_dump(mode='json'),
                "message": "MCP 서버가 성공적으로 등록되었습니다."
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{server_id}", response_model=APIResponse[MCPServerResponse])
async def update_mcp_server(
    server_id: uuid.UUID,
    server: MCPServerUpdate,
    db: Session = Depends(get_db)
):
    """MCP 서버 정보 수정"""
    try:
        db_server = db.query(MCPServer).filter(MCPServer.id == server_id).first()
        if not db_server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MCP 서버를 찾을 수 없습니다."
            )
        
        if server.name is not None:
            db_server.name = server.name
        if server.url is not None:
            db_server.url = server.url
        if server.api_key is not None:
            db_server.api_key = server.api_key
        if server.description is not None:
            db_server.description = server.description
            
        db.commit()
        db.refresh(db_server)
        
        server_response = MCPServerResponse.model_validate(db_server)
        return APIResponse(
            success=True,
            data=server_response,
            message="MCP 서버 정보가 성공적으로 수정되었습니다."
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{server_id}", response_model=None)
async def delete_mcp_server(server_id: uuid.UUID, db: Session = Depends(get_db)):
    """MCP 서버 삭제"""
    try:
        server = db.query(MCPServer).filter(MCPServer.id == server_id).first()
        if not server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MCP 서버를 찾을 수 없습니다."
            )
        
        db.delete(server)
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{server_id}/test", response_model=APIResponse[MCPConnectionTestResponse])
async def test_mcp_connection(server_id: uuid.UUID, db: Session = Depends(get_db)):
    """MCP 서버 연결 테스트"""
    try:
        server = db.query(MCPServer).filter(MCPServer.id == server_id).first()
        if not server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MCP 서버를 찾을 수 없습니다."
            )
        
        # 실제 연결 테스트는 생략 (mock)
        return APIResponse(
            success=True,
            data=MCPConnectionTestResponse(
                success=True,
                message="연결 테스트 성공",
                tools_count=10
            ),
            message="MCP 서버 연결 테스트가 성공적으로 완료되었습니다."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{server_id}/sync", response_model=APIResponse[MCPToolSyncResponse])
async def sync_mcp_tools(server_id: uuid.UUID, db: Session = Depends(get_db)):
    """MCP 서버 도구 동기화"""
    try:
        server = db.query(MCPServer).filter(MCPServer.id == server_id).first()
        if not server:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MCP 서버를 찾을 수 없습니다."
            )
        
        # 실제 동기화는 생략 (mock)
        return APIResponse(
            success=True,
            data=MCPToolSyncResponse(
                success=True,
                message="도구 동기화 성공",
                synced_tools=5,
                removed_tools=0
            ),
            message="MCP 서버 도구 동기화가 성공적으로 완료되었습니다."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 