# app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type_primary = Column(String, nullable=False)  # ex: "fire", "water", ...
    type_secondary = Column(String, nullable=True)  # optionnel
