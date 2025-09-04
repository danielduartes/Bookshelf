from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.domain.user import User
from infra.repositories.user_repository import UserRepository

class UserService:
    """Service de usuário - orquestra casos de uso e regras de negócio"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_all_users(self) -> List[User]:
        """Retorna todos os usuários"""
        try:
            return self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar usuários: {str(e)}"
            )
    
    def get_user_by_id(self, user_id: int) -> User:
        """Retorna um usuário específico"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    
    def create_user(self, nome: str, email: str, filme_favorito: str = None) -> User:
        """Cria um novo usuário"""
        try:
            # Verificar se email já existe
            if self.repository.email_exists(email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já está em uso"
                )
            
            # Criar entidade de domínio
            domain_user = User(
                id=None,
                nome=nome,
                email=email,
                filme_favorito=filme_favorito,
                criado_em=None
            )
            
            # Salvar no banco
            return self.repository.create(domain_user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar usuário: {str(e)}"
            )
    
    def update_user(self, user_id: int, nome: str = None, email: str = None, filme_favorito: str = None) -> User:
        """Atualiza um usuário"""
        # Buscar usuário existente
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        try:
            # Criar entidade de domínio com dados existentes
            domain_user = User(
                id=db_user.id,
                nome=db_user.nome,
                email=db_user.email,
                filme_favorito=db_user.filme_favorito,
                criado_em=db_user.criado_em
            )
            
            # Aplicar atualizações
            if nome is not None:
                domain_user.update_nome(nome)
            
            if email is not None:
                # Verificar se novo email já existe (se diferente do atual)
                if email != db_user.email and self.repository.email_exists(email):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email já está em uso"
                    )
                domain_user.update_email(email)
            
            if filme_favorito is not None:
                domain_user.update_filme_favorito(filme_favorito)
            
            # Atualizar no banco
            return self.repository.update(user_id, domain_user)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar usuário: {str(e)}"
            )
    
    def delete_user(self, user_id: int) -> None:
        """Remove um usuário"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        try:
            self.repository.delete(user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao remover usuário: {str(e)}"
            )
