"""
MCP (Model Context Protocol) API endpoints
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse, Response
import json

from schemas.mcp import (
    MCPServerCreate, MCPServerUpdate, MCPServerResponse, 
    MCPServerWithTools, MCPToolResponse,
    MCPConnectionTestResponse, MCPToolSyncResponse
)
from schemas.common import APIResponse
from database.connection import get_db_cursor

# 개발 환경용 mock 사용자 ID
MOCK_USER_ID = "00000000-0000-0000-0000-000000000001"

router = APIRouter(prefix="/mcp-servers", tags=["mcp"])

@router.get("", response_model=APIResponse[List[MCPServerResponse]])
async def get_mcp_servers():
    """사용자의 MCP 서버 목록 조회"""
    try:
        with get_db_cursor() as cur:
            cur.execute("""
                SELECT id, name, url, api_key, created_at, updated_at
                FROM mcp_servers
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (MOCK_USER_ID,))
            results = cur.fetchall()
            
            servers = [
                MCPServerResponse(
                    id=str(row[0]),
                    name=row[1],
                    url=row[2],
                    api_key=row[3],
                    created_at=row[4],
                    updated_at=row[5]
                ) for row in results
            ]
            
            return APIResponse(
                success=True,
                data=servers,
                message="MCP 서버 목록을 성공적으로 조회했습니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{server_id}", response_model=APIResponse[MCPServerWithTools])
