#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Prático de Uso da Integração Utmify + Pushinpay

Este script demonstra como usar a integração na prática,
mostrando diferentes cenários de uso.

Autor: Kyoko Bot
Data: 2024
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any

# Configurações (substitua pelas suas)
BASE_URL = "http://localhost:5000"  # URL do seu servidor de integração
PUSHINPAY_TOKEN = "seu_token_pushinpay"  # Token da Pushinpay

class ExemploIntegracao:
    """Classe com exemplos práticos de uso da integração"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def testar_integracao(self) -> Dict[str, Any]:
        """Testa a integração usando o endpoint de teste"""
        try:
            print("🧪 Testando integração...")
            
            response = requests.post(f"{self.base_url}/webhook/test")
            
            if response.status_code == 200:
                resultado = response.json()
                print("✅ Teste realizado com sucesso!")
                print(f"📊 Status: {resultado.get('status')}")
                print(f"💳 Transaction ID: {resultado.get('conversion_data', {}).get('transaction_id')}")
                print(f"🎯 Utmify Success: {resultado.get('utmify_success')}")
                return resultado
            else:
                print(f"❌ Erro no teste: {response.status_code}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"❌ Erro ao testar: {e}")
            return {'error': str(e)}
    
    def verificar_saude(self) -> Dict[str, Any]:
        """Verifica se o servidor está funcionando"""
        try:
            print("🏥 Verificando saúde do servidor...")
            
            response = requests.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                resultado = response.json()
                print("✅ Servidor funcionando normalmente!")
                print(f"⏰ Timestamp: {resultado.get('timestamp')}")
                print(f"📦 Versão: {resultado.get('version')}")
                return resultado
            else:
                print(f"❌ Servidor com problemas: {response.status_code}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"❌ Erro ao verificar saúde: {e}")
            return {'error': str(e)}
    
    def simular_webhook_pushinpay(self, dados_personalizados: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simula um webhook da Pushinpay com dados personalizados"""
        try:
            print("📡 Simulando webhook da Pushinpay...")
            
            # Dados padrão do webhook
            dados_webhook = {
                "event": "payment.approved",
                "transaction_id": f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "amount": 149.90,
                "status": "approved",
                "customer_email": "cliente@exemplo.com",
                "customer_id": "cust_123456",
                "custom_data": {
                    "utm_source": "instagram",
                    "utm_medium": "stories",
                    "utm_campaign": "lancamento_produto",
                    "utm_content": "video_promocional",
                    "utm_term": "produto_digital"
                }
            }
            
            # Aplicar dados personalizados se fornecidos
            if dados_personalizados:
                dados_webhook.update(dados_personalizados)
            
            print(f"💰 Valor: R$ {dados_webhook['amount']}")
            print(f"📧 Cliente: {dados_webhook['customer_email']}")
            print(f"🎯 UTM Source: {dados_webhook['custom_data']['utm_source']}")
            print(f"📱 UTM Medium: {dados_webhook['custom_data']['utm_medium']}")
            
            response = requests.post(
                f"{self.base_url}/webhook/pushinpay",
                json=dados_webhook,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                resultado = response.json()
                print("✅ Webhook processado com sucesso!")
                print(f"📊 Status: {resultado.get('status')}")
                print(f"💳 Transaction ID: {resultado.get('transaction_id')}")
                return resultado
            else:
                print(f"❌ Erro ao processar webhook: {response.status_code}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"❌ Erro ao simular webhook: {e}")
            return {'error': str(e)}

def exemplo_campanha_facebook():
    """Exemplo de campanha do Facebook"""
    print("\n🔵 === EXEMPLO: CAMPANHA FACEBOOK ===")
    
    integracao = ExemploIntegracao(BASE_URL)
    
    dados_facebook = {
        "amount": 97.00,
        "customer_email": "cliente.facebook@exemplo.com",
        "custom_data": {
            "utm_source": "facebook",
            "utm_medium": "cpc",
            "utm_campaign": "black_friday_2024",
            "utm_content": "carousel_produtos",
            "utm_term": "desconto_50"
        }
    }
    
    resultado = integracao.simular_webhook_pushinpay(dados_facebook)
    return resultado

def exemplo_campanha_google():
    """Exemplo de campanha do Google Ads"""
    print("\n🔴 === EXEMPLO: CAMPANHA GOOGLE ADS ===")
    
    integracao = ExemploIntegracao(BASE_URL)
    
    dados_google = {
        "amount": 199.90,
        "customer_email": "cliente.google@exemplo.com",
        "custom_data": {
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "curso_online_2024",
            "utm_content": "anuncio_texto",
            "utm_term": "curso+marketing+digital"
        }
    }
    
    resultado = integracao.simular_webhook_pushinpay(dados_google)
    return resultado

def exemplo_campanha_email():
    """Exemplo de campanha de email marketing"""
    print("\n📧 === EXEMPLO: CAMPANHA EMAIL MARKETING ===")
    
    integracao = ExemploIntegracao(BASE_URL)
    
    dados_email = {
        "amount": 67.50,
        "customer_email": "cliente.email@exemplo.com",
        "custom_data": {
            "utm_source": "newsletter",
            "utm_medium": "email",
            "utm_campaign": "promocao_semanal",
            "utm_content": "botao_cta_principal",
            "utm_term": "oferta_limitada"
        }
    }
    
    resultado = integracao.simular_webhook_pushinpay(dados_email)
    return resultado

def exemplo_campanha_influencer():
    """Exemplo de campanha com influenciador"""
    print("\n🌟 === EXEMPLO: CAMPANHA INFLUENCIADOR ===")
    
    integracao = ExemploIntegracao(BASE_URL)
    
    dados_influencer = {
        "amount": 299.00,
        "customer_email": "cliente.influencer@exemplo.com",
        "custom_data": {
            "utm_source": "instagram",
            "utm_medium": "influencer",
            "utm_campaign": "parceria_joao_silva",
            "utm_content": "stories_swipe_up",
            "utm_term": "desconto_joao20"
        }
    }
    
    resultado = integracao.simular_webhook_pushinpay(dados_influencer)
    return resultado

def gerar_relatorio_testes(resultados: list):
    """Gera um relatório dos testes realizados"""
    print("\n📊 === RELATÓRIO DOS TESTES ===")
    print(f"📈 Total de testes: {len(resultados)}")
    
    sucessos = sum(1 for r in resultados if r.get('status') == 'success')
    erros = len(resultados) - sucessos
    
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📊 Taxa de sucesso: {(sucessos/len(resultados)*100):.1f}%")
    
    if erros > 0:
        print("\n🔍 Erros encontrados:")
        for i, resultado in enumerate(resultados):
            if resultado.get('status') != 'success':
                print(f"   {i+1}. {resultado.get('error', 'Erro desconhecido')}")

def main():
    """Função principal com exemplos de uso"""
    print("🚀 === EXEMPLOS DE USO DA INTEGRAÇÃO UTMIFY + PUSHINPAY ===")
    print(f"🌐 Servidor: {BASE_URL}")
    print("\n⚠️  Certifique-se de que o servidor está rodando antes de executar os testes!")
    
    integracao = ExemploIntegracao(BASE_URL)
    resultados = []
    
    # Verificar saúde do servidor
    print("\n" + "="*50)
    saude = integracao.verificar_saude()
    if 'error' in saude:
        print("❌ Servidor não está funcionando. Verifique se está rodando.")
        return
    
    # Teste básico da integração
    print("\n" + "="*50)
    teste_basico = integracao.testar_integracao()
    resultados.append(teste_basico)
    
    # Exemplos de diferentes campanhas
    print("\n" + "="*50)
    resultados.append(exemplo_campanha_facebook())
    
    print("\n" + "="*50)
    resultados.append(exemplo_campanha_google())
    
    print("\n" + "="*50)
    resultados.append(exemplo_campanha_email())
    
    print("\n" + "="*50)
    resultados.append(exemplo_campanha_influencer())
    
    # Gerar relatório
    print("\n" + "="*50)
    gerar_relatorio_testes(resultados)
    
    print("\n🎉 Testes concluídos!")
    print("\n💡 Próximos passos:")
    print("   1. Configure suas credenciais reais no .env")
    print("   2. Teste com dados reais da Pushinpay")
    print("   3. Configure o webhook no painel da Pushinpay")
    print("   4. Monitore os logs para verificar o funcionamento")
    print("   5. Analise os dados no painel da Utmify")

if __name__ == "__main__":
    main()