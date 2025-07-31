# Integração Utmify + Pushinpay - Guia Completo

## 📋 Visão Geral

Este documento fornece um guia completo para integrar a **Utmify** (plataforma de tracking de UTM) com a **Pushinpay** (gateway de pagamento PIX) para rastrear vendas e campanhas de marketing.

## 🎯 Objetivo

Permitir o rastreamento preciso de conversões de vendas PIX, associando cada transação aos parâmetros UTM da campanha de marketing que a originou.

## 🏗️ Arquitetura da Solução

```
[Campanha Marketing] → [Link com UTMs] → [Página de Vendas] → [Gerar PIX] → [Pagamento] → [Webhook] → [Utmify]
```

### Componentes:

1. **Pushinpay API** - Gera PIX com dados UTM
2. **Sistema Intermediário** - Recebe webhooks e processa dados
3. **Utmify API** - Recebe dados de conversão

## 📁 Arquivos do Projeto

### Arquivos Principais

- **`integracao_utmify_pushinpay.py`** - Script principal da integração
- **`.env.integracao`** - Configurações de ambiente
- **`requirements_integracao.txt`** - Dependências Python

### Estrutura de Pastas

```
bot-packs/
├── integracao_utmify_pushinpay.py
├── .env.integracao
├── requirements_integracao.txt
└── Docs/
    └── integracao_utmify_pushinpay_completa.md
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.8+
- Conta na Pushinpay com API ativa
- Conta na Utmify com API ativa
- Servidor com HTTPS para receber webhooks

### 2. Instalação

```bash
# Clonar ou baixar os arquivos
cd bot-packs

# Instalar dependências
pip install -r requirements_integracao.txt

# Configurar ambiente
cp .env.integracao .env
```

### 3. Configuração das Credenciais

Edite o arquivo `.env` com suas credenciais:

```env
# Pushinpay
PUSHINPAY_TOKEN=pk_live_sua_chave_aqui
PUSHINPAY_API_URL=https://api.pushinpay.com.br/api

# Utmify
UTMIFY_API_KEY=utm_sk_sua_chave_aqui
UTMIFY_API_URL=https://api.utmify.com/v1

# Webhook
WEBHOOK_SECRET=sua_chave_secreta_webhook
```

### 4. Configuração nos Painéis

#### Pushinpay:
1. Acesse o painel da Pushinpay
2. Vá em **Configurações > Webhooks**
3. Configure a URL: `https://seu-dominio.com/webhook/pushinpay`
4. Copie o token de API

#### Utmify:
1. Acesse o painel da Utmify
2. Vá em **Configurações > API**
3. Gere uma chave de API
4. Configure os eventos de conversão

## 🔧 Como Usar

### 1. Executar o Servidor

**Desenvolvimento:**
```bash
python integracao_utmify_pushinpay.py
```

**Produção:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 integracao_utmify_pushinpay:app
```

### 2. Gerar PIX com UTMs

```python
# Exemplo de uso da função
utm_params = {
    'utm_source': 'facebook',
    'utm_medium': 'cpc',
    'utm_campaign': 'black_friday_2024',
    'utm_content': 'anuncio_produto_x',
    'utm_term': 'comprar_agora'
}

resultado = gerar_pix_com_utm(
    valor=99.90,
    email='cliente@exemplo.com',
    utm_params=utm_params
)
```

### 3. Testar a Integração

```bash
# Teste básico
curl -X POST http://localhost:5000/webhook/test

