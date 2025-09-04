# Bookshelf Backend - Arquitetura Limpa

Backend da aplicação Bookshelf desenvolvido com FastAPI, SQLAlchemy ORM e arquitetura em camadas.

## 🏗️ Arquitetura

```
Backend/
├── database/
│   ├── schema.sql        # Schemas SQL
├── main.py               # Aplicação FastAPI principal
├── requirements.txt      # Dependências
└── README.md             # Documentação
```

## 📋 Camadas da Arquitetura

### 1. **Controllers** (Apresentação)
- Recebem requisições HTTP
- Validam entrada com Pydantic
- Chamam services
- Retornam respostas HTTP

### 2. **Services** (Lógica de Negócio)
- Contêm regras de negócio
- Validações complexas
- Orquestram operações
- Chamam repositories

### 3. **Repositories** (Acesso a Dados)
- Operações CRUD
- Queries complexas
- Abstração do banco de dados
- Retornam modelos SQLAlchemy

### 4. **Models**
- **SQLAlchemy**: Estrutura do banco de dados
- **Pydantic**: Validação de entrada/saída da API

## 🔄 Fluxo de Dados

```
HTTP Request → Controller → Service → Repository → Database
                ↓
HTTP Response ← Controller ← Service ← Repository ← Database
```

## 📦 Separação de Responsabilidades

### Controllers
```python
@router.post("/", response_model=LivroSchema)
def create_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    service = LivroService(db)
    return service.create_livro(livro)
```

### Services
```python
def create_livro(self, livro_data: LivroCreate) -> LivroSchema:
    try:
        livro = self.repository.create(livro_data)
        return livro
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Repositories
```python
def create(self, livro_data: LivroCreate) -> Livro:
    db_livro = Livro(
        nome=livro_data.nome,
        descricao=livro_data.descricao,
        # ...
    )
    self.db.add(db_livro)
    self.db.commit()
    self.db.refresh(db_livro)
    return db_livro
```

## 🎯 Vantagens desta Arquitetura

1. **Separação de Responsabilidades**: Cada camada tem uma função específica
2. **Testabilidade**: Fácil de testar cada camada isoladamente
3. **Manutenibilidade**: Mudanças em uma camada não afetam outras
4. **Escalabilidade**: Fácil adicionar novas funcionalidades
5. **Reutilização**: Services e repositories podem ser reutilizados
6. **Clareza**: Código mais organizado e fácil de entender

## 🚀 Como Adicionar Nova Funcionalidade

1. **Criar Model SQLAlchemy** (se necessário)
2. **Criar Model Pydantic** (se necessário)
3. **Criar Repository** (operações de banco)
4. **Criar Service** (lógica de negócio)
5. **Criar Controller** (endpoints da API)
6. **Incluir no main.py**

## 📝 Exemplo: Adicionar Usuários

```python
# 1. Repository
class UsuarioRepository:
    def create(self, usuario_data: UsuarioCreate) -> Usuario:
        # lógica de criação

# 2. Service  
class UsuarioService:
    def create_usuario(self, usuario_data: UsuarioCreate) -> UsuarioSchema:
        # validações e lógica de negócio

# 3. Controller
@router.post("/", response_model=UsuarioSchema)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.create_usuario(usuario)
```

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
