# 🚀 Backend PIX + ZapVoice

## 📋 Visão Geral para Leigos

Este backend é como um "intermediário inteligente" que:

1. **Recebe pedidos** de pagamento PIX
2. **Gera QR Codes** automaticamente
3. **Monitora pagamentos** em tempo real
4. **Atualiza sistemas** quando o pagamento é confirmado

### 🎯 Para que serve?

- ✅ **Automatizar vendas**: Cliente paga PIX e recebe produto automaticamente
- ✅ **Integrar sistemas**: Conecta Pushinpay (pagamentos) com ZapVoice (entregas)
- ✅ **Monitorar vendas**: Acompanha todos os pagamentos em tempo real
- ✅ **Facilitar gestão**: Interface simples para consultar pedidos

## 🏗️ Como Funciona?

```
👤 Cliente → 💰 Solicita PIX → 🤖 Backend → 📱 Gera QR Code
                                    ↓
💳 Cliente Paga → 🔔 Pushinpay Notifica → 🤖 Backend → 📦 ZapVoice Entrega
```

## 🚀 Instalação Rápida

### 1. Pré-requisitos

- Python 3.8 ou superior
- Conta no Pushinpay
- Conta no ZapVoice (opcional)

### 2. Configuração

```bash
# 1. Instalar dependências
pip install -r requirements_backend.txt

# 2. Configurar variáveis de ambiente
# Copie .env.backend e preencha com seus dados

# 3. Executar servidor
python backend_pix_zapvoice.py
```

### 3. Testar Funcionamento

```bash
# Executar testes automáticos
python test_backend.py
```

## 🔧 Configuração Detalhada

### Arquivo `.env.backend`

```env
# 🔑 Pushinpay (Obrigatório)
PUSHINPAY_API_KEY=sua_chave_api_pushinpay
PUSHINPAY_SECRET_KEY=sua_chave_secreta_pushinpay

# 📱 ZapVoice (Opcional)
ZAPVOICE_API_KEY=sua_chave_zapvoice

# 🌐 Servidor
PORT=5000
DEBUG=True
```

### Como Obter as Chaves?

#### Pushinpay:
1. Acesse [Pushinpay](https://pushinpay.com.br)
2. Faça login na sua conta
3. Vá em "Configurações" → "API"
4. Copie sua API Key e Secret Key

#### ZapVoice:
1. Acesse [ZapVoice](https://zapvoice.com.br)
2. Faça login na sua conta
3. Vá em "Integrações" → "API"
4. Gere uma nova chave de API

## 📡 Como Usar a API

### 1. Criar um PIX

**Endpoint**: `POST /pix/criar`

```javascript
// Exemplo em JavaScript
fetch('http://localhost:5000/pix/criar', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    valor: 19.90,
    nome_cliente: 'João Silva',
    descricao: 'Pack Premium - 20 fotos + 5 vídeos'
  })
})
.then(response => response.json())
.then(data => {
  console.log('PIX criado:', data.qr_code);
});
```

### 2. Consultar Status

**Endpoint**: `GET /pix/status/{pedido_id}`

```javascript
// Verificar se foi pago
fetch('http://localhost:5000/pix/status/ped_123456')
.then(response => response.json())
.then(data => {
  if (data.status === 'paid') {
    console.log('Pagamento confirmado!');
  }
});
```

### 3. Listar Todos os Pedidos

**Endpoint**: `GET /pedidos`

```javascript
// Ver todos os pedidos
fetch('http://localhost:5000/pedidos')
.then(response => response.json())
.then(data => {
  console.log('Total de pedidos:', data.total);
});
```

## 🎨 Interface Web (Exemplo)

Incluímos um arquivo `frontend_exemplo.html` que mostra como usar o backend:

1. Abra `frontend_exemplo.html` no navegador
2. Preencha os dados do cliente
3. Clique em "Gerar PIX"
4. Escaneie o QR Code ou copie o código PIX
5. Acompanhe o status em tempo real

## 🔔 Configurar Webhooks

### No Pushinpay

1. Acesse o painel do Pushinpay
2. Vá em "Configurações" → "Webhooks"
3. Adicione a URL: `https://seusite.com/webhook/pushinpay`
4. Selecione os eventos: "Pagamento Aprovado" e "Pagamento Rejeitado"

### Testar Webhook Localmente

Para testar em desenvolvimento, use [ngrok](https://ngrok.com):

```bash
# 1. Instalar ngrok
# 2. Expor servidor local
ngrok http 5000

# 3. Usar URL do ngrok no Pushinpay
# Exemplo: https://abc123.ngrok.io/webhook/pushinpay
```

## 📊 Monitoramento

### Logs do Sistema

O backend gera logs automáticos em `backend.log`:

```bash
# Ver logs em tempo real
tail -f backend.log
```

### Métricas Importantes

- **PIX Criados**: Quantos PIX foram gerados
- **Taxa de Conversão**: % de PIX que foram pagos
- **Tempo de Resposta**: Velocidade da API
- **Erros**: Problemas de integração

## 🚀 Deploy em Produção

### Opção 1: Servidor Próprio

```bash
# 1. Servidor Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip nginx

# 2. Instalar aplicação
git clone seu-repositorio
cd bot-packs
pip3 install -r requirements_backend.txt

# 3. Configurar Nginx
sudo nano /etc/nginx/sites-available/backend

# 4. Executar com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend_pix_zapvoice:app
```

### Opção 2: Heroku

```bash
# 1. Instalar Heroku CLI
# 2. Fazer deploy
heroku create seu-app-backend
git push heroku main
heroku config:set PUSHINPAY_API_KEY=sua_chave
```

### Opção 3: DigitalOcean/AWS

1. Criar droplet/instância
2. Instalar Docker
3. Usar docker-compose (arquivo incluído)

## 🐛 Problemas Comuns

### ❌ "Servidor não responde"

**Solução**:
```bash
# Verificar se está rodando
ps aux | grep python

# Reiniciar servidor
python backend_pix_zapvoice.py
```

### ❌ "PIX não é criado"

**Possíveis causas**:
- API Key do Pushinpay incorreta
- Saldo insuficiente na conta Pushinpay
- Problemas de conectividade

**Solução**:
```bash
# Verificar logs
tail -f backend.log

# Testar conexão
curl http://localhost:5000/health
```

### ❌ "Webhook não funciona"

**Solução**:
1. Verificar URL no painel Pushinpay
2. Testar com ngrok em desenvolvimento
3. Verificar logs de webhook

## 📞 Suporte

### Documentação Completa

Veja `Docs/backend_pix_zapvoice.md` para documentação técnica detalhada.

### Testes Automáticos

```bash
# Executar todos os testes
python test_backend.py

# Ver relatório detalhado
cat test_report.json
```

### Contato

- **Issues**: Abra uma issue no GitHub
- **Email**: suporte@seudominio.com
- **Documentação**: Pasta `Docs/`

## 🎯 Próximos Passos

1. ✅ **Configurar ambiente** - Seguir este README
2. ✅ **Testar localmente** - Usar `test_backend.py`
3. ✅ **Integrar com bot** - Conectar com seu bot existente
4. ✅ **Deploy produção** - Escolher uma opção de deploy
5. ✅ **Monitorar** - Acompanhar logs e métricas

---

**🚀 Pronto para começar?**

1. Configure o `.env.backend`
2. Execute `python backend_pix_zapvoice.py`
3. Teste com `python test_backend.py`
4. Abra `frontend_exemplo.html` para ver funcionando!

**Versão**: 1.0.0  
**Compatibilidade**: Python 3.8+  
**Status**: ✅ Pronto para produção