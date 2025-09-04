from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from infra.database import get_db
from core.services.user_service import UserService
from api.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=List[UserListResponse])
def get_users(db: Session = Depends(get_db)):
    """Retorna todos os usuários"""
    service = UserService(db)
    users = service.get_all_users()
    return [UserListResponse.from_orm(user) for user in users]

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário"""
    service = UserService(db)
    created_user = service.create_user(
        nome=user.nome,
        email=user.email,
        filme_favorito=user.filme_favorito
    )
    return UserResponse.from_orm(created_user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retorna um usuário específico"""
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Atualiza um usuário"""
    service = UserService(db)
    updated_user = service.update_user(
        user_id=user_id,
        nome=user.nome,
        email=user.email,
        filme_favorito=user.filme_favorito
    )
    return UserResponse.from_orm(updated_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Remove um usuário"""
    service = UserService(db)
    service.delete_user(user_id)
    return None
