from sqlalchemy.orm import Session
from typing import List, Optional
from infra.models.user import UserModel
from core.domain.user import User

class UserRepository:
    """Repository para operações de banco de dados relacionadas a usuários"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[UserModel]:
        """Retorna todos os usuários ordenados por data de criação"""
        return self.db.query(UserModel).order_by(UserModel.criado_em.desc()).all()
    
    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Retorna um usuário por ID"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Retorna um usuário por email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def create(self, user: User) -> UserModel:
        """Cria um novo usuário no banco de dados"""
        db_user = UserModel(
            nome=user.nome,
            email=user.email,
            filme_favorito=user.filme_favorito
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user: User) -> UserModel:
        """Atualiza um usuário no banco de dados"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            raise ValueError("Usuário não encontrado")
        
        # Atualizar campos
        db_user.nome = user.nome
        db_user.email = user.email
        db_user.filme_favorito = user.filme_favorito
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """Remove um usuário do banco de dados"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def email_exists(self, email: str) -> bool:
        """Verifica se um email já existe no banco"""
        return self.db.query(UserModel).filter(UserModel.email == email).first() is not None
    
    def search_by_name(self, name: str) -> List[UserModel]:
        """Busca usuários por nome (case insensitive)"""
        return self.db.query(UserModel).filter(
            UserModel.nome.ilike(f"%{name}%")
        ).all()
    
    def count_users(self) -> int:
        """Retorna o total de usuários cadastrados"""
        return self.db.query(UserModel).count()
