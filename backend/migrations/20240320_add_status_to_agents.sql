-- agents 테이블에 status 컬럼 추가
ALTER TABLE agents ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'active';

-- 기존 레코드에 대해 status 값을 'active'로 설정
UPDATE agents SET status = 'active' WHERE status IS NULL; 