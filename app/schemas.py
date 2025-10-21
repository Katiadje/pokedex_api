# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

class PokemonCreate(BaseModel):
    name: str = Field(..., examples=["Charmander"])
    type_primary: str = Field(..., examples=["fire"])
    type_secondary: Optional[str] = Field(None, examples=["flying"])

class PokemonOut(BaseModel):
    id: int
    name: str
    type_primary: str
    type_secondary: Optional[str]
    weakness_due_to_weather: bool
    weather_summary: Optional[str] = None

    class Config:
        from_attributes = True
