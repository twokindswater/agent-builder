# Core Features Tasks
> PRD 섹션: [tasks/prd.txt](mdc:tasks/prd.txt)의 Core Features 참조

## 우선순위: High
- [ ] (High) AI Agent 생성 기능 구현 - 템플릿 기반 Agent 생성 및 설정 관리
  - 의존성: 데이터베이스 모델 구현, AI API 연동 기반 구조 완료
  - 완료 기준: Agent 생성 폼에서 이름, 설명, 프롬프트, AI 모델 선택 후 저장/수정 가능
  - 산출물: backend/services/agent_service.py, frontend/pages/agent-creator.html

- [ ] (High) AI Agent 템플릿 시스템 구현 - 사전 정의된 Agent 템플릿 제공
  - 의존성: AI Agent 생성 기능 구현 완료
  - 완료 기준: 챗봇, 데이터 분석, 크리에이티브 등 5개 기본 템플릿 제공
  - 산출물: backend/templates/agent_templates.json, backend/services/template_service.py

- [ ] (High) MCP 서버 연결 기능 구현 - 외부 MCP 서버 연결 및 도구 관리
  - 의존성: MCP 클라이언트 기본 구현 완료
  - 완료 기준: MCP 서버 URL 입력, 연결 테스트, 사용 가능한 도구 목록 조회 가능
  - 산출물: backend/services/mcp_service.py, frontend/pages/mcp-connection.html

- [ ] (High) 기본 워크플로우 생성 기능 구현 - 단순한 노드 기반 워크플로우 생성
  - 의존성: AI Agent 생성 기능, MCP 서버 연결 기능 완료
  - 완료 기준: Agent 노드, MCP 도구 노드를 연결하여 간단한 워크플로우 생성 가능
  - 산출물: backend/services/workflow_service.py, frontend/pages/workflow-builder.html

## 우선순위: Medium
- [ ] (Medium) 드래그&드롭 워크플로우 빌더 구현 - 시각적 노드 기반 워크플로우 편집기
  - 의존성: 기본 워크플로우 생성 기능 완료
  - 완료 기준: 노드 드래그&드롭, 노드 간 연결, 워크플로우 시각화 기능 구현
  - 산출물: frontend/js/workflow-builder.js, frontend/css/workflow-builder.css

- [ ] (Medium) 워크플로우 실행 엔진 구현 - 워크플로우 순차/병렬 실행 로직
  - 의존성: 기본 워크플로우 생성 기능 완료
  - 완료 기준: 워크플로우 노드 순서대로 실행, 결과 전달, 에러 처리 구현
  - 산출물: backend/services/workflow_executor.py, backend/models/workflow_execution.py

- [ ] (Medium) 실시간 모니터링 대시보드 구현 - 워크플로우 실행 상태 실시간 표시
  - 의존성: 워크플로우 실행 엔진, WebSocket 통신 구현 완료
  - 완료 기준: 실행 중인 워크플로우 상태, 진행률, 결과 실시간 표시 가능
  - 산출물: frontend/pages/monitoring-dashboard.html, frontend/js/monitoring.js

- [ ] (Medium) 템플릿 라이브러리 구현 - 워크플로우 템플릿 저장/불러오기
  - 의존성: 워크플로우 실행 엔진 구현 완료
  - 완료 기준: 워크플로우 템플릿 저장, 카테고리별 분류, 템플릿 불러오기 기능 구현
  - 산출물: backend/services/template_library.py, frontend/pages/template-library.html

## 우선순위: Low
- [ ] (Low) 고급 워크플로우 노드 구현 - 조건문, 반복문, 데이터 처리 노드
  - 의존성: 워크플로우 실행 엔진 구현 완료
  - 완료 기준: IF 조건문, FOR 반복문, 데이터 변환 노드 구현 및 테스트
  - 산출물: backend/nodes/condition_node.py, backend/nodes/loop_node.py, backend/nodes/data_node.py

- [ ] (Low) 워크플로우 버전 관리 구현 - 워크플로우 변경 이력 관리
  - 의존성: 워크플로우 실행 엔진 구현 완료
  - 완료 기준: 워크플로우 수정 시 버전 생성, 이전 버전 복구 기능 구현
  - 산출물: backend/services/version_service.py, backend/models/workflow_version.py

- [ ] (Low) 협업 기능 기초 구현 - 워크플로우 공유 및 권한 관리
  - 의존성: 사용자 인증 시스템 구현 완료
  - 완료 기준: 워크플로우 공유 링크 생성, 읽기/쓰기 권한 설정 기능 구현
  - 산출물: backend/services/collaboration_service.py, backend/models/workflow_share.py 