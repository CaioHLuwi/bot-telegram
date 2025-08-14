#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o endpoint correto da API Pushinpay: /api/pix/cashIn
"""

import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_pushinpay_cashin():
    """Testa o endpoint correto /api/pix/cashIn da Pushinpay"""
    
    # Buscar token de diferentes fontes
    token = (
        os.getenv('PUSHIN_PAY_TOKEN') or 
        os.getenv('PUSHINPAY_TOKEN') or
        '42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1'  # Token do config.py
    )
    
    if not token:
        print("❌ Token não encontrado!")
        return
    
    print(f"🔑 Token encontrado: {token[:20]}...")
    
    # URL correta da API
    base_url = "https://api.pushinpay.com.br/api"
    endpoint = f"{base_url}/pix/cashIn"
    
    # Headers corretos
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Payload de teste (valor mínimo: 50 centavos)
    payload = {
        'value': 100,  # R$ 1,00 em centavos
        'webhook_url': 'https://exemplo.com/webhook'  # Opcional
    }
    
    print(f"\n🚀 Testando endpoint: {endpoint}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📋 Headers de Resposta: {dict(response.headers)}")
        
        if response.status_code in [200, 201]:
            pix_data = response.json()
            print(f"\n✅ PIX criado com sucesso!")
            print(f"🆔 ID: {pix_data.get('id')}")
            print(f"💰 Valor: {pix_data.get('value')} centavos")
            print(f"📱 Status: {pix_data.get('status')}")
            print(f"🔗 QR Code: {pix_data.get('qr_code', 'N/A')[:50]}...")
            
            if 'qr_code_base64' in pix_data:
                print(f"🖼️ QR Code Base64: Presente ({len(pix_data['qr_code_base64'])} caracteres)")
            
        else:
            print(f"\n❌ Erro na API:")
            print(f"📄 Resposta: {response.text}")
            
            # Tentar parsear JSON de erro
            try:
                error_data = response.json()
                print(f"🔍 Detalhes do erro: {json.dumps(error_data, indent=2)}")
            except:
                pass
                
    except requests.exceptions.Timeout:
        print("\n⏰ Timeout na requisição")
    except requests.exceptions.ConnectionError:
        print("\n🌐 Erro de conexão")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")

def test_user_endpoint():
    """Testa o endpoint /user para verificar autenticação"""
    
    token = (
        os.getenv('PUSHIN_PAY_TOKEN') or 
        os.getenv('PUSHINPAY_TOKEN') or
        '42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1'
    )
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    endpoint = "https://api.pushinpay.com.br/api/user"
    
    print(f"\n🔐 Testando autenticação: {endpoint}")
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Autenticação válida!")
            print(f"👤 Usuário: {user_data.get('name', 'N/A')}")
            print(f"📧 Email: {user_data.get('email', 'N/A')}")
        else:
            print(f"❌ Falha na autenticação: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except Exception as e:
        print(f"💥 Erro: {e}")

if __name__ == "__main__":
    print("🧪 TESTE DA API PUSHINPAY - ENDPOINT CORRETO")
    print("=" * 50)
    
    # Primeiro testar autenticação
    test_user_endpoint()
    
    print("\n" + "=" * 50)
    
    # Depois testar criação de PIX
    test_pushinpay_cashin()
    
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")