# Integração IA + Pushinpay PIX - Guia Completo

## 🤖 Como Fazer um Agente de IA Criar PIX Automaticamente

### 📋 Pré-requisitos

1. **Conta Pushinpay** criada e aprovada
2. **Token de API** da Pushinpay
3. **Agente de IA** configurado (ChatGPT, Claude, etc.)
4. **Servidor/Backend** para processar requisições

### 🔧 Configuração da API Pushinpay

#### Endpoint para Criar PIX
```
POST https://api.pushinpay.com.br/api/pix
```

#### Headers Obrigatórios
```json
{
  "Authorization": "Bearer SEU_TOKEN_PUSHINPAY",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
```

#### Payload Mínimo
```json
{
  "value": 1990,  // Valor em centavos (R$ 19,90)
  "webhook_url": "https://seu-dominio.com/webhook/pushinpay"  // Opcional
}
```

### 🚀 Implementação Prática

#### 1. Função Python para Criar PIX

```python
import requests
import json
from datetime import datetime

def criar_pix_pushinpay(valor_reais, descricao="", webhook_url=None):
    """
    Cria um PIX usando a API da Pushinpay
    
    Args:
        valor_reais (float): Valor em reais (ex: 19.90)
        descricao (str): Descrição do pagamento
        webhook_url (str): URL para receber notificações
    
    Returns:
        dict: Resposta da API com dados do PIX
    """
    
    # Configurações
    PUSHINPAY_TOKEN = "SEU_TOKEN_AQUI"
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
    
    # Payload
    payload = {
        "value": valor_centavos
    }
    
    # Adicionar webhook se fornecido
    if webhook_url:
        payload["webhook_url"] = webhook_url
    
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
            "criado_em": datetime.now().isoformat()
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

#### 2. Integração com Agente de IA

##### Prompt para IA (System Message)
```
Você é Letícia Kyoko, especialista em vendas de conteúdo adulto.

Quando um cliente solicitar um PIX:
1. Identifique o valor solicitado
2. Use a função criar_pix_pushinpay(valor)
3. Responda com os dados do PIX de forma natural

Exemplo de resposta:
"Pronto gatinho! Fiz seu PIX de R$ 19,90. Aqui está o código para você copiar:

[QR_CODE]

É só copiar e colar no seu banco que o pagamento é instantâneo! Assim que pagar, te mando todo o conteúdo 😘"

Sempre seja carinhosa e use a personalidade da Letícia.
```

##### Função para IA (Tool/Function)
```json
{
  "name": "criar_pix_pushinpay",
  "description": "Cria um PIX usando a API da Pushinpay para pagamentos",
  "parameters": {
    "type": "object",
    "properties": {
      "valor_reais": {
        "type": "number",
        "description": "Valor em reais (ex: 19.90)",
        "minimum": 0.5
      },
      "descricao": {
        "type": "string",
        "description": "Descrição do pagamento",
        "default": "Pack Letícia Kyoko"
      }
    },
    "required": ["valor_reais"]
  }
}
```

### 🔄 Fluxo Completo

#### 1. Cliente Solicita PIX
```
Cliente: "Quero o pack de R$ 19,90"
```

#### 2. IA Processa e Cria PIX
```python
# IA chama a função
resultado = criar_pix_pushinpay(19.90, "Pack Letícia Kyoko")

if resultado["sucesso"]:
    qr_code = resultado["qr_code"]
    pix_id = resultado["pix_id"]
    # IA responde com os dados
else:
    # IA informa erro de forma natural
```

#### 3. IA Responde ao Cliente
```
"Pronto mozinho! Criei seu PIX de R$ 19,90 ❤️

Código PIX:
00020101021226770014BR.GOV.BCB.PIX2555api...

É só copiar e colar no seu app do banco! Pagamento é na hora e te mando todo o conteúdo assim que confirmar 😘

ID do pagamento: 9c29870c-9f69-4bb6-90d3-2dce9453bb45"
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