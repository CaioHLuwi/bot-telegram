#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend para Integração PIX + ZapVoice

Este backend:
1. Gera PIX com nome/valor/descrição via Pushinpay
2. Retorna QR Code para o frontend
3. Recebe webhooks de pagamento
4. Atualiza status do pedido no ZapVoice

Autor: Bot Kyoko Team
Data: 2024
"""

import os
import json
import hmac
import hashlib
import logging
import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
import uuid

# Carregar variáveis de ambiente
load_dotenv('.env.integracao')

# Configuração do Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para frontend

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend_pix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações da API
PUSHINPAY_TOKEN = os.getenv('PUSHINPAY_TOKEN', '39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5')
PUSHINPAY_BASE_URL = os.getenv('PUSHINPAY_BASE_URL', 'https://api.pushinpay.com.br/api')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'minha_chave_secreta_webhook')
ZAPVOICE_API_KEY = os.getenv('ZAPVOICE_API_KEY', '')
ZAPVOICE_BASE_URL = os.getenv('ZAPVOICE_BASE_URL', 'https://api.zapvoice.com.br')

# Armazenamento em memória para pedidos (em produção, usar banco de dados)
pedidos = {}

class PushinpayAPI:
    """Classe para interagir com a API Pushinpay"""
    
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def criar_pix(self, valor, nome_cliente, descricao, pedido_id):
        """Cria um PIX na Pushinpay"""
        try:
            url = f"{self.base_url}/pix"
            
            payload = {
                'amount': float(valor),
                'description': descricao,
                'payer_name': nome_cliente,
                'external_id': pedido_id,
                'expires_in': 1800,  # 30 minutos
                'webhook_url': f"{os.getenv('WEBHOOK_BASE_URL', 'https://seu-dominio.com')}/webhook/pushinpay"
            }
            
            logger.info(f"Criando PIX: {payload}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code == 201:
                data = response.json()
                logger.info(f"PIX criado com sucesso: {data.get('id')}")
                return {
                    'success': True,
                    'data': data
                }
            else:
                logger.error(f"Erro ao criar PIX: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"Erro {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Exceção ao criar PIX: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def consultar_pagamento(self, payment_id):
        """Consulta status de um pagamento"""
        try:
            url = f"{self.base_url}/pix/{payment_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"Erro {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao consultar pagamento: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

class ZapVoiceAPI:
    """Classe para interagir com a API ZapVoice"""
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def atualizar_pedido(self, pedido_id, status, dados_pagamento=None):
        """Atualiza status do pedido no ZapVoice"""
        try:
            url = f"{self.base_url}/orders/{pedido_id}"
            
            payload = {
                'status': status,
                'updated_at': datetime.now().isoformat(),
            }
            
            if dados_pagamento:
                payload['payment_data'] = dados_pagamento
            
            logger.info(f"Atualizando pedido {pedido_id} no ZapVoice: {status}")
            response = requests.put(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code in [200, 204]:
                logger.info(f"Pedido {pedido_id} atualizado com sucesso")
                return {'success': True}
            else:
                logger.error(f"Erro ao atualizar pedido: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"Erro {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Erro ao atualizar pedido no ZapVoice: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def enviar_produto(self, pedido_id, cliente_info, produto_info):
        """Envia produto/conteúdo para o cliente via ZapVoice"""
        try:
            url = f"{self.base_url}/messages/send"
            
            payload = {
                'phone': cliente_info.get('phone'),
                'message': f"🎉 Pagamento confirmado!\n\n"
                          f"Pedido: {pedido_id}\n"
                          f"Produto: {produto_info.get('name')}\n\n"
                          f"Seu conteúdo está sendo preparado e será enviado em breve!",
                'order_id': pedido_id
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Mensagem enviada para {cliente_info.get('phone')}")
                return {'success': True}
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Erro ao enviar produto: {str(e)}")
            return {'success': False, 'error': str(e)}

# Instanciar APIs
pushinpay = PushinpayAPI(PUSHINPAY_TOKEN, PUSHINPAY_BASE_URL)
zapvoice = ZapVoiceAPI(ZAPVOICE_API_KEY, ZAPVOICE_BASE_URL) if ZAPVOICE_API_KEY else None

def validar_webhook_signature(payload, signature):
    """Valida assinatura do webhook"""
    if not WEBHOOK_SECRET:
        return True  # Se não há secret configurado, aceita
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de saúde do serviço"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'pushinpay': 'configured' if PUSHINPAY_TOKEN else 'not_configured',
            'zapvoice': 'configured' if ZAPVOICE_API_KEY else 'not_configured'
        }
    })

@app.route('/pix/criar', methods=['POST'])
def criar_pix():
    """Endpoint para criar PIX"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['valor', 'nome_cliente', 'descricao']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }), 400
        
        # Gerar ID único para o pedido
        pedido_id = data.get('pedido_id', str(uuid.uuid4()))
        
        # Criar PIX na Pushinpay
        resultado = pushinpay.criar_pix(
            valor=data['valor'],
            nome_cliente=data['nome_cliente'],
            descricao=data['descricao'],
            pedido_id=pedido_id
        )
        
        if resultado['success']:
            pix_data = resultado['data']
            
            # Armazenar informações do pedido
            pedidos[pedido_id] = {
                'id': pedido_id,
                'valor': data['valor'],
                'nome_cliente': data['nome_cliente'],
                'descricao': data['descricao'],
                'pix_id': pix_data.get('id'),
                'qr_code': pix_data.get('qr_code'),
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'cliente_info': data.get('cliente_info', {}),
                'produto_info': data.get('produto_info', {})
            }
            
            return jsonify({
                'success': True,
                'pedido_id': pedido_id,
                'pix_id': pix_data.get('id'),
                'qr_code': pix_data.get('qr_code'),
                'qr_code_image': pix_data.get('qr_code_image'),
                'expires_at': pix_data.get('expires_at'),
                'valor': data['valor']
            })
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        logger.error(f"Erro ao criar PIX: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@app.route('/pix/status/<pedido_id>', methods=['GET'])
def consultar_status_pedido(pedido_id):
    """Consulta status de um pedido"""
    try:
        if pedido_id not in pedidos:
            return jsonify({
                'success': False,
                'error': 'Pedido não encontrado'
            }), 404
        
        pedido = pedidos[pedido_id]
        
        # Consultar status atual na Pushinpay
        if pedido.get('pix_id'):
            resultado = pushinpay.consultar_pagamento(pedido['pix_id'])
            
            if resultado['success']:
                pix_data = resultado['data']
                status_atual = pix_data.get('status', 'pending')
                
                # Atualizar status local
                pedido['status'] = status_atual
                pedido['updated_at'] = datetime.now().isoformat()
                
                return jsonify({
                    'success': True,
                    'pedido_id': pedido_id,
                    'status': status_atual,
                    'valor': pedido['valor'],
                    'created_at': pedido['created_at'],
                    'updated_at': pedido.get('updated_at')
                })
        
        return jsonify({
            'success': True,
            'pedido_id': pedido_id,
            'status': pedido['status'],
            'valor': pedido['valor'],
            'created_at': pedido['created_at']
        })
        
    except Exception as e:
        logger.error(f"Erro ao consultar status: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    """Webhook para receber notificações da Pushinpay"""
    try:
        # Validar assinatura se configurada
        signature = request.headers.get('X-Pushinpay-Signature', '')
        payload = request.get_data()
        
        if not validar_webhook_signature(payload, signature):
            logger.warning("Webhook com assinatura inválida")
            abort(401)
        
        data = request.get_json()
        logger.info(f"Webhook recebido: {data}")
        
        # Extrair informações do webhook
        pix_id = data.get('id')
        status = data.get('status')
        external_id = data.get('external_id')  # nosso pedido_id
        
        if not external_id or external_id not in pedidos:
            logger.warning(f"Pedido não encontrado: {external_id}")
            return jsonify({'success': False, 'error': 'Pedido não encontrado'}), 404
        
        # Atualizar pedido local
        pedido = pedidos[external_id]
        pedido['status'] = status
        pedido['updated_at'] = datetime.now().isoformat()
        pedido['webhook_data'] = data
        
        # Se pagamento foi aprovado
        if status == 'paid':
            logger.info(f"Pagamento confirmado para pedido {external_id}")
            
            # Atualizar no ZapVoice se configurado
            if zapvoice:
                resultado_zapvoice = zapvoice.atualizar_pedido(
                    external_id, 
                    'paid',
                    {
                        'pix_id': pix_id,
                        'paid_at': data.get('paid_at'),
                        'amount': data.get('amount')
                    }
                )
                
                if resultado_zapvoice['success']:
                    # Enviar produto/conteúdo
                    zapvoice.enviar_produto(
                        external_id,
                        pedido.get('cliente_info', {}),
                        pedido.get('produto_info', {})
                    )
            
            pedido['processed'] = True
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    """Lista todos os pedidos (para debug/admin)"""
    try:
        return jsonify({
            'success': True,
            'pedidos': list(pedidos.values()),
            'total': len(pedidos)
        })
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@app.route('/zapvoice/test', methods=['POST'])
def test_zapvoice():
    """Endpoint para testar integração ZapVoice"""
    try:
        if not zapvoice:
            return jsonify({
                'success': False,
                'error': 'ZapVoice não configurado'
            }), 400
        
        data = request.get_json()
        pedido_id = data.get('pedido_id', 'test_' + str(uuid.uuid4()))
        
        resultado = zapvoice.atualizar_pedido(pedido_id, 'test')
        
        return jsonify({
            'success': True,
            'zapvoice_result': resultado
        })
        
    except Exception as e:
        logger.error(f"Erro no teste ZapVoice: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Pushinpay configurado: {'Sim' if PUSHINPAY_TOKEN else 'Não'}")
    logger.info(f"ZapVoice configurado: {'Sim' if ZAPVOICE_API_KEY else 'Não'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)