# Integração UTMify + Pushinpay - Versão Corrigida

## 🎯 Visão Geral

Esta documentação apresenta a integração **corrigida** entre UTMify e Pushinpay para rastreamento automático de vendas PIX com parâmetros UTM.

### ✅ Correções Implementadas

1. **URL da API UTMify corrigida**: `https://api.utmify.com.br/api-credentials/orders`
2. **Header de autenticação correto**: `x-api-token` (não Bearer)
3. **Payload seguindo documentação oficial** da UTMify brasileira
4. **Estrutura de dados completa** para tracking de conversões
5. **Tratamento de erros aprimorado**

## 🔧 Configurações Necessárias

### Variáveis de Ambiente

```bash
# .env
PUSHINPAY_TOKEN=42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1
UTMIFY_API_KEY=seu_token_utmify_aqui
UTMIFY_API_URL=https://api.utmify.com.br/api-credentials/orders
WEBHOOK_SECRET=seu_secret_webhook_seguro
```

### Dependências Python

```bash
pip install requests flask python-dotenv
```

## 📊 API UTMify - Documentação Oficial

### Endpoint Correto
```
POST https://api.utmify.com.br/api-credentials/orders
```

### Headers Obrigatórios
```json
{
  "x-api-token": "SEU_TOKEN_UTMIFY",
  "Content-Type": "application/json"
}
```

### Payload Completo (Seguindo Documentação Oficial)
```json
{
  "order_id": "pix_123456789",
  "total_value": 19.90,
  "currency": "BRL",
  "status": "completed",
  "payment_method": "pix",
  "customer": {
    "email": "cliente@email.com",
    "name": "Nome do Cliente",
    "phone": "+5511999999999",
    "document": "12345678901"
  },
  "products": [{
    "name": "Pack Digital",
    "quantity": 1,
    "price": 19.90
  }],
  "tracking": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "pack_digital_2024",
    "utm_content": "anuncio_video_01",
    "utm_term": "pack+digital",
    "src": "",
    "sck": "",
    "fbclid": "IwAR123...",
    "gclid": "Cj0KCQ..."
  },
  "commission": {
    "value": 0,
    "type": "fixed"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

## 🚀 Implementação Corrigida

### Classe UtmifyIntegration Atualizada

```python
import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import logging

class UtmifyIntegration:
    """Classe para gerenciar integração com UTMify - Versão Corrigida"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        # Header correto conforme documentação oficial
        self.headers = {
            'x-api-token': api_key,  # ✅ Correto: x-api-token (não Bearer)
            'Content-Type': 'application/json',
            'User-Agent': 'KyokoBot-Utmify/2.0'
        }
    
    def enviar_conversao(self, dados_conversao: Dict[str, Any]) -> bool:
        """Envia dados de conversão para UTMify seguindo a documentação oficial"""
        try:
            # ✅ Payload seguindo a documentação oficial da UTMify brasileira
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
            
            logging.info(f"📊 Enviando conversão para UTMify: {payload['order_id']}")
            
            # ✅ URL correta da API
            response = requests.post(
                self.base_url,  # https://api.utmify.com.br/api-credentials/orders
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logging.info(f"✅ Conversão enviada com sucesso: {response.status_code}")
                return True
            else:
                logging.error(f"❌ Erro ao enviar conversão: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erro de rede ao enviar para UTMify: {e}")
            return False
        except Exception as e:
            logging.error(f"❌ Erro inesperado ao enviar para UTMify: {e}")
            return False
    
    def _limpar_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Remove campos vazios ou None do payload"""
        def limpar_dict(d):
            if isinstance(d, dict):
                return {k: limpar_dict(v) for k, v in d.items() 
                       if v is not None and v != '' and v != {}}
            return d
        
        return limpar_dict(payload)
```

### Webhook Pushinpay Atualizado

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Configuração corrigida
config = {
    'PUSHINPAY_TOKEN': os.getenv('PUSHINPAY_TOKEN'),
    'UTMIFY_API_KEY': os.getenv('UTMIFY_API_KEY'),
    'UTMIFY_API_URL': 'https://api.utmify.com.br/api-credentials/orders',  # ✅ URL correta
    'WEBHOOK_SECRET': os.getenv('WEBHOOK_SECRET')
}

# Instanciar integração UTMify
utmify = UtmifyIntegration(config['UTMIFY_API_KEY'], config['UTMIFY_API_URL'])

@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    """Endpoint para receber webhooks da Pushinpay - Versão Corrigida"""
    try:
        dados = request.get_json()
        
        # Verificar se é um pagamento aprovado
        if dados.get('status') not in ['approved', 'completed', 'paid']:
            return jsonify({'status': 'ignored', 'message': 'Payment not approved'}), 200
        
        # Extrair custom_data com parâmetros UTM
        custom_data = dados.get('custom_data', {})
        if isinstance(custom_data, str):
            try:
                custom_data = json.loads(custom_data)
            except json.JSONDecodeError:
                custom_data = {}
        
        # ✅ Estrutura de dados corrigida para UTMify
        conversao_data = {
            'transaction_id': dados.get('transaction_id') or dados.get('id'),
            'value': dados.get('amount') or dados.get('value'),
            'customer_email': custom_data.get('customer_email', ''),
            'customer_name': custom_data.get('customer_name', 'Cliente'),
            'customer_phone': custom_data.get('customer_phone', ''),
            'customer_document': custom_data.get('customer_document', ''),
            'status': dados.get('status'),
            'payment_method': 'pix',
            # Parâmetros UTM
            'utm_source': custom_data.get('utm_source', ''),
            'utm_medium': custom_data.get('utm_medium', ''),
            'utm_campaign': custom_data.get('utm_campaign', ''),
            'utm_content': custom_data.get('utm_content', ''),
            'utm_term': custom_data.get('utm_term', ''),
            'src': custom_data.get('src', ''),
            'sck': custom_data.get('sck', ''),
            'fbclid': custom_data.get('fbclid', ''),
            'gclid': custom_data.get('gclid', '')
        }
        
        # ✅ Enviar para UTMify com estrutura corrigida
        sucesso = utmify.enviar_conversao(conversao_data)
        
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
        logging.error(f"❌ Erro no webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🧪 Teste da Integração

### Script de Teste

```python
import requests
import json
from datetime import datetime