# Verificar saúde
curl http://localhost:5000/health
```

## 📊 Endpoints da API

### GET `/`
**Descrição:** Informações da API
**Resposta:**
```json
{
  "name": "Integração Utmify + Pushinpay",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### GET `/health`
**Descrição:** Verificação de saúde
**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### POST `/webhook/pushinpay`
**Descrição:** Recebe webhooks da Pushinpay
**Headers:**
- `Content-Type: application/json`
- `X-Signature: sha256_hash` (opcional)

**Body:**
```json
{
  "event": "payment.approved",
  "transaction_id": "txn_123456",
  "amount": 99.90,
  "status": "approved",
  "customer_email": "cliente@exemplo.com",
  "custom_data": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "black_friday"
  }
}
```

### POST `/webhook/test`
**Descrição:** Testa a integração com dados fictícios
**Resposta:**
```json
{
  "status": "success",
  "test_data": {...},
  "conversion_data": {...},
  "utmify_success": true
}
```

## 🔄 Fluxo de Dados

### 1. Geração do PIX
```
Usuário clica no link → Página captura UTMs → Gera PIX com custom_data
```

### 2. Pagamento
```
Cliente paga PIX → Pushinpay processa → Envia webhook
```

### 3. Tracking
```
Webhook recebido → Dados processados → Enviado para Utmify
```

## 📈 Estrutura de Dados

### Dados Enviados para Utmify

```json
{
  "event": "conversion",
  "transaction_id": "txn_123456",
  "value": 99.90,
  "currency": "BRL",
  "payment_method": "pix",
  "attribution": {
    "utm_source": "facebook",
    "utm_medium": "cpc",
    "utm_campaign": "black_friday_2024",
    "utm_content": "anuncio_produto_x",
    "utm_term": "comprar_agora"
  },
  "customer": {
    "email": "cliente@exemplo.com",
    "id": "customer_123"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔒 Segurança

### Validação de Webhooks

```python
# Validação HMAC SHA256
expected_signature = hmac.new(
    webhook_secret.encode('utf-8'),
    payload.encode('utf-8'),
    hashlib.sha256
).hexdigest()
```

### Boas Práticas

- ✅ Use HTTPS em produção
- ✅ Valide assinaturas de webhook
- ✅ Mantenha logs detalhados
- ✅ Configure rate limiting
- ✅ Use variáveis de ambiente para credenciais
- ✅ Implemente retry logic

## 📝 Logs e Monitoramento

### Configuração de Logs

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Eventos Logados

- ✅ Webhooks recebidos
- ✅ Conversões processadas
- ✅ Erros de API
- ✅ Validações de segurança

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Webhook não recebido
**Causa:** URL incorreta ou servidor offline
**Solução:**
- Verificar URL no painel da Pushinpay
- Testar conectividade: `curl https://seu-dominio.com/health`

#### 2. Erro 401 na Utmify
**Causa:** API key inválida
**Solução:**
- Verificar `UTMIFY_API_KEY` no `.env`
- Regenerar chave no painel da Utmify

#### 3. UTMs não aparecem
**Causa:** custom_data não enviado corretamente
**Solução:**
- Verificar se UTMs estão no `custom_data` do PIX
- Testar com `/webhook/test`

### Debug

```bash
# Ativar logs detalhados
export LOG_LEVEL=DEBUG
python integracao_utmify_pushinpay.py

# Testar webhook manualmente
curl -X POST http://localhost:5000/webhook/test -v
```

## 📊 Métricas e Analytics

### KPIs Rastreados

- 💰 **Receita por Campanha**
- 📈 **Taxa de Conversão por UTM**
- 🎯 **ROI por Fonte de Tráfego**
- 📱 **Performance por Dispositivo**
- 🕐 **Tempo até Conversão**

### Relatórios Disponíveis

1. **Dashboard Utmify** - Visão geral das conversões
2. **Relatório de Campanhas** - Performance por UTM
3. **Análise de Funil** - Jornada do cliente
4. **Comparativo Temporal** - Evolução das métricas

## 🚀 Deploy em Produção

### Opções de Hospedagem

#### 1. Railway
```bash
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn integracao_utmify_pushinpay:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Heroku
```bash
# Procfile
web: gunicorn integracao_utmify_pushinpay:app
```

#### 3. VPS/Cloud
```bash
# Usando systemd
sudo systemctl enable utmify-integration
sudo systemctl start utmify-integration
```

### Variáveis de Ambiente

```bash
# Configurar no painel de hospedagem
PUSHINPAY_TOKEN=pk_live_...
UTMIFY_API_KEY=utm_sk_...
WEBHOOK_SECRET=...
ENVIRONMENT=production
```

## 📚 Recursos Adicionais

### Documentação Oficial

- [Pushinpay API Docs](https://docs.pushinpay.com.br)
- [Utmify API Docs](https://docs.utmify.com)
- [Flask Documentation](https://flask.palletsprojects.com)

### Ferramentas Úteis

- **Postman** - Testar APIs
- **ngrok** - Túnel para desenvolvimento
- **Sentry** - Monitoramento de erros
- **DataDog** - Métricas e logs

## ❓ FAQ

### P: Preciso de um servidor dedicado?
**R:** Não, pode usar serviços como Railway, Heroku ou Vercel.

### P: Como testar sem pagamentos reais?
**R:** Use o endpoint `/webhook/test` para simular conversões.

### P: Posso usar com outros gateways?
**R:** Sim, adapte a classe `PushinpayWebhook` para outros provedores.

### P: Os dados são enviados em tempo real?
**R:** Sim, assim que o webhook é recebido da Pushinpay.

### P: Como garantir que não perca conversões?
**R:** Implemente retry logic e monitore os logs.

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs da aplicação
2. Teste com `/webhook/test`
3. Consulte a documentação das APIs
4. Entre em contato com o suporte técnico

---

**Desenvolvido por:** Kyoko Bot  
**Versão:** 1.0.0  
**Data:** 2024  
**Licença:** MIT