async def get_mcp_server(server_id: str):
    """특정 MCP 서버 상세 조회 (도구 목록 포함)"""
    try:
        with get_db_cursor() as cur:
            # 서버 정보 조회
            cur.execute("""
                SELECT id, name, url, api_key, created_at, updated_at
                FROM mcp_servers
                WHERE id = %s AND user_id = %s
            """, (server_id, MOCK_USER_ID))
            server = cur.fetchone()
            
            if not server:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            # 서버의 도구 목록 조회
            cur.execute("""
                SELECT id, name, description, parameters, created_at, updated_at
                FROM mcp_tools
                WHERE server_id = %s
                ORDER BY created_at DESC
            """, (server_id,))
            tools = cur.fetchall()
            
            server_response = MCPServerResponse(
                id=str(server[0]),
                name=server[1],
                url=server[2],
                api_key=server[3],
                created_at=server[4],
                updated_at=server[5]
            )
            
            tools_response = [
                MCPToolResponse(
                    id=str(tool[0]),
                    name=tool[1],
                    description=tool[2],
                    parameters=tool[3],
                    created_at=tool[4],
                    updated_at=tool[5]
                ) for tool in tools
            ]
            
            return APIResponse(
                success=True,
                data=MCPServerWithTools(
                    **server_response.model_dump(mode='json'),
                    tools=tools_response
                ),
                message="MCP 서버 정보를 성공적으로 조회했습니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("", response_model=APIResponse[MCPServerResponse])
async def create_mcp_server(server: MCPServerCreate):
    """새로운 MCP 서버 등록"""
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO mcp_servers (name, url, api_key, user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, url, api_key, created_at, updated_at;
            """, (
                server.name,
                server.url,
                server.api_key,
                MOCK_USER_ID
            ))
            result = cur.fetchone()
            
            new_server = MCPServerResponse(
                id=str(result[0]),
                name=result[1],
                url=result[2],
                api_key=result[3],
                created_at=result[4],
                updated_at=result[5]
            )
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "data": new_server.model_dump(mode='json'),
                    "message": "MCP 서버가 성공적으로 등록되었습니다."
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{server_id}", response_model=APIResponse[MCPServerResponse])
async def update_mcp_server(server_id: str, server: MCPServerUpdate):
    """MCP 서버 정보 수정"""
    try:
        with get_db_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE mcp_servers
                SET name = %s,
                    url = %s,
                    api_key = %s,
                    updated_at = NOW()
                WHERE id = %s AND user_id = %s
                RETURNING id, name, url, api_key, created_at, updated_at;
            """, (
                server.name,
                server.url,
                server.api_key,
                server_id,
                MOCK_USER_ID
            ))
            result = cur.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            updated_server = MCPServerResponse(
                id=str(result[0]),
                name=result[1],
                url=result[2],
                api_key=result[3],
                created_at=result[4],
                updated_at=result[5]
            )
            
            return APIResponse(
                success=True,
                data=updated_server,
                message="MCP 서버 정보가 성공적으로 수정되었습니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{server_id}", response_model=None)
async def delete_mcp_server(server_id: str):
    """MCP 서버 삭제"""
    try:
        with get_db_cursor(commit=True) as cur:
            # 먼저 연결된 도구들을 삭제
            cur.execute("""
                DELETE FROM mcp_tools
                WHERE server_id = %s;
            """, (server_id,))
            
            # 서버 삭제
            cur.execute("""
                DELETE FROM mcp_servers
                WHERE id = %s AND user_id = %s
                RETURNING id;
            """, (server_id, MOCK_USER_ID))
            result = cur.fetchone()
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{server_id}/test", response_model=APIResponse[MCPConnectionTestResponse])
async def test_mcp_connection(server_id: str):
    """MCP 서버 연결 테스트"""
    try:
        with get_db_cursor() as cur:
            # 서버 정보 조회
            cur.execute("""
                SELECT id, name, url, api_key
                FROM mcp_servers
                WHERE id = %s AND user_id = %s
            """, (server_id, MOCK_USER_ID))
            server = cur.fetchone()
            
            if not server:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            # 실제로는 여기서 MCP 서버에 연결 테스트를 수행해야 하지만,
            # 테스트 환경에서는 항상 성공으로 처리
            return APIResponse(
                success=True,
                data=MCPConnectionTestResponse(
                    success=True,
                    message="MCP 서버 연결 테스트가 성공적으로 완료되었습니다.",
                    tools_count=0
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
async def sync_mcp_tools(server_id: str):
    """MCP 서버의 도구 목록 동기화"""
    try:
        with get_db_cursor(commit=True) as cur:
            # 서버 정보 조회
            cur.execute("""
                SELECT id, name, url, api_key
                FROM mcp_servers
                WHERE id = %s AND user_id = %s
            """, (server_id, MOCK_USER_ID))
            server = cur.fetchone()
            
            if not server:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            # 실제로는 여기서 MCP 서버의 도구 목록을 가져와서 동기화해야 하지만,
            # 테스트 환경에서는 Mock 데이터 사용
            mock_tools = [
                {
                    "name": "test_tool_1",
                    "description": "테스트 도구 1",
                    "parameters": {"param1": "string", "param2": "number"}
                },
                {
                    "name": "test_tool_2",
                    "description": "테스트 도구 2",
                    "parameters": {"param1": "boolean"}
                }
            ]
            
            # 기존 도구 삭제
            cur.execute("""
                DELETE FROM mcp_tools
                WHERE server_id = %s
                RETURNING id
            """, (server_id,))
            removed_count = len(cur.fetchall())
            
            # 새로운 도구 추가
            for tool in mock_tools:
                cur.execute("""
                    INSERT INTO mcp_tools (server_id, name, description, parameters)
                    VALUES (%s, %s, %s, %s::jsonb)
                """, (
                    server_id,
                    tool["name"],
                    tool["description"],
                    json.dumps(tool["parameters"])
                ))
            
            return APIResponse(
                success=True,
                data=MCPToolSyncResponse(
                    success=True,
                    message="MCP 서버의 도구 목록이 성공적으로 동기화되었습니다.",
                    synced_tools=len(mock_tools),
                    removed_tools=removed_count
                ),
                message="MCP 서버의 도구 목록이 성공적으로 동기화되었습니다."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{server_id}/tools", response_model=APIResponse[List[MCPToolResponse]])
async def get_server_tools(server_id: uuid.UUID):
    """특정 MCP 서버의 도구 목록 조회"""
    try:
        with get_db_cursor() as cur:
            # 서버 정보 조회
            cur.execute("""
                SELECT id, name, url, api_key, created_at, updated_at
                FROM mcp_servers
                WHERE id = %s AND user_id = %s
            """, (server_id, MOCK_USER_ID))
            server = cur.fetchone()
            
            if not server:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="MCP 서버를 찾을 수 없습니다."
                )
            
            # 서버의 도구 목록 조회
            cur.execute("""
                SELECT id, name, description, parameters, created_at, updated_at
                FROM mcp_tools
                WHERE server_id = %s
                ORDER BY created_at DESC
            """, (server_id,))
            tools = cur.fetchall()
            
            tools_response = [
                MCPToolResponse(
                    id=str(tool[0]),
                    name=tool[1],
                    description=tool[2],
                    parameters=tool[3],
                    created_at=tool[4],
                    updated_at=tool[5]
                ) for tool in tools
            ]
            
            return APIResponse(
                success=True,
                data=tools_response,
                message="MCP 서버 도구 목록을 성공적으로 조회했습니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# 전체 MCP 도구 목록 조회 (사용자별)
@router.get("/tools/all", response_model=APIResponse[List[MCPToolResponse]])
async def get_all_mcp_tools():
    """사용자의 모든 MCP 도구 목록 조회"""
    try:
        with get_db_cursor() as cur:
            cur.execute("""
                SELECT mt.id, mt.name, mt.description, mt.parameters, mt.created_at, mt.updated_at
                FROM mcp_tools mt
                JOIN mcp_servers ms ON mt.server_id = ms.id
                WHERE ms.user_id = %s
                ORDER BY mt.created_at DESC;
            """, (MOCK_USER_ID,))
            tools = cur.fetchall()
            
            tools_response = [
                MCPToolResponse(
                    id=str(tool[0]),
                    name=tool[1],
                    description=tool[2],
                    parameters=tool[3],
                    created_at=tool[4],
                    updated_at=tool[5]
                ) for tool in tools
            ]
            
            return APIResponse(
                success=True,
                data=tools_response,
                message="전체 MCP 도구 목록을 성공적으로 조회했습니다."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 