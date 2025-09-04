from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """Entidade de domínio pura - sem dependências externas"""
    id: Optional[int]
    nome: str
    email: str
    filme_favorito: Optional[str]
    criado_em: Optional[datetime]
    
    def __post_init__(self):
        """Validações de domínio"""
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome não pode estar vazio")
        
        if len(self.nome) > 100:
            raise ValueError("Nome não pode ter mais de 100 caracteres")
        
        if not self.email or '@' not in self.email:
            raise ValueError("Email deve ser válido")
    
    def update_nome(self, novo_nome: str) -> None:
        """Atualiza o nome do usuário"""
        if not novo_nome or len(novo_nome.strip()) == 0:
            raise ValueError("Nome não pode estar vazio")
        
        if len(novo_nome) > 100:
            raise ValueError("Nome não pode ter mais de 100 caracteres")
        
        self.nome = novo_nome.strip()
    
    def update_email(self, novo_email: str) -> None:
        """Atualiza o email do usuário"""
        if not novo_email or '@' not in novo_email:
            raise ValueError("Email deve ser válido")
        
        self.email = novo_email.lower().strip()
    
    def update_filme_favorito(self, novo_filme: Optional[str]) -> None:
        """Atualiza o filme favorito do usuário"""
        if novo_filme and len(novo_filme) > 200:
            raise ValueError("Filme favorito não pode ter mais de 200 caracteres")
        
        self.filme_favorito = novo_filme.strip() if novo_filme else None
