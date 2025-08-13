# Integração IA + Pushinpay PIX + UTMify - Guia Completo

## 🤖 Como Fazer um Agente de IA Criar PIX Automaticamente com Tracking UTMify

### 🎯 Visão Geral

Este guia demonstra como integrar:
- **Pushinpay**: Para geração automática de PIX
- **UTMify**: Para rastreamento de conversões e vendas
- **Bot Telegram**: Para automação de vendas

A integração permite rastrear a origem de cada venda (Facebook, Instagram, Google, etc.) e medir o ROI de campanhas publicitárias.

### 📋 Pré-requisitos

1. **Conta Pushinpay** criada e aprovada
2. **Token de API** da Pushinpay
3. **Conta UTMify** ativa
4. **Token de API** da UTMify (x-api-token)
5. **Agente de IA** configurado (ChatGPT, Claude, etc.)
6. **Servidor/Backend** para processar requisições e webhooks
7. **Domínio público** para receber webhooks da Pushinpay

### 🔧 Configuração das APIs

#### API Pushinpay - Criar PIX
```
POST https://api.pushinpay.com.br/api/pix
```

**Headers Obrigatórios:**
```json
{
  "Authorization": "Bearer SEU_TOKEN_PUSHINPAY",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
```

**Payload Mínimo:**
```json
{
  "value": 1990,  // Valor em centavos (R$ 19,90)
  "webhook_url": "https://seu-dominio.com/webhook/pushinpay",
  "custom_data": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "pack_digital",
    "utm_content": "anuncio_01",
    "utm_term": "pack"
  }
}
```

#### API UTMify - Enviar Conversão
```
POST https://api.utmify.com.br/api-credentials/orders
```

**Headers Obrigatórios:**
```json
{
  "x-api-token": "SEU_TOKEN_UTMIFY",
  "Content-Type": "application/json"
}
```

**Payload Completo:**
```json
{
  "order_id": "pix_123456789",
  "total_value": 19.90,
  "currency": "BRL",
  "status": "completed",
  "payment_method": "pix",
  "customer": {
    "email": "cliente@email.com",
    "name": "Cliente",
    "phone": "",
    "document": ""
  },
  "products": [{
    "name": "Pack Digital",
    "quantity": 1,
    "price": 19.90
  }],
  "tracking": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "pack_digital",
    "utm_content": "anuncio_01",
    "utm_term": "pack",
    "src": "",
    "sck": "",
    "fbclid": "",
    "gclid": ""
  },
  "commission": {
    "value": 0,
    "type": "fixed"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 🚀 Implementação Prática

#### 1. Função Python Completa com UTMify

```python
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

def criar_pix_com_tracking(valor_reais: float, email: str, utm_params: Dict[str, str], descricao: str = "Pack Digital") -> Dict[str, Any]:
    """
    Cria um PIX usando a API da Pushinpay com parâmetros UTM para tracking
    
    Args:
        valor_reais (float): Valor em reais (ex: 19.90)
        email (str): Email do cliente
        utm_params (dict): Parâmetros UTM para tracking
        descricao (str): Descrição do pagamento
    
    Returns:
        dict: Resposta da API com dados do PIX
    """
    
    # Configurações
    PUSHINPAY_TOKEN = "SEU_TOKEN_PUSHINPAY"
    WEBHOOK_URL = "https://seu-dominio.com/webhook/pushinpay"
    API_URL = "https://api.pushinpay.com.br/api/pix"
    
    # Converter valor para centavos
    valor_centavos = int(valor_reais * 100)
    
    # Validar valor mínimo (50 centavos)
    if valor_centavos < 50:
        raise ValueError("Valor mínimo é R$ 0,50")
    
    # Headers
    headers = {
        "Authorization": f"Bearer {PUSHINPAY_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Payload com UTM tracking
    payload = {
        "value": valor_centavos,
        "webhook_url": WEBHOOK_URL,
        "custom_data": {
            "customer_email": email,
            "description": descricao,
            "utm_source": utm_params.get('utm_source', ''),
            "utm_medium": utm_params.get('utm_medium', ''),
            "utm_campaign": utm_params.get('utm_campaign', ''),
            "utm_content": utm_params.get('utm_content', ''),
            "utm_term": utm_params.get('utm_term', ''),
            "fbclid": utm_params.get('fbclid', ''),
            "gclid": utm_params.get('gclid', '')
        }
    }
    
    try:
        # Fazer requisição
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Retornar dados do PIX
        pix_data = response.json()
        
        return {
            "sucesso": True,
            "pix_id": pix_data["id"],
            "qr_code": pix_data["qr_code"],
            "qr_code_base64": pix_data["qr_code_base64"],
            "valor": valor_reais,
            "status": pix_data["status"],
            "criado_em": datetime.now().isoformat(),
            "tracking_params": utm_params
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "sucesso": False,
            "erro": f"Erro na API: {str(e)}",
            "valor": valor_reais
        }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": f"Erro interno: {str(e)}",
            "valor": valor_reais
        }