def testar_integracao_utmify():
    """Testa a integração corrigida com UTMify"""
    
    # Configurações
    UTMIFY_API_KEY = "seu_token_utmify"
    UTMIFY_API_URL = "https://api.utmify.com.br/api-credentials/orders"
    
    headers = {
        'x-api-token': UTMIFY_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Dados de teste
    payload = {
        'order_id': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'total_value': 19.90,
        'currency': 'BRL',
        'status': 'completed',
        'payment_method': 'pix',
        'customer': {
            'email': 'teste@exemplo.com',
            'name': 'Cliente Teste',
            'phone': '+5511999999999',
            'document': '12345678901'
        },
        'products': [{
            'name': 'Pack Digital Teste',
            'quantity': 1,
            'price': 19.90
        }],
        'tracking': {
            'utm_source': 'telegram',
            'utm_medium': 'bot',
            'utm_campaign': 'teste_integracao',
            'utm_content': 'teste_correcao',
            'utm_term': 'pack_digital'
        },
        'commission': {
            'value': 0,
            'type': 'fixed'
        },
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    try:
        response = requests.post(UTMIFY_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Teste da integração UTMify: SUCESSO")
            return True
        else:
            print("❌ Teste da integração UTMify: FALHOU")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == '__main__':
    testar_integracao_utmify()
```

## 📋 Checklist de Verificação

### ✅ Configurações Corretas

- [ ] Token UTMify configurado na variável `UTMIFY_API_KEY`
- [ ] URL da API: `https://api.utmify.com.br/api-credentials/orders`
- [ ] Header de autenticação: `x-api-token`
- [ ] Payload seguindo estrutura oficial da UTMify
- [ ] Webhook da Pushinpay configurado
- [ ] Servidor público para receber webhooks

### ✅ Testes Necessários

- [ ] Teste de criação de PIX com parâmetros UTM
- [ ] Teste de webhook da Pushinpay
- [ ] Teste de envio para UTMify
- [ ] Verificação de dados no painel UTMify
- [ ] Teste de diferentes fontes de tráfego

## 🔍 Troubleshooting

### Erros Comuns e Soluções

#### 1. Erro 401 - Unauthorized
```
❌ Problema: Token UTMify inválido
✅ Solução: Verificar se o token está correto e usar header 'x-api-token'
```

#### 2. Erro 400 - Bad Request
```
❌ Problema: Payload com estrutura incorreta
✅ Solução: Seguir exatamente a estrutura da documentação oficial
```

#### 3. Webhook não recebido
```
❌ Problema: URL do webhook incorreta na Pushinpay
✅ Solução: Configurar URL pública no painel da Pushinpay
```

#### 4. Dados não aparecem no UTMify
```
❌ Problema: Parâmetros UTM não enviados corretamente
✅ Solução: Verificar se custom_data está sendo enviado no PIX
```

## 📊 Monitoramento

### Logs Importantes

```python
# Logs de sucesso
logging.info(f"✅ PIX criado: {pix_id} - Valor: R$ {valor}")
logging.info(f"📊 Webhook recebido: {transaction_id}")
logging.info(f"🎯 Conversão enviada para UTMify: {order_id}")

# Logs de erro
logging.error(f"❌ Erro ao criar PIX: {error}")
logging.error(f"❌ Erro no webhook: {error}")
logging.error(f"❌ Erro ao enviar para UTMify: {error}")
```

### Métricas para Acompanhar

- Taxa de sucesso de criação de PIX
- Taxa de sucesso de webhooks recebidos
- Taxa de sucesso de envio para UTMify
- Tempo de resposta das APIs
- Conversões por fonte de tráfego

## 🚀 Deploy em Produção

### Railway/Heroku

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export PUSHINPAY_TOKEN="seu_token"
export UTMIFY_API_KEY="seu_token"
export UTMIFY_API_URL="https://api.utmify.com.br/api-credentials/orders"
export WEBHOOK_SECRET="seu_secret"

# Executar aplicação
python integracao_utmify_pushinpay.py
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "integracao_utmify_pushinpay.py"]
```

---

## 📝 Resumo das Correções

1. **✅ URL da API corrigida**: `https://api.utmify.com.br/api-credentials/orders`
2. **✅ Header de autenticação correto**: `x-api-token`
3. **✅ Payload seguindo documentação oficial** da UTMify
4. **✅ Estrutura de dados completa** para tracking
5. **✅ Tratamento de erros aprimorado**
6. **✅ Logs detalhados** para monitoramento
7. **✅ Testes de integração** incluídos

Com essas correções, a integração UTMify + Pushinpay funcionará corretamente para rastreamento automático de vendas PIX com parâmetros UTM.