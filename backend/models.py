from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(
        Integer, ForeignKey("users.id"),
        primary_key=True, index=True, unique=True
        )
    key = Column(String, unique=True, nullable=True)


class APIUsage(Base):
    __tablename__ = "api_usage"
    id = Column(
        Integer, ForeignKey("users.id"),
        primary_key=True, index=True, unique=True
        )
    usage = Column(Integer, default=0, nullable=False)


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, default=func.now(), nullable=False)
