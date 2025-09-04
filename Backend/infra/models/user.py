from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserModel(Base):
    """Modelo SQLAlchemy para a tabela de usuários"""
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    filme_favorito = Column(String(200))
    criado_em = Column(DateTime, default=func.now())
