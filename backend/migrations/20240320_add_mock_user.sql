-- mock 사용자 추가
INSERT INTO auth.users (
    id,
    email,
    raw_user_meta_data,
    created_at,
    updated_at,
    role,
    email_confirmed_at,
    is_anonymous,
    is_sso_user
)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'mock.user@example.com',
    '{"full_name": "Mock User"}',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    'authenticated',
    CURRENT_TIMESTAMP,
    false,
    false
) ON CONFLICT (id) DO NOTHING; 