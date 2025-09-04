# Bookshelf Backend - Arquitetura Limpa

Backend da aplicação Bookshelf desenvolvido com FastAPI, SQLAlchemy ORM e arquitetura em camadas.

## 🏗️ Estrutura do Projeto

```
Backend/
├── main.py                    # Aplicação FastAPI principal
├── config.py                  # Configurações da aplicação
├── api/                       # Camada de apresentação (HTTP)
│   ├── schemas/               # Modelos Pydantic (validação API)
│   │   ├── __init__.py
│   │   └── user.py
│   └── routes/                # Controllers/Routers FastAPI
│       ├── __init__.py
│       └── user_routes.py
├── core/                      # Camada de domínio e lógica de negócio
│   ├── domain/                # Entidades de domínio puras
│   │   └── user.py
│   └── services/              # Services (casos de uso)
│       └── user_service.py
└── infra/                     # Camada de infraestrutura
    ├── database/              # Configuração do banco
    │   ├── __init__.py
    │   └── database.py
    ├── models/                # Modelos SQLAlchemy (tabelas)
    │   └── user.py
    └── repositories/          # Repositories (acesso a dados)
        └── user_repository.py
```

## 📋 Camadas da Arquitetura

### 1. **API** (Apresentação)
- **schemas/**: Modelos Pydantic para validação de entrada/saída
- **routes/**: Controllers FastAPI que recebem requisições HTTP
- **Responsabilidade**: Comunicação com HTTP

### 2. **Core** (Domínio e Lógica de Negócio)
- **domain/**: Entidades de domínio puras (sem dependências externas)
- **services/**: Orquestram casos de uso e regras de negócio
- **Responsabilidade**: Regras de negócio

### 3. **Infra** (Infraestrutura)
- **database/**: Configuração do banco de dados
- **models/**: Modelos SQLAlchemy (schema do banco)
- **repositories/**: Operações de persistência
- **Responsabilidade**: Comunicação com banco de dados

## 🔄 Fluxo de Dados

```
HTTP Request → Routes → Services → Domain → Repositories → Database
                ↓
HTTP Response ← Routes ← Services ← Domain ← Repositories ← Database
```

## 📦 Separação de Responsabilidades

### API Layer
```python
# routes/user_routes.py
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)
```

### Core Layer
```python
# services/user_service.py
def create_user(self, user_data: UserCreate) -> UserResponse:
    # Regras de negócio
    if self.repository.email_exists(user_data.email):
        raise HTTPException(detail="Email já está em uso")
    
    # Criar entidade de domínio
    domain_user = User(...)
    return self.repository.create(domain_user)
```

### Infra Layer
```python
# repositories/user_repository.py
def create(self, user: User) -> UserModel:
    db_user = UserModel(
        nome=user.nome,
        email=user.email,
        filme_favorito=user.filme_favorito
    )
    self.db.add(db_user)
    self.db.commit()
    return db_user
```

## 🎯 Vantagens desta Arquitetura

1. **Separação Clara**: Cada camada tem responsabilidade específica
2. **Testabilidade**: Fácil testar cada camada isoladamente
3. **Manutenibilidade**: Mudanças isoladas em cada camada
4. **Escalabilidade**: Fácil adicionar novas funcionalidades
5. **Reutilização**: Services e repositories reutilizáveis
6. **Clareza**: Código organizado e fácil de entender

## 🚀 Como Adicionar Nova Funcionalidade

1. **Criar Model SQLAlchemy** (`infra/models/`)
2. **Criar Schema Pydantic** (`api/schemas/`)
3. **Criar Entidade de Domínio** (`core/domain/`)
4. **Criar Repository** (`infra/repositories/`)
5. **Criar Service** (`core/services/`)
6. **Criar Routes** (`api/routes/`)
7. **Incluir no main.py**

## 🔧 Instalação e Execução

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python main.py

# Ou com uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🎯 Endpoints de Usuário

- `GET /api/users` - Listar todos os usuários
- `POST /api/users` - Criar novo usuário
- `GET /api/users/{user_id}` - Buscar usuário específico
- `PUT /api/users/{user_id}` - Atualizar usuário
- `DELETE /api/users/{user_id}` - Remover usuário
