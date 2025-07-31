# Integração Utmify + Pushinpay para Tracking de Vendas PIX

## Visão Geral

Este documento explica como integrar a **Utmify** (plataforma de tracking de vendas) com a **Pushinpay** (gateway de pagamentos PIX) para rastrear com precisão a origem das vendas realizadas via PIX.

## Arquitetura da Solução

### Fluxo de Dados
1. **Cliente acessa** o link com parâmetros UTM
2. **Utmify captura** os parâmetros de origem (utm_source, utm_medium, utm_campaign, etc.)
3. **Pushinpay gera** o código PIX para pagamento
4. **Cliente realiza** o pagamento PIX
5. **Pushinpay notifica** via webhook sobre o pagamento aprovado
6. **Sistema processa** e envia dados para Utmify via API

### Componentes Necessários

#### 1. Webhook da Pushinpay
- **Função**: Receber notificações de pagamentos aprovados
- **Endpoint**: Configurado na conta Pushinpay
- **Método**: POST
- **Formato**: JSON

#### 2. API da Utmify
- **Função**: Enviar dados de conversão para tracking
- **Autenticação**: API Key ou Token Bearer
- **Endpoint**: Fornecido pela Utmify

#### 3. Sistema Intermediário (Necessário)
- **Função**: Conectar Pushinpay → Utmify
- **Responsabilidades**:
  - Receber webhooks da Pushinpay
  - Processar dados de pagamento
  - Enviar conversões para Utmify
  - Armazenar parâmetros UTM temporariamente

## Implementação Técnica

### Passo 1: Configuração do Webhook Pushinpay

```json
{
  "webhook_url": "https://seu-dominio.com/webhook/pushinpay",
  "events": ["payment.approved", "payment.completed"]
}
```

**Dados recebidos do webhook:**
```json
{
  "event": "payment.approved",
  "transaction_id": "txn_123456",
  "amount": 99.90,
  "status": "approved",
  "customer_email": "cliente@email.com",
  "custom_data": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "promocao_natal",
    "utm_content": "anuncio_01",
    "utm_term": "produto_digital"
  }
}
```

### Passo 2: Processamento do Webhook

```python
# Exemplo em Python
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/webhook/pushinpay', methods=['POST'])
def processar_webhook_pushinpay():
    try:
        # Receber dados do webhook
        dados = request.json
        
        # Verificar se é um pagamento aprovado
        if dados.get('status') == 'approved':
            # Extrair dados para Utmify
            conversao_data = {
                'transaction_id': dados['transaction_id'],
                'value': dados['amount'],
                'utm_source': dados['custom_data'].get('utm_source'),
                'utm_medium': dados['custom_data'].get('utm_medium'),
                'utm_campaign': dados['custom_data'].get('utm_campaign'),
                'utm_content': dados['custom_data'].get('utm_content'),
                'utm_term': dados['custom_data'].get('utm_term'),
                'customer_email': dados['customer_email']
            }
            
            # Enviar para Utmify
            enviar_para_utmify(conversao_data)
            
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Erro no webhook: {e}")
        return jsonify({'error': str(e)}), 500

def enviar_para_utmify(dados):
    """Envia dados de conversão para Utmify"""
    
    headers = {
        'Authorization': 'Bearer SEU_TOKEN_UTMIFY',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'event': 'conversion',
        'transaction_id': dados['transaction_id'],
        'value': dados['value'],
        'attribution': {
            'utm_source': dados['utm_source'],
            'utm_medium': dados['utm_medium'],
            'utm_campaign': dados['utm_campaign'],
            'utm_content': dados['utm_content'],
            'utm_term': dados['utm_term']
        },
        'customer': {
            'email': dados['customer_email']
        }
    }
    
    try:
        response = requests.post(
            'https://api.utmify.com/v1/conversions',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            print("Conversão enviada com sucesso para Utmify")
        else:
            print(f"Erro ao enviar para Utmify: {response.status_code}")
            
    except Exception as e:
        print(f"Erro na requisição para Utmify: {e}")
```

### Passo 3: Captura de Parâmetros UTM

```javascript
// Script para capturar UTMs no frontend
function capturarUTMs() {
    const urlParams = new URLSearchParams(window.location.search);
    
    const utmData = {
        utm_source: urlParams.get('utm_source'),
        utm_medium: urlParams.get('utm_medium'),
        utm_campaign: urlParams.get('utm_campaign'),
        utm_content: urlParams.get('utm_content'),
        utm_term: urlParams.get('utm_term')
    };
    
    // Armazenar no localStorage para usar no checkout
    localStorage.setItem('utm_data', JSON.stringify(utmData));
    
    return utmData;
}

// Usar no momento de gerar PIX
function gerarPIX(valor, email) {
    const utmData = JSON.parse(localStorage.getItem('utm_data') || '{}');
    
    const payload = {
        amount: valor,
        customer_email: email,
        webhook_url: 'https://seu-dominio.com/webhook/pushinpay',
        custom_data: utmData // Incluir UTMs nos dados customizados
    };
    
    // Enviar para Pushinpay
    fetch('https://api.pushinpay.com.br/api/pix/cashIn', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer SEU_TOKEN_PUSHINPAY',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Exibir QR Code para o cliente
        console.log('PIX gerado:', data);
    });
}
```

