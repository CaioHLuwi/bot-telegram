#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificação do Bot Kyoko
Verifica se há instâncias não autorizadas ou problemas de segurança
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

def verificar_webhook():
    """Verifica se há webhook configurado"""
    print("🔍 Verificando configuração de webhook...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['ok']:
            webhook_info = data['result']
            if webhook_info['url']:
                print(f"⚠️  WEBHOOK ATIVO: {webhook_info['url']}")
                print(f"   Certificado customizado: {webhook_info['has_custom_certificate']}")
                print(f"   Updates pendentes: {webhook_info['pending_update_count']}")
                return True
            else:
                print("✅ Nenhum webhook configurado")
                return False
        else:
            print(f"❌ Erro ao verificar webhook: {data}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def verificar_bot_info():
    """Verifica informações básicas do bot"""
    print("\n🤖 Verificando informações do bot...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['ok']:
            bot_info = data['result']
            print(f"✅ Bot ativo: @{bot_info['username']}")
            print(f"   Nome: {bot_info['first_name']}")
            print(f"   ID: {bot_info['id']}")
            print(f"   Pode receber mensagens: {bot_info.get('can_read_all_group_messages', 'N/A')}")
            return bot_info
        else:
            print(f"❌ Erro ao obter info do bot: {data}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def verificar_updates_recentes():
    """Verifica updates recentes do bot"""
    print("\n📨 Verificando updates recentes...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['ok']:
            updates = data['result']
            if updates:
                print(f"⚠️  {len(updates)} updates pendentes encontrados")
                for update in updates[-3:]:  # Mostrar apenas os 3 mais recentes
                    update_id = update['update_id']
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg['chat']['id']
                        text = msg.get('text', '[Sem texto]')[:50]
                        print(f"   Update {update_id}: Chat {chat_id} - {text}...")
            else:
                print("✅ Nenhum update pendente")
            return updates
        else:
            print(f"❌ Erro ao obter updates: {data}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def enviar_mensagem_teste():
    """Envia uma mensagem de teste para verificar se o bot está funcionando"""
    print("\n🧪 Enviando mensagem de teste...")
    
    if not GROUP_CHAT_ID:
        print("❌ GROUP_CHAT_ID não configurado")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': GROUP_CHAT_ID,
        'text': f"🔍 Teste de verificação do bot - {datetime.now().strftime('%H:%M:%S')}"
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['ok']:
            print("✅ Mensagem de teste enviada com sucesso")
            return True
        else:
            print(f"❌ Erro ao enviar mensagem: {result}")
            return False
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def verificar_permissoes_grupo():
    """Verifica permissões do bot no grupo"""
    print("\n👥 Verificando permissões no grupo...")
    
    if not GROUP_CHAT_ID:
        print("❌ GROUP_CHAT_ID não configurado")
        return None
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    
    # Primeiro, obter info do bot
    bot_info = verificar_bot_info()
    if not bot_info:
        return None
    
    data = {
        'chat_id': GROUP_CHAT_ID,
        'user_id': bot_info['id']
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['ok']:
            member_info = result['result']
            status = member_info['status']
            print(f"✅ Status no grupo: {status}")
            
            if 'can_send_messages' in member_info:
                print(f"   Pode enviar mensagens: {member_info['can_send_messages']}")
            
            return member_info
        else:
            print(f"❌ Erro ao verificar permissões: {result}")
            return None
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def main():
    """Função principal de verificação"""
    print("🔍 VERIFICAÇÃO DE SEGURANÇA DO BOT KYOKO")
    print("=" * 50)
    
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN não encontrado no arquivo .env")
        return
    
    print(f"🔑 Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
    print(f"👥 Grupo: {GROUP_CHAT_ID}")
    
    # Executar verificações
    webhook_ativo = verificar_webhook()
    bot_info = verificar_bot_info()
    updates = verificar_updates_recentes()
    permissoes = verificar_permissoes_grupo()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    if webhook_ativo:
        print("⚠️  ALERTA: Webhook ativo detectado - pode indicar deploy em produção")
    
    if updates:
        print(f"⚠️  ALERTA: {len(updates)} updates pendentes - pode indicar conflito de instâncias")
    
    if bot_info:
        print(f"✅ Bot funcionando: @{bot_info['username']}")
    
    # Teste final
    print("\n🧪 Executando teste de envio...")
    teste_ok = enviar_mensagem_teste()
    
    if teste_ok:
        print("\n✅ VERIFICAÇÃO CONCLUÍDA: Bot funcionando normalmente")
        print("💡 Se ainda há mensagens de Ethereum, elas podem estar vindo de:")
        print("   - Deploy em produção (Railway/Heroku)")
        print("   - Token comprometido")
        print("   - Outro bot no mesmo grupo")
    else:
        print("\n❌ PROBLEMA DETECTADO: Bot não conseguiu enviar mensagem")

if __name__ == "__main__":
    main()