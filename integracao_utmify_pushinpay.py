#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integração Utmify + Pushinpay para Tracking de Vendas PIX

Este script demonstra como integrar a Utmify com a Pushinpay para
rastrear vendas realizadas via PIX com parâmetros UTM.

Autor: Kyoko Bot
Data: 2024
"""

import os
import json
import hmac
import hashlib
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
import logging
from logger_pix_requests import PixRequestLogger
import time

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa o logger de PIX requests
pix_logger = PixRequestLogger()

app = Flask(__name__)

# Configurações (usar variáveis de ambiente em produção)
class Config:
    PUSHINPAY_TOKEN = os.getenv('PUSHINPAY_TOKEN', 'seu_token_pushinpay')
    UTMIFY_API_KEY = os.getenv('UTMIFY_API_KEY', 'seu_token_utmify')
    UTMIFY_API_URL = os.getenv('UTMIFY_API_URL', 'https://api.utmify.com.br/api-credentials/orders')
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'seu_secret_webhook')
    
config = Config()

class UtmifyIntegration:
    """Classe para gerenciar integração com Utmify"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'x-api-token': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'KyokoBot-Utmify/1.0'
        }
    
    def enviar_conversao(self, dados_conversao: Dict[str, Any]) -> bool:
        """Envia dados de conversão para Utmify seguindo a documentação oficial"""
        try:
            # Payload seguindo a documentação oficial da UTMify brasileira
            payload = {
                'order_id': dados_conversao.get('transaction_id'),
                'total_value': float(dados_conversao.get('value', 0)),
                'currency': 'BRL',
                'status': 'completed',
                'payment_method': 'pix',
                'customer': {
                    'email': dados_conversao.get('customer_email', ''),
                    'name': dados_conversao.get('customer_name', 'Cliente'),
                    'phone': dados_conversao.get('customer_phone', ''),
                    'document': dados_conversao.get('customer_document', '')
                },
                'products': [{
                    'name': 'Pack Digital',
                    'quantity': 1,
                    'price': float(dados_conversao.get('value', 0))
                }],
                'tracking': {
                    'utm_source': dados_conversao.get('utm_source', ''),
                    'utm_medium': dados_conversao.get('utm_medium', ''),
                    'utm_campaign': dados_conversao.get('utm_campaign', ''),
                    'utm_content': dados_conversao.get('utm_content', ''),
                    'utm_term': dados_conversao.get('utm_term', ''),
                    'src': dados_conversao.get('src', ''),
                    'sck': dados_conversao.get('sck', ''),
                    'fbclid': dados_conversao.get('fbclid', ''),
                    'gclid': dados_conversao.get('gclid', '')
                },
                'commission': {
                    'value': 0,
                    'type': 'fixed'
                },
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            # Remover campos vazios
            payload = self._limpar_payload(payload)
            
            logger.info(f"Enviando conversão para Utmify: {payload['order_id']}")
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Conversão enviada com sucesso: {response.status_code}")
                return True
            else:
                logger.error(f"Erro ao enviar conversão: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao enviar para Utmify: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar para Utmify: {e}")
            return False
    
    def _limpar_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Remove campos vazios ou None do payload"""
        def limpar_dict(d):
            if isinstance(d, dict):
                return {k: limpar_dict(v) for k, v in d.items() 
                       if v is not None and v != '' and v != {}}
            return d
        
        return limpar_dict(payload)

class PushinpayWebhook:
    """Classe para gerenciar webhooks da Pushinpay"""
    
    def __init__(self, secret: str):
        self.secret = secret
    
    def validar_assinatura(self, payload: str, signature: str) -> bool:
        """Valida a assinatura do webhook da Pushinpay"""
        try:
            expected_signature = hmac.new(
                self.secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Comparação segura
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Erro ao validar assinatura: {e}")
            return False
    
    def processar_webhook(self, dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa dados do webhook da Pushinpay"""
        try:
            # Verificar se é um pagamento aprovado
            if dados.get('status') not in ['approved', 'completed', 'paid']:
                logger.info(f"Pagamento não aprovado: {dados.get('status')}")
                return None
            
            # Extrair dados relevantes
            conversao_data = {
                'transaction_id': dados.get('transaction_id') or dados.get('id'),
                'value': dados.get('amount') or dados.get('value'),
                'customer_email': dados.get('customer_email') or dados.get('email'),
                'customer_id': dados.get('customer_id'),
                'status': dados.get('status'),
                'payment_method': 'pix'
            }
            
            # Extrair UTMs dos custom_data
            custom_data = dados.get('custom_data', {})
            if isinstance(custom_data, str):
                try:
                    custom_data = json.loads(custom_data)
                except json.JSONDecodeError:
                    custom_data = {}
            
            # Adicionar parâmetros UTM
            conversao_data.update({
                'utm_source': custom_data.get('utm_source'),
                'utm_medium': custom_data.get('utm_medium'),
                'utm_campaign': custom_data.get('utm_campaign'),
                'utm_content': custom_data.get('utm_content'),
                'utm_term': custom_data.get('utm_term')
            })
            
            logger.info(f"Dados de conversão processados: {conversao_data['transaction_id']}")
            return conversao_data
            
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {e}")
            return None

# Instanciar classes
utmify = UtmifyIntegration(config.UTMIFY_API_KEY, config.UTMIFY_API_URL)
pushinpay_webhook = PushinpayWebhook(config.WEBHOOK_SECRET)

@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    """Endpoint para receber webhooks da Pushinpay"""
    try:
        # Obter dados da requisição
        payload = request.get_data(as_text=True)
        signature = request.headers.get('X-Signature') or request.headers.get('Signature')
        
        # Validar assinatura (opcional, dependendo da Pushinpay)
        if signature and not pushinpay_webhook.validar_assinatura(payload, signature):
            logger.warning("Assinatura do webhook inválida")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Processar dados JSON
        dados = request.get_json()
        if not dados:
            logger.error("Dados JSON inválidos no webhook")
            return jsonify({'error': 'Invalid JSON'}), 400
        
        logger.info(f"Webhook recebido: {dados.get('event', 'unknown')}")
        
        # Extrair parâmetros UTM dos dados
        custom_data = dados.get('custom_data', {})
        if isinstance(custom_data, str):
            try:
                custom_data = json.loads(custom_data)
            except json.JSONDecodeError:
                custom_data = {}
        
        utm_params = {
            'utm_source': custom_data.get('utm_source'),
            'utm_medium': custom_data.get('utm_medium'),
            'utm_campaign': custom_data.get('utm_campaign'),
            'utm_content': custom_data.get('utm_content'),
            'utm_term': custom_data.get('utm_term')
        }
        
        # Processar webhook
        conversao_data = pushinpay_webhook.processar_webhook(dados)
        
        if conversao_data:
            # Enviar para Utmify
            sucesso = utmify.enviar_conversao(conversao_data)
            
            # Log do webhook com resultado da UTMify
            pix_logger.log_webhook_received(
                webhook_data=dados,
                payment_id=conversao_data.get('transaction_id'),
                utm_params=utm_params,
                utmify_sent=sucesso,
                utmify_response={'success': sucesso}
            )
            
            if sucesso:
                logger.info(f"Conversão processada com sucesso: {conversao_data['transaction_id']}")
                return jsonify({
                    'status': 'success',
                    'message': 'Conversion tracked successfully',
                    'transaction_id': conversao_data['transaction_id']
                }), 200
            else:
                logger.error(f"Falha ao enviar conversão: {conversao_data['transaction_id']}")
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to track conversion'
                }), 500
        else:
            # Log do webhook mesmo se não for conversão válida
            pix_logger.log_webhook_received(
                webhook_data=dados,
                payment_id=dados.get('transaction_id') or dados.get('id'),
                utm_params=utm_params,
                utmify_sent=False,
                utmify_response={'message': 'Webhook processado, mas não é uma conversão válida'}
            )
            
            logger.info("Webhook processado, mas não é uma conversão válida")
            return jsonify({
                'status': 'ignored',
                'message': 'Webhook processed but not a valid conversion'
            }), 200
            
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        
        # Log do erro no webhook
        try:
            pix_logger.log_webhook_received(
                webhook_data=request.get_json() or {},
                payment_id="unknown",
                utm_params={},
                utmify_sent=False,
                utmify_response={'error': str(e)}
            )
        except:
            pass
        
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/test', methods=['POST'])
def webhook_test():
    """Endpoint para testar a integração"""
    try:
        # Dados de teste
        dados_teste = {
            'event': 'payment.approved',
            'transaction_id': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'amount': 99.90,
            'status': 'approved',
            'customer_email': 'teste@exemplo.com',
            'custom_data': {
                'utm_source': 'facebook',
                'utm_medium': 'cpc',
                'utm_campaign': 'teste_integracao',
                'utm_content': 'anuncio_teste',
                'utm_term': 'produto_digital'
            }
        }
        
        # Processar como se fosse um webhook real
        conversao_data = pushinpay_webhook.processar_webhook(dados_teste)
        
        if conversao_data:
            sucesso = utmify.enviar_conversao(conversao_data)
            
            return jsonify({
                'status': 'success' if sucesso else 'error',
                'test_data': dados_teste,
                'conversion_data': conversao_data,
                'utmify_success': sucesso
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to process test data'
            }), 500
            
    except Exception as e:
        logger.error(f"Erro no teste: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/logs/stats')
def logs_statistics():
    """Endpoint para visualizar estatísticas dos logs"""
    try:
        stats = pix_logger.get_statistics()
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/logs/date/<date_str>')
def logs_by_date(date_str):
    """Endpoint para visualizar logs por data (formato: YYYY-MM-DD)"""
    try:
        logs = pix_logger.get_logs_by_date(date_str)
        return jsonify({
            'success': True,
            'date': date_str,
            'count': len(logs),
            'data': logs,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/logs/status/<status>')
def logs_by_status(status):
    """Endpoint para visualizar logs por status (success, error, pending)"""
    try:
        logs = pix_logger.get_logs_by_status(status)
        return jsonify({
            'success': True,
            'status': status,
            'count': len(logs),
            'data': logs,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Página inicial com informações da API"""
    return jsonify({
        'name': 'Integração Utmify + Pushinpay',
        'version': '1.0.0',
        'endpoints': {
            'webhook_pushinpay': '/webhook/pushinpay',
            'webhook_test': '/webhook/test',
            'health': '/health'
        },
        'description': 'API para integrar tracking de vendas PIX entre Pushinpay e Utmify'
    })

def gerar_pix_com_utm(valor: float, email: str, utm_params: Dict[str, str], user_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Função auxiliar para gerar PIX com parâmetros UTM"""
    start_time = time.time()
    
    try:
        headers = {
            'Authorization': f'Bearer {config.PUSHINPAY_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'amount': valor,
            'customer_email': email,
            'webhook_url': 'https://seu-dominio.com/webhook/pushinpay',
            'custom_data': utm_params
        }
        
        response = requests.post(
            'https://api.pushinpay.com.br/api/pix/cashIn',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        if response.status_code in [200, 201]:
            result = response.json()
            logger.info(f"PIX gerado com sucesso para {email}")
            
            # Log da solicitação PIX
            pix_logger.log_pix_request(
                user_info=user_info or {"email": email},
                pix_data={
                    "valor_reais": valor,
                    "customer_email": email,
                    "payment_id": result.get('payment_id'),
                    "qr_code": result.get('qr_code'),
                    "expires_at": result.get('expires_at')
                },
                utm_params=utm_params,
                pushinpay_response=result,
                status="success",
                processing_time_ms=processing_time_ms
            )
            
            return result
        else:
            logger.error(f"Erro ao gerar PIX: {response.status_code} - {response.text}")
            
            # Log do erro
            pix_logger.log_pix_request(
                user_info=user_info or {"email": email},
                pix_data={
                    "valor_reais": valor,
                    "customer_email": email
                },
                utm_params=utm_params,
                pushinpay_response={"error": response.text, "status_code": response.status_code},
                status="error",
                errors=[f"HTTP {response.status_code}: {response.text}"],
                processing_time_ms=processing_time_ms
            )
            
            return {'error': 'Failed to generate PIX'}
            
    except Exception as e:
        processing_time_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Erro ao gerar PIX: {e}")
        
        # Log da exceção
        pix_logger.log_pix_request(
            user_info=user_info or {"email": email},
            pix_data={
                "valor_reais": valor,
                "customer_email": email
            },
            utm_params=utm_params,
            pushinpay_response={"error": str(e)},
            status="error",
            errors=[str(e)],
            processing_time_ms=processing_time_ms
        )
        
        return {'error': str(e)}

if __name__ == '__main__':
    # Configurações para desenvolvimento
    print("🚀 Iniciando servidor de integração Utmify + Pushinpay...")
    print(f"📊 Utmify API: {config.UTMIFY_API_URL}")
    print(f"💳 Pushinpay Token: {'✅ Configurado' if config.PUSHINPAY_TOKEN != 'seu_token_pushinpay' else '❌ Não configurado'}")
    print(f"🔑 Utmify API Key: {'✅ Configurado' if config.UTMIFY_API_KEY != 'seu_token_utmify' else '❌ Não configurado'}")
    print("\n📋 Endpoints disponíveis:")
    print("   GET  /              - Informações da API")
    print("   GET  /health        - Verificação de saúde")
    print("   POST /webhook/pushinpay - Webhook da Pushinpay")
    print("   POST /webhook/test  - Teste da integração")
    print("\n⚠️  Lembre-se de configurar as variáveis de ambiente:")
    print("   PUSHINPAY_TOKEN, UTMIFY_API_KEY, UTMIFY_API_URL, WEBHOOK_SECRET")
    print("\n🌐 Servidor rodando em: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)