## Credenciais Necessárias

### Da Utmify
1. **API Key** ou **Token Bearer**
2. **Webhook URL** (se disponível)
3. **Endpoint da API** para envio de conversões

### Da Pushinpay
1. **Token de API** (Bearer Token)
2. **URL do Webhook** (seu endpoint)
3. **Configuração de eventos** (payment.approved, payment.completed)

## Configuração no Painel Utmify

1. **Acessar** o painel da Utmify
2. **Ir para** Configurações → API
3. **Gerar** uma nova API Key
4. **Configurar** webhook (se disponível):
   - URL: `https://seu-dominio.com/webhook/utmify`
   - Eventos: conversions, attribution
5. **Copiar** credenciais para uso na integração

## Configuração no Painel Pushinpay

1. **Acessar** https://app.pushinpay.com.br
2. **Ir para** Configurações → Webhooks
3. **Adicionar** novo webhook:
   - URL: `https://seu-dominio.com/webhook/pushinpay`
   - Eventos: `payment.approved`, `payment.completed`
4. **Configurar** autenticação (se necessário)
5. **Testar** o webhook

## Estrutura de Dados

### Webhook Pushinpay → Sistema
```json
{
  "event": "payment.approved",
  "transaction_id": "string",
  "amount": "number",
  "status": "string",
  "customer_email": "string",
  "payment_method": "pix",
  "created_at": "datetime",
  "custom_data": {
    "utm_source": "string",
    "utm_medium": "string",
    "utm_campaign": "string",
    "utm_content": "string",
    "utm_term": "string"
  }
}
```

### Sistema → API Utmify
```json
{
  "event": "conversion",
  "transaction_id": "string",
  "value": "number",
  "currency": "BRL",
  "attribution": {
    "utm_source": "string",
    "utm_medium": "string",
    "utm_campaign": "string",
    "utm_content": "string",
    "utm_term": "string"
  },
  "customer": {
    "email": "string",
    "id": "string"
  },
  "timestamp": "datetime"
}
```

## Segurança

### Validação de Webhooks
```python
import hmac
import hashlib

def validar_webhook_pushinpay(payload, signature, secret):
    """Valida a assinatura do webhook da Pushinpay"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)
```

### Autenticação API Utmify
```python
headers = {
    'Authorization': 'Bearer ' + UTMIFY_API_KEY,
    'Content-Type': 'application/json',
    'User-Agent': 'SeuApp/1.0'
}
```

## Monitoramento e Logs

### Logs Essenciais
- Webhooks recebidos da Pushinpay
- Conversões enviadas para Utmify
- Erros de API
- Falhas de validação

### Métricas Importantes
- Taxa de sucesso dos webhooks
- Latência das requisições
- Conversões por fonte UTM
- Receita por campanha

## Troubleshooting

### Problemas Comuns

1. **Webhook não recebido**
   - Verificar URL configurada
   - Testar conectividade
   - Verificar logs do servidor

2. **UTMs não capturados**
   - Verificar JavaScript no frontend
   - Confirmar localStorage
   - Testar com URLs de exemplo

3. **Erro na API Utmify**
   - Verificar credenciais
   - Validar formato dos dados
   - Conferir rate limits

### Comandos de Teste

```bash
# Testar webhook
curl -X POST https://seu-dominio.com/webhook/pushinpay \
  -H "Content-Type: application/json" \
  -d '{"event":"payment.approved","transaction_id":"test_123"}'

# Testar API Utmify
curl -X POST https://api.utmify.com/v1/conversions \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event":"conversion","value":99.90}'
```

## Conclusão

A integração entre Utmify e Pushinpay **requer o desenvolvimento de um sistema intermediário** que:

1. **Receba** webhooks da Pushinpay
2. **Processe** dados de pagamento
3. **Envie** conversões para Utmify via API
4. **Gerencie** parâmetros UTM durante o fluxo

**Não é possível** uma integração direta entre as duas plataformas, sendo necessário programar uma API/webhook personalizada para fazer a ponte entre os sistemas.

---

**Próximos Passos:**
1. Obter credenciais da Utmify e Pushinpay
2. Desenvolver o sistema intermediário
3. Configurar webhooks em ambas as plataformas
4. Implementar captura de UTMs no frontend
5. Testar o fluxo completo
6. Monitorar e otimizar a integração