```

#### 2. Função para Enviar Conversão para UTMify

```python
def enviar_conversao_utmify(dados_conversao: Dict[str, Any]) -> bool:
    """
    Envia dados de conversão para UTMify seguindo a documentação oficial
    
    Args:
        dados_conversao (dict): Dados da conversão do webhook Pushinpay
    
    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    
    # Configurações
    UTMIFY_API_KEY = "SEU_TOKEN_UTMIFY"
    UTMIFY_API_URL = "https://api.utmify.com.br/api-credentials/orders"
    
    headers = {
        'x-api-token': UTMIFY_API_KEY,
        'Content-Type': 'application/json'
    }
    
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
    
    try:
        response = requests.post(UTMIFY_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code in [200, 201]:
            print(f"✅ Conversão enviada para UTMify: {payload['order_id']}")
            return True
        else:
            print(f"❌ Erro ao enviar para UTMify: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar para UTMify: {e}")
        return False
```

#### 3. Webhook para Receber Notificações da Pushinpay

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    """
    Endpoint para receber webhooks da Pushinpay e enviar para UTMify
    """
    try:
        # Obter dados da requisição
        dados = request.get_json()
        
        # Verificar se é um pagamento aprovado
        if dados.get('status') not in ['approved', 'completed', 'paid']:
            return jsonify({'status': 'ignored', 'message': 'Payment not approved'}), 200
        
        # Extrair dados relevantes
        custom_data = dados.get('custom_data', {})
        if isinstance(custom_data, str):
            try:
                custom_data = json.loads(custom_data)
            except json.JSONDecodeError:
                custom_data = {}
        
        conversao_data = {
            'transaction_id': dados.get('transaction_id') or dados.get('id'),
            'value': dados.get('amount') or dados.get('value'),
            'customer_email': custom_data.get('customer_email', ''),
            'customer_name': custom_data.get('customer_name', 'Cliente'),
            'status': dados.get('status'),
            'payment_method': 'pix',
            'utm_source': custom_data.get('utm_source', ''),
            'utm_medium': custom_data.get('utm_medium', ''),
            'utm_campaign': custom_data.get('utm_campaign', ''),
            'utm_content': custom_data.get('utm_content', ''),
            'utm_term': custom_data.get('utm_term', ''),
            'fbclid': custom_data.get('fbclid', ''),
            'gclid': custom_data.get('gclid', '')
        }
        
        # Enviar para UTMify
        sucesso = enviar_conversao_utmify(conversao_data)
        
        if sucesso:
            return jsonify({
                'status': 'success',
                'message': 'Conversion tracked successfully',
                'transaction_id': conversao_data['transaction_id']
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to track conversion'
            }), 500
            
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### 4. Integração com Bot Telegram/IA

##### Prompt para IA (System Message)
```
Você é Letícia Kyoko, especialista em vendas de conteúdo adulto.

Quando um cliente solicitar um PIX:
1. Identifique o valor solicitado e email do cliente
2. Extraia parâmetros UTM da conversa (se disponíveis)
3. Use a função criar_pix_com_tracking(valor, email, utm_params)
4. Responda com os dados do PIX de forma natural

Exemplo de resposta:
"Pronto gatinho! Fiz seu PIX de R$ 19,90. Aqui está o código para você copiar:

[QR_CODE]

É só copiar e colar no seu banco que o pagamento é instantâneo! Assim que pagar, te mando todo o conteúdo 😘

ID do pagamento: [PIX_ID]"

Sempre seja carinhosa e use a personalidade da Letícia.
Sempre peça o email do cliente antes de gerar o PIX.
```

##### Função para IA (Tool/Function)
```json
{
  "name": "criar_pix_com_tracking",
  "description": "Cria um PIX usando a API da Pushinpay com tracking UTMify",
  "parameters": {
    "type": "object",
    "properties": {
      "valor_reais": {
        "type": "number",
        "description": "Valor em reais (ex: 19.90)",
        "minimum": 0.5
      },
      "email": {
        "type": "string",
        "description": "Email do cliente",
        "format": "email"
      },
      "utm_params": {
        "type": "object",
        "description": "Parâmetros UTM para tracking",
        "properties": {
          "utm_source": {"type": "string", "description": "Fonte do tráfego (facebook, instagram, google)"},
          "utm_medium": {"type": "string", "description": "Meio (cpc, organic, social)"},
          "utm_campaign": {"type": "string", "description": "Nome da campanha"},
          "utm_content": {"type": "string", "description": "Conteúdo do anúncio"},
          "utm_term": {"type": "string", "description": "Termo de pesquisa"},
          "fbclid": {"type": "string", "description": "Facebook Click ID"},
          "gclid": {"type": "string", "description": "Google Click ID"}
        }
      },
      "descricao": {
        "type": "string",
        "description": "Descrição do pagamento",
        "default": "Pack Digital"
      }
    },
    "required": ["valor_reais", "email"]
  }
}
```

### 🔧 Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Tokens das APIs
PUSHINPAY_TOKEN=seu_token_pushinpay_aqui
UTMIFY_API_KEY=seu_token_utmify_aqui

# URLs das APIs
UTMIFY_API_URL=https://api.utmify.com.br/api-credentials/orders
WEBHOOK_SECRET=seu_secret_webhook_aqui

# Configurações do servidor
FLASK_ENV=production
PORT=5000
```

### 🔄 Fluxo Completo da Integração

#### 1. Cliente Solicita PIX
```
Cliente: "Quero o pack de R$ 19,90"
Bot: "Perfeito! Preciso do seu email para gerar o PIX 😊"
Cliente: "meu.email@gmail.com"
```

#### 2. IA Processa e Cria PIX com Tracking
```python
# IA extrai parâmetros UTM (se disponíveis)
utm_params = {
    'utm_source': 'telegram',
    'utm_medium': 'bot',
    'utm_campaign': 'pack_digital',
    'utm_content': 'conversa_direta'
}

# IA chama a função
resultado = criar_pix_com_tracking(
    valor_reais=19.90,
    email="meu.email@gmail.com",
    utm_params=utm_params,
    descricao="Pack Digital Letícia"
)

if resultado["sucesso"]:
    qr_code = resultado["qr_code"]
    pix_id = resultado["pix_id"]
    # IA responde com os dados
else:
    # IA informa erro de forma natural
```

#### 3. IA Responde ao Cliente
```
"Pronto gatinho! Criei seu PIX de R$ 19,90 ❤️

Código PIX:
00020101021226770014BR.GOV.BCB.PIX2555api...

É só copiar e colar no seu app do banco! Pagamento é na hora e te mando todo o conteúdo assim que confirmar 😘

ID do pagamento: 9c29870c-9f69-4bb6-90d3-2dce9453bb45"
```

#### 4. Cliente Paga o PIX
- Cliente copia o código PIX
- Realiza o pagamento no banco
- Pushinpay detecta o pagamento

#### 5. Webhook Automático
- Pushinpay envia webhook para seu servidor
- Servidor processa os dados do pagamento
- Dados são enviados automaticamente para UTMify
- UTMify registra a conversão com parâmetros UTM

#### 6. Confirmação e Entrega
```
"🎉 Pagamento confirmado!

Obrigada pela compra, gatinho! Aqui está seu pack completo:

📁 [LINK_DO_CONTEUDO]

Qualquer dúvida, é só chamar! 😘"
```

### 🎯 Implementação no ChatGPT/Claude

#### Configuração de Function Calling

```javascript
// Para OpenAI GPT
const functions = [
  {
    name: "criar_pix_pushinpay",
    description: "Cria PIX para pagamentos usando Pushinpay",
    parameters: {
      type: "object",
      properties: {
        valor_reais: {
          type: "number",
          description: "Valor em reais"
        }
      },
      required: ["valor_reais"]
    }
  }
];

// Chamada da API
const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    {role: "system", content: "Você é Letícia Kyoko..."},
    {role: "user", content: "Quero o pack de R$ 19,90"}
  ],
  functions: functions,
  function_call: "auto"
});
```

### 📊 Tratamento de Respostas

#### Resposta de Sucesso da API
```json
{
  "id": "9c29870c-9f69-4bb6-90d3-2dce9453bb45",
  "qr_code": "00020101021226770014BR.GOV.BCB.PIX2555api...",
  "status": "created",
  "value": 1990,
  "webhook_url": "https://seu-dominio.com/webhook",
  "qr_code_base64": "data:image/png;base64,iVBORw0KGgoAA.....",
  "webhook": null,
  "split_rules": [],
  "end_to_end_id": null,
  "payer_name": null,
  "payer_national_registration": null
}
```

#### Como a IA Deve Processar
```python
def processar_resposta_pix(resposta_api):
    if resposta_api["sucesso"]:
        return f"""
