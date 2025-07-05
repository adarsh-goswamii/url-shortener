from datetime import datetime

from sqlalchemy import BIGINT, Column, DateTime, VARCHAR, Enum
from sqlalchemy.ext.declarative import declarative_base

from src.configs.enums import URLStatus
from src.configs.constants import DBTables, DBConfig

Base = declarative_base()

class URLModel(Base):
    __tablename__  = DBTables.URLS
    __table_args__ = DBConfig.BASE_ARGS

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    redirect_url     = Column(VARCHAR, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    status = Column(Enum(URLStatus), default=URLStatus.ACTIVE)
    last_interacted_at  = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id  = Column(BIGINT, nullable=True)
    ip = Column(VARCHAR(45), nullable=False)
