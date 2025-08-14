#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a criação de PIX através do bot
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from bot_leticia_menu import LeticiaKyokoBot
from config import PRICES

def test_pix_creation():
    """Testa a criação de PIX através da classe do bot"""
    
    print("🧪 TESTE DE CRIAÇÃO DE PIX ATRAVÉS DO BOT")
    print("=" * 50)
    
    # Criar instância do bot
    bot = LeticiaKyokoBot()
    
    # Testar diferentes packs
    packs_to_test = [
        ('pack_basico', PRICES['pack_basico']),
        ('pack_medio', PRICES['pack_medio']),
        ('pack_completo', PRICES['pack_completo'])
    ]
    
    for pack_type, price in packs_to_test:
        print(f"\n🎯 Testando {pack_type} - R$ {price:.2f}")
        print("-" * 30)
        
        try:
            # Testar criação de PIX
            result = bot.create_pix_payment(price, pack_type)
            
            if result.get('sucesso'):
                print(f"✅ PIX criado com sucesso!")
                print(f"🆔 ID: {result.get('id')}")
                print(f"💰 Valor: R$ {result.get('valor'):.2f}")
                print(f"📱 Status: {result.get('status')}")
                print(f"🔗 QR Code: {result.get('qr_code', 'N/A')[:50]}...")
                
                if result.get('qr_code_base64'):
                    print(f"🖼️ QR Code Base64: Presente")
                    
            else:
                print(f"❌ Falha ao criar PIX")
                print(f"🔍 Erro: {result.get('erro', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"💥 Exceção: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")

if __name__ == "__main__":
    test_pix_creation()