Pronto gatinho! Seu PIX de R$ {resposta_api['valor']:.2f} está criado ❤️

🔸 **Código PIX:**
`{resposta_api['qr_code']}`

🔸 **ID do Pagamento:**
`{resposta_api['pix_id']}`

É só copiar o código PIX e colar no seu banco! O pagamento é instantâneo e te mando todo o conteúdo assim que confirmar 😘
"""
    else:
        return f"""
Ai que pena gatinho, deu um probleminha para criar seu PIX 😔

Erro: {resposta_api['erro']}

Tenta de novo em alguns minutinhos ou me chama que a gente resolve juntos ❤️
"""
```

### 🔒 Segurança e Boas Práticas

#### 1. Validações Importantes
```python
def validar_valor_pix(valor):
    # Valor mínimo Pushinpay
    if valor < 0.50:
        return False, "Valor mínimo é R$ 0,50"
    
    # Valor máximo (verificar limite da conta)
    if valor > 1000.00:
        return False, "Valor máximo é R$ 1.000,00"
    
    return True, "Valor válido"
```

#### 2. Rate Limiting
```python
import time
from collections import defaultdict

# Controle de rate limiting
rate_limit = defaultdict(list)

def verificar_rate_limit(user_id, limite=5, janela=60):
    agora = time.time()
    
    # Limpar requisições antigas
    rate_limit[user_id] = [
        timestamp for timestamp in rate_limit[user_id]
        if agora - timestamp < janela
    ]
    
    # Verificar limite
    if len(rate_limit[user_id]) >= limite:
        return False, "Muitas tentativas. Aguarde um minuto."
    
    # Adicionar nova requisição
    rate_limit[user_id].append(agora)
    return True, "OK"
```

#### 3. Logs e Monitoramento
```python
import logging

def log_criacao_pix(user_id, valor, resultado):
    logging.info(f"""
    PIX_CRIADO:
    - User: {user_id}
    - Valor: R$ {valor:.2f}
    - Sucesso: {resultado['sucesso']}
    - PIX ID: {resultado.get('pix_id', 'N/A')}
    - Timestamp: {datetime.now()}
    """)
```

### 🎯 Exemplo Completo de Integração

```python
class LeticiaKyokoIA:
    def __init__(self, pushinpay_token):
        self.pushinpay_token = pushinpay_token
        self.rate_limit = defaultdict(list)
    
    def processar_mensagem(self, user_id, mensagem):
        # Verificar se é solicitação de PIX
        if "pix" in mensagem.lower() or "pack" in mensagem.lower():
            # Extrair valor da mensagem
            valor = self.extrair_valor(mensagem)
            
            if valor:
                return self.criar_pix_para_usuario(user_id, valor)
            else:
                return "Qual valor você quer no PIX, gatinho? 😘"
        
        # Outras respostas da Letícia...
        return self.resposta_padrao(mensagem)
    
    def criar_pix_para_usuario(self, user_id, valor):
        # Verificar rate limit
        pode_criar, msg = verificar_rate_limit(user_id)
        if not pode_criar:
            return f"Calma gatinho! {msg} ❤️"
        
        # Criar PIX
        resultado = criar_pix_pushinpay(valor)
        
        # Log
        log_criacao_pix(user_id, valor, resultado)
        
        # Responder
        return processar_resposta_pix(resultado)
```

### 📱 Integração com Telegram/WhatsApp

```python
# Para Telegram Bot
from telegram import Update
from telegram.ext import ContextTypes

async def handle_pix_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mensagem = update.message.text
    
    # Processar com IA
    leticia = LeticiaKyokoIA(PUSHINPAY_TOKEN)
    resposta = leticia.processar_mensagem(user_id, mensagem)
    
    # Enviar resposta
    await update.message.reply_text(resposta)
```

### 🔄 Webhook para Confirmação de Pagamento

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    data = request.json
    
    if data['status'] == 'paid':
        # Pagamento confirmado
        pix_id = data['id']
        valor = data['value'] / 100  # Converter centavos para reais
        
        # Enviar conteúdo para o cliente
        enviar_conteudo_cliente(pix_id, valor)
        
        return jsonify({"status": "success"})
    
    return jsonify({"status": "received"})

def enviar_conteudo_cliente(pix_id, valor):
    # Lógica para enviar o conteúdo
    # Pode ser via Telegram, WhatsApp, email, etc.
    pass
```

---

## 🎯 Resumo da Implementação

1. **Configure** a função `criar_pix_pushinpay()` com seu token
2. **Integre** com seu agente de IA usando Function Calling
3. **Configure** o webhook para confirmação de pagamentos
4. **Teste** com valores pequenos primeiro
5. **Monitore** logs e rate limiting
6. **Implemente** em produção

### ✅ Checklist Final

- [ ] Token Pushinpay configurado
- [ ] Função de criação de PIX testada
- [ ] IA configurada com Function Calling
- [ ] Webhook de confirmação implementado
- [ ] Rate limiting ativo
- [ ] Logs configurados
- [ ] Testes realizados
- [ ] Deploy em produção

**Com essa implementação, sua IA poderá criar PIX automaticamente e processar pagamentos de forma natural e eficiente!** 🚀