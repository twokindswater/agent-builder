# Overview Tasks
> PRD 섹션: [tasks/prd.txt](mdc:tasks/prd.txt)의 Overview 참조

## 우선순위: High
- [ ] (High) 프로젝트 기본 구조 설정 - Git 저장소 초기화, 폴더 구조 생성, .gitignore 설정
  - 의존성: 없음
  - 완료 기준: 프로젝트 루트 폴더에 frontend/, backend/, docs/, tests/ 폴더 생성
  - 산출물: 프로젝트 폴더 구조

- [ ] (High) 백엔드 프로젝트 초기 설정 - Conda 환경(Python 3.12), FastAPI 설치, 기본 구조 생성
  - 의존성: 프로젝트 기본 구조 설정 완료
  - 완료 기준: backend/app.py 파일에서 "Hello World" API 엔드포인트 실행 가능
  - 산출물: backend/requirements.txt, backend/app.py, backend/config.py

- [ ] (High) 프론트엔드 프로젝트 초기 설정 - Vite, React 설치 및 기본 구조 생성
  - 의존성: 프로젝트 기본 구조 설정 완료
  - 완료 기준: frontend/src/main.tsx에서 "AI Agent Builder" 제목과 기본 네비게이션 표시
  - 산출물: frontend/src/main.tsx, frontend/src/App.tsx, frontend/src/index.html, frontend/src/styles/style.css

- [ ] (High) 데이터베이스 초기 설정 - SQLite 설정, 기본 테이블 스키마 설계
  - 의존성: 백엔드 프로젝트 초기 설정 완료
  - 완료 기준: users, agents, workflows 테이블 생성 및 연결 테스트 성공
  - 산출물: backend/database.py, backend/models.py, backend/schema.sql

## 우선순위: Medium
- [ ] (Medium) 개발 환경 설정 - Docker 컨테이너 설정, 로컬 개발 서버 구성
  - 의존성: 백엔드/프론트엔드 초기 설정 완료
  - 완료 기준: `docker-compose up` 명령어로 전체 서비스 실행 가능
  - 산출물: Dockerfile, docker-compose.yml, README.md

- [ ] (Medium) 환경 변수 및 설정 관리 - 개발/프로덕션 환경 분리, 시크릿 관리
  - 의존성: 백엔드 프로젝트 초기 설정 완료
  - 완료 기준: .env 파일로 API 키, DB 연결 정보 관리 가능
  - 산출물: backend/.env.example, backend/config.py 업데이트

## 우선순위: Low
- [ ] (Low) 기본 문서화 - README.md, 개발 가이드 작성
  - 의존성: 개발 환경 설정 완료
  - 완료 기준: 새로운 개발자가 README 보고 로컬 환경 구축 가능
  - 산출물: README.md, docs/development.md 