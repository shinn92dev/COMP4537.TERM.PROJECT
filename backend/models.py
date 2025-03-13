import enum
from database import Base
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, DateTime, Boolean, Enum)
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)


class APIKey(Base):
    __tablename__ = "api_keys"

    key_id = Column(Integer, index=True, unique=True, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id"),
        index=True, nullable=False
        )
    key = Column(String, unique=True, nullable=False)


class HTTPMethodEnum(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class APIUsage(Base):
    __tablename__ = "api_usage"

    usage_id = Column(Integer, primary_key=True, index=True, unique=True)
    key_id = Column(
        Integer, ForeignKey("api_keys.key_id"),
        nullable=False, index=True)
    count = Column(Integer, default=0, nullable=False)
    method = Column(Enum(HTTPMethodEnum), nullable=False)


class Token(Base):
    __tablename__ = "tokens"

    user_id = Column(
        Integer, ForeignKey("users.user_id"),
        primary_key=True, nullable=False, unique=True
        )
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, default=func.now(), nullable=False)
