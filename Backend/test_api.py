#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que ela está rodando.")
        return False

def test_create_user():
    """Testa a criação de um usuário"""
    print("\n👤 Testando criação de usuário...")
    
    user_data = {
        "nome": "João Silva",
        "email": "joao@email.com",
        "filme_favorito": "Matrix"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            user = response.json()
            print(f"✅ Usuário criado com sucesso! ID: {user['id']}")
            return user['id']
        else:
            print(f"❌ Erro ao criar usuário: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_get_users():
    """Testa a listagem de usuários"""
    print("\n📋 Testando listagem de usuários...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Listagem OK! {len(users)} usuário(s) encontrado(s)")
            for user in users:
                print(f"  - {user['nome']} ({user['email']})")
            return True
        else:
            print(f"❌ Erro ao listar usuários: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_get_user(user_id):
    """Testa a busca de um usuário específico"""
    print(f"\n🔍 Testando busca do usuário {user_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}")
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuário encontrado: {user['nome']}")
            return True
        else:
            print(f"❌ Erro ao buscar usuário: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_update_user(user_id):
    """Testa a atualização de um usuário"""
    print(f"\n✏️ Testando atualização do usuário {user_id}...")
    
    update_data = {
        "nome": "João Silva Atualizado",
        "filme_favorito": "Matrix Reloaded"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/users/{user_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuário atualizado: {user['nome']}")
            return True
        else:
            print(f"❌ Erro ao atualizar usuário: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_delete_user(user_id):
    """Testa a remoção de um usuário"""
    print(f"\n🗑️ Testando remoção do usuário {user_id}...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        
        if response.status_code == 204:
            print("✅ Usuário removido com sucesso!")
            return True
        else:
            print(f"❌ Erro ao remover usuário: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Bookshelf...")
    print("=" * 50)
    
    # Teste 1: Health check
    if not test_health_check():
        print("\n❌ API não está funcionando. Execute 'python main.py' primeiro.")
        return
    
    # Teste 2: Criar usuário
    user_id = test_create_user()
    if not user_id:
        print("\n❌ Falha ao criar usuário. Verifique os logs da API.")
        return
    
    # Teste 3: Listar usuários
    test_get_users()
    
    # Teste 4: Buscar usuário específico
    test_get_user(user_id)
    
    # Teste 5: Atualizar usuário
    test_update_user(user_id)
    
    # Teste 6: Remover usuário
    test_delete_user(user_id)
    
    print("\n" + "=" * 50)
    print("🎉 Todos os testes concluídos!")

if __name__ == "__main__":
    main()
