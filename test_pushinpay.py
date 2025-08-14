#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
from dotenv import load_dotenv
import json

# Carregar variáveis de ambiente
load_dotenv()

def test_pushinpay_api():
    """Testa a conectividade com a API da Pushinpay"""
    
    # Buscar token nas diferentes variáveis de ambiente
    token = os.getenv('PUSHIN_PAY_TOKEN') or os.getenv('PUSHINPAY_TOKEN')
    
    if not token:
        print("❌ Token da Pushinpay não encontrado nas variáveis de ambiente")
        print("Verifique se PUSHIN_PAY_TOKEN ou PUSHINPAY_TOKEN estão configurados")
        return False
    
    print(f"🔑 Token encontrado: {token[:20]}...")
    
    # Configurar headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Testar diferentes endpoints
    base_url = 'https://api.pushinpay.com.br/api'
    endpoints_to_test = [
        ('/user', 'GET', 'Informações do usuário'),
        ('/pix', 'GET', 'Listar PIX'),
        ('/payments', 'GET', 'Listar pagamentos')
    ]
    
    print("\n🧪 Testando endpoints da Pushinpay:")
    print("-" * 50)
    
    for endpoint, method, description in endpoints_to_test:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n📡 Testando: {method} {endpoint} ({description})")
            
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Sucesso")
                # Mostrar parte da resposta
                try:
                    data = response.json()
                    if isinstance(data, dict) and len(str(data)) > 100:
                        print(f"   📄 Resposta: {str(data)[:100]}...")
                    else:
                        print(f"   📄 Resposta: {data}")
                except:
                    print(f"   📄 Resposta: {response.text[:100]}...")
            elif response.status_code == 401:
                print("   ❌ Erro 401: Token inválido ou expirado")
                print(f"   📄 Resposta: {response.text}")
                return False
            elif response.status_code == 404:
                print("   ⚠️  Endpoint não encontrado (normal para alguns endpoints)")
            else:
                print(f"   ⚠️  Status inesperado: {response.status_code}")
                print(f"   📄 Resposta: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout ao conectar com {endpoint}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Erro de conexão com {endpoint}")
        except Exception as e:
            print(f"   ❌ Erro inesperado: {str(e)[:100]}")
    
    print("\n" + "="*50)
    print("🔍 Teste de criação de PIX:")
    
    # Testar criação de PIX
    try:
        pix_data = {
            "amount": 19.90,
            "description": "Teste de PIX - Bot Kyoko",
            "customer": {
                "name": "Teste Cliente",
                "email": "teste@exemplo.com"
            }
        }
        
        response = requests.post(
            f"{base_url}/pix",
            headers=headers,
            json=pix_data,
            timeout=15
        )
        
        print(f"Status da criação de PIX: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ PIX criado com sucesso!")
            try:
                pix_response = response.json()
                print(f"📄 ID do PIX: {pix_response.get('id', 'N/A')}")
                print(f"📄 Status: {pix_response.get('status', 'N/A')}")
            except:
                print(f"📄 Resposta: {response.text[:200]}")
        else:
            print(f"❌ Erro ao criar PIX: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar criação de PIX: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("🚀 Teste da API Pushinpay")
    print("=" * 30)
    test_pushinpay_api()
    print("\n✅ Teste concluído!")