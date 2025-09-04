from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings
import os
from pathlib import Path

# Criar diretório do banco se não existir
def ensure_database_directory():
    """Garante que o diretório do banco de dados existe"""
    db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
    db_dir = db_path.parent
    db_dir.mkdir(parents=True, exist_ok=True)

# Criar engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Criar todas as tabelas"""
    ensure_database_directory()
    from infra.models.user import Base
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Remover todas as tabelas"""
    ensure_database_directory()
    from infra.models.user import Base
    Base.metadata.drop_all(bind=engine)
