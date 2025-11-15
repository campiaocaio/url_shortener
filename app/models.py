from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(30), unique=True, nullable=False, index=True)
    target_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    hits = Column(Integer, server_default="0")

