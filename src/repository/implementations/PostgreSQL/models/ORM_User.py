from datetime import datetime ,timezone
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    email = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)