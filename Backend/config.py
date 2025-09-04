from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./infra/database/bookshelf.db"  # Mudou para data/
    
    # Configurações da API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Bookshelf API"
    VERSION: str = "1.0.0"
    
    # Configurações de CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Configurações de segurança
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()
