from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base schema
class UserBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    filme_favorito: Optional[str] = Field(None, max_length=200)

# Request schemas
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    filme_favorito: Optional[str] = Field(None, max_length=200)

# Response schemas
class UserResponse(UserBase):
    id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    id: int
    nome: str
    email: str
    filme_favorito: Optional[str]
    criado_em: datetime
    
    class Config:
        from_attributes = True
