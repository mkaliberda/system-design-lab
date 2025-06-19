from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..core.db import Base


# This Python class defines the schema for the "urls" table.
class URL(Base):
    """
    Model representing a shortened URL.
    key is protected by unique index to ensure no duplicates.
    """

    __tablename__ = "urls"

    # Columns for our table:
    id = Column(Integer, primary_key=True)
    url = Column(String, index=True, nullable=False)
    alias = Column(String, max_length=10, unique=True, index=True, nullable=False)
    expires = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
