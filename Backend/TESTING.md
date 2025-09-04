# 🧪 Como Testar a API Bookshelf

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **pip** para instalar dependências

## 🚀 Passo a Passo

### 1. **Instalar Dependências**
```bash
cd Backend
pip install -r requirements.txt
```

### 2. **Executar a API**
```bash
python main.py
```

Você verá algo como:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. **Testar com Script Automático**
Em outro terminal:
```bash
python test_api.py
```

### 4. **Testar Manualmente**

#### **Health Check**
```bash
curl http://localhost:8000/health
```

#### **Criar Usuário**
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "filme_favorito": "Matrix"
  }'
```

#### **Listar Usuários**
```bash
curl http://localhost:8000/api/users
```

#### **Buscar Usuário Específico**
```bash
curl http://localhost:8000/api/users/1
```

#### **Atualizar Usuário**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Atualizado",
    "filme_favorito": "Matrix Reloaded"
  }'
```

#### **Remover Usuário**
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

## 🌐 Interface Web

### **Swagger UI (Documentação Interativa)**
Acesse: http://localhost:8000/docs

### **ReDoc (Documentação Alternativa)**
Acesse: http://localhost:8000/redoc

## 🔍 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Verificar se a API está funcionando |
| GET | `/api/users` | Listar todos os usuários |
| POST | `/api/users` | Criar novo usuário |
| GET | `/api/users/{id}` | Buscar usuário específico |
| PUT | `/api/users/{id}` | Atualizar usuário |
| DELETE | `/api/users/{id}` | Remover usuário |

## 📝 Exemplo de Resposta

### **Criar Usuário (POST /api/users)**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "filme_favorito": "Matrix",
  "criado_em": "2023-12-01T10:00:00"
}
```

### **Listar Usuários (GET /api/users)**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "filme_favorito": "Matrix",
    "criado_em": "2023-12-01T10:00:00"
  }
]
```

## 🐛 Solução de Problemas

### **Erro: ModuleNotFoundError**
```bash
# Instale as dependências
pip install -r requirements.txt
```

### **Erro: Port already in use**
```bash
# Mude a porta no main.py ou mate o processo
lsof -ti:8000 | xargs kill -9
```

### **Erro: Database connection**
```bash
# Verifique se o diretório database/ existe
mkdir -p database
```

## 🎯 Validações Testadas

- ✅ Nome obrigatório
- ✅ Email válido e único
- ✅ Filme favorito opcional
- ✅ ID automático
- ✅ Data de criação automática
- ✅ Atualização parcial
- ✅ Remoção com confirmação
