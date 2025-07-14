"""
기본 모델 클래스
"""
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UUIDType(TypeDecorator):
    """UUID 타입을 SQLite와 PostgreSQL에서 모두 사용할 수 있도록 하는 커스텀 타입"""
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            return uuid.UUID(value) 