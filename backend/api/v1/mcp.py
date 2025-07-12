"""
MCP (Model Context Protocol) API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from schemas.mcp import (
    MCPServerCreate, MCPServerUpdate, MCPServerResponse, 
    MCPServerWithTools, MCPToolResponse,
    MCPConnectionTestResponse, MCPToolSyncResponse
)
from schemas.common import APIResponse
from models.database import MCPServer, MCPTool
from database.connection import get_db

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/mcp-servers", tags=["mcp"])

@router.get("", response_model=APIResponse[List[MCPServerResponse]])
async def get_mcp_servers(
    db: Session = Depends(get_db)
):
    """사용자의 MCP 서버 목록 조회"""
    servers = db.query(MCPServer).filter(
        MCPServer.user_id == MOCK_USER_ID
    ).all()
    
    return APIResponse(
        success=True,
        data=[MCPServerResponse.from_orm(server) for server in servers],
        message="MCP 서버 목록을 성공적으로 조회했습니다."
    )

@router.post("", response_model=APIResponse[MCPServerResponse])
async def create_mcp_server(
    server: MCPServerCreate,
    db: Session = Depends(get_db)
):
    """새 MCP 서버 추가"""
    # TODO: 토큰 암호화 로직 추가
    encrypted_token = server.token if server.token else None
    
    db_server = MCPServer(
        user_id=MOCK_USER_ID,
        name=server.name,
        url=server.url,
        description=server.description,
        encrypted_token=encrypted_token
    )
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    
    return APIResponse(
        success=True,
        data=MCPServerResponse.from_orm(db_server),
        message="MCP 서버가 성공적으로 추가되었습니다."
    )

@router.get("/{server_id}", response_model=APIResponse[MCPServerWithTools])
async def get_mcp_server(
    server_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """특정 MCP 서버 상세 조회 (도구 목록 포함)"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    # 서버의 도구 목록 조회
    tools = db.query(MCPTool).filter(MCPTool.server_id == server_id).all()
    
    server_data = MCPServerResponse.from_orm(server)
    server_with_tools = MCPServerWithTools(
        **server_data.dict(),
        tools=[MCPToolResponse.from_orm(tool) for tool in tools]
    )
    
    return APIResponse(
        success=True,
        data=server_with_tools,
        message="MCP 서버 정보를 성공적으로 조회했습니다."
    )

@router.put("/{server_id}", response_model=APIResponse[MCPServerResponse])
async def update_mcp_server(
    server_id: uuid.UUID,
    server_update: MCPServerUpdate,
    db: Session = Depends(get_db)
):
    """MCP 서버 정보 수정"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    # 업데이트할 필드만 적용
    update_data = server_update.dict(exclude_unset=True)
    
    # 토큰이 업데이트되는 경우 암호화
    if "token" in update_data:
        # TODO: 토큰 암호화 로직 추가
        update_data["encrypted_token"] = update_data.pop("token")
    
    for field, value in update_data.items():
        setattr(server, field, value)
    
    db.commit()
    db.refresh(server)
    
    return APIResponse(
        success=True,
        data=MCPServerResponse.from_orm(server),
        message="MCP 서버 정보가 성공적으로 수정되었습니다."
    )

@router.delete("/{server_id}", response_model=APIResponse[dict])
async def delete_mcp_server(
    server_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """MCP 서버 삭제"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    db.delete(server)
    db.commit()
    
    return APIResponse(
        success=True,
        data={"deleted_id": str(server_id)},
        message="MCP 서버가 성공적으로 삭제되었습니다."
    )

@router.post("/{server_id}/connect", response_model=APIResponse[MCPConnectionTestResponse])
async def test_mcp_connection(
    server_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """MCP 서버 연결 테스트"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    # TODO: 실제 MCP 서버 연결 테스트 로직 구현
    # 현재는 Mock 응답 반환
    try:
        # Mock 연결 테스트
        import time
        time.sleep(0.5)  # 연결 시뮬레이션
        
        # 연결 상태 업데이트
        server.is_connected = True
        server.last_connected_at = db.func.now()
        db.commit()
        
        return APIResponse(
            success=True,
            data=MCPConnectionTestResponse(
                success=True,
                message="MCP 서버 연결이 성공했습니다.",
                tools_count=3  # Mock 도구 개수
            ),
            message="MCP 서버 연결 테스트가 성공했습니다."
        )
        
    except Exception as e:
        server.is_connected = False
        db.commit()
        
        return APIResponse(
            success=False,
            data=MCPConnectionTestResponse(
                success=False,
                message="MCP 서버 연결에 실패했습니다.",
                error=str(e)
            ),
            message="MCP 서버 연결 테스트가 실패했습니다."
        )

@router.post("/{server_id}/sync-tools", response_model=APIResponse[MCPToolSyncResponse])
async def sync_mcp_tools(
    server_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """MCP 서버의 도구 목록 동기화"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    if not server.is_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MCP 서버가 연결되지 않았습니다. 먼저 연결 테스트를 수행해주세요."
        )
    
    # TODO: 실제 MCP 서버 도구 동기화 로직 구현
    # 현재는 Mock 응답 반환
    try:
        # 기존 도구 목록 삭제
        existing_tools = db.query(MCPTool).filter(MCPTool.server_id == server_id).all()
        for tool in existing_tools:
            db.delete(tool)
        
        # Mock 도구 생성
        mock_tools = [
            {
                "name": "file_search",
                "description": "파일 검색 도구",
                "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
                "output_schema": {"type": "object", "properties": {"results": {"type": "array"}}}
            },
            {
                "name": "code_edit",
                "description": "코드 편집 도구",
                "input_schema": {"type": "object", "properties": {"file": {"type": "string"}, "content": {"type": "string"}}},
                "output_schema": {"type": "object", "properties": {"success": {"type": "boolean"}}}
            },
            {
                "name": "web_search",
                "description": "웹 검색 도구",
                "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
                "output_schema": {"type": "object", "properties": {"results": {"type": "array"}}}
            }
        ]
        
        synced_count = 0
        for tool_data in mock_tools:
            tool = MCPTool(
                server_id=server_id,
                **tool_data
            )
            db.add(tool)
            synced_count += 1
        
        db.commit()
        
        return APIResponse(
            success=True,
            data=MCPToolSyncResponse(
                success=True,
                message="도구 목록이 성공적으로 동기화되었습니다.",
                synced_tools=synced_count,
                removed_tools=len(existing_tools)
            ),
            message="MCP 서버 도구 동기화가 완료되었습니다."
        )
        
    except Exception as e:
        db.rollback()
        return APIResponse(
            success=False,
            data=MCPToolSyncResponse(
                success=False,
                message="도구 동기화 중 오류가 발생했습니다.",
                synced_tools=0,
                removed_tools=0,
                error=str(e)
            ),
            message="MCP 서버 도구 동기화가 실패했습니다."
        )

@router.get("/{server_id}/tools", response_model=APIResponse[List[MCPToolResponse]])
async def get_server_tools(
    server_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """특정 MCP 서버의 도구 목록 조회"""
    server = db.query(MCPServer).filter(
        MCPServer.id == server_id,
        MCPServer.user_id == MOCK_USER_ID
    ).first()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCP 서버를 찾을 수 없습니다."
        )
    
    tools = db.query(MCPTool).filter(MCPTool.server_id == server_id).all()
    
    return APIResponse(
        success=True,
        data=[MCPToolResponse.from_orm(tool) for tool in tools],
        message="MCP 서버 도구 목록을 성공적으로 조회했습니다."
    )

# 전체 MCP 도구 목록 조회 (사용자별)
@router.get("/tools/all", response_model=APIResponse[List[MCPToolResponse]])
async def get_all_mcp_tools(
    db: Session = Depends(get_db)
):
    """사용자의 모든 MCP 도구 목록 조회"""
    tools = db.query(MCPTool).join(MCPServer).filter(
        MCPServer.user_id == MOCK_USER_ID
    ).all()
    
    return APIResponse(
        success=True,
        data=[MCPToolResponse.from_orm(tool) for tool in tools],
        message="전체 MCP 도구 목록을 성공적으로 조회했습니다."
    ) 