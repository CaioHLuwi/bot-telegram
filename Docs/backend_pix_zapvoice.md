# Backend PIX + ZapVoice - Documentação Completa

## 📋 Visão Geral

Este backend foi desenvolvido para integrar pagamentos PIX via Pushinpay com o sistema ZapVoice, permitindo:

- ✅ Geração automática de PIX com QR Code
- ✅ Recebimento de webhooks de pagamento
- ✅ Atualização automática de status no ZapVoice
- ✅ Consulta de status de pedidos
- ✅ Interface REST API completa

## 🏗️ Arquitetura

### Componentes Principais

1. **Flask API Server** - Servidor web principal
2. **PushinpayAPI** - Classe para integração com Pushinpay
3. **ZapVoiceAPI** - Classe para integração com ZapVoice
4. **Sistema de Webhooks** - Processamento de notificações
5. **Gerenciamento de Pedidos** - Controle de status e dados

### Fluxo de Funcionamento

```
1. Cliente solicita PIX → API cria PIX no Pushinpay
2. Pushinpay retorna QR Code → API retorna para cliente
3. Cliente paga PIX → Pushinpay envia webhook
4. API recebe webhook → Atualiza status no ZapVoice
5. Cliente pode consultar status → API retorna status atual
```

## 🚀 Instalação e Configuração

### 1. Dependências

```bash
pip install -r requirements_backend.txt
```

### 2. Configuração de Ambiente

Crie o arquivo `.env.backend` com as seguintes variáveis:

```env
# Pushinpay API
PUSHINPAY_API_KEY=sua_api_key_aqui
PUSHINPAY_SECRET_KEY=sua_secret_key_aqui
PUSHINPAY_BASE_URL=https://api.pushinpay.com.br

# ZapVoice API
ZAPVOICE_API_KEY=sua_zapvoice_api_key
ZAPVOICE_BASE_URL=https://api.zapvoice.com.br

# Webhook
WEBHOOK_SECRET_KEY=chave_secreta_webhook
WEBHOOK_BASE_URL=https://seudominio.com

# Servidor
PORT=5000
DEBUG=True
```

### 3. Executar o Servidor

```bash
python backend_pix_zapvoice.py
```

O servidor estará disponível em: `http://localhost:5000`

## 📡 Endpoints da API

### 1. Health Check

**GET** `/health`

Verifica se o servidor está funcionando.

**Resposta:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "pushinpay": "connected",
    "zapvoice": "connected"
  }
}
```

### 2. Criar PIX

**POST** `/pix/criar`

Cria um novo PIX e retorna QR Code.

**Parâmetros:**
```json
{
  "valor": 19.90,
  "nome_cliente": "João Silva",
  "descricao": "Pack Premium - 20 fotos + 5 vídeos",
  "cliente_info": {
    "phone": "11999999999",
    "email": "joao@email.com"
  },
  "produto_info": {
    "name": "Pack Premium",
    "type": "pack_premium"
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "pedido_id": "ped_123456789",
  "pix_id": "pix_987654321",
  "valor": 19.90,
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "pix_code": "00020126580014br.gov.bcb.pix...",
  "expires_at": "2024-01-15T11:30:00Z",
  "status": "pending"
}
```

### 3. Consultar Status

**GET** `/pix/status/{pedido_id}`

Consulta o status atual de um pedido.

**Resposta:**
```json
{
  "success": true,
  "pedido_id": "ped_123456789",
  "status": "paid",
  "valor": 19.90,
  "paid_at": "2024-01-15T10:45:00Z",
  "zapvoice_updated": true
}
```

### 4. Webhook Pushinpay

**POST** `/webhook/pushinpay`

Recebe notificações de pagamento do Pushinpay.

**Parâmetros (enviados pelo Pushinpay):**
```json
{
  "id": "pix_987654321",
  "status": "paid",
  "external_id": "ped_123456789",
  "amount": 19.90,
  "paid_at": "2024-01-15T10:45:00Z",
  "payer_name": "João Silva",
  "description": "Pack Premium"
}
```

### 5. Listar Pedidos

**GET** `/pedidos`

Lista todos os pedidos com paginação.

**Parâmetros de Query:**
- `page`: Página (padrão: 1)
- `limit`: Itens por página (padrão: 20)
- `status`: Filtrar por status

**Resposta:**
```json
{
  "success": true,
  "pedidos": [
    {
      "pedido_id": "ped_123456789",
      "valor": 19.90,
      "status": "paid",
      "created_at": "2024-01-15T10:30:00Z",
      "paid_at": "2024-01-15T10:45:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1
}
```

## 🔗 Integração ZapVoice

### Funcionalidades

1. **Atualização de Status**: Quando um PIX é pago, o status é automaticamente atualizado no ZapVoice
2. **Criação de Pedidos**: Novos pedidos são registrados no ZapVoice
3. **Sincronização**: Dados são mantidos sincronizados entre os sistemas

### Endpoints ZapVoice Utilizados

- `POST /orders` - Criar novo pedido
- `PUT /orders/{id}` - Atualizar status do pedido
- `GET /orders/{id}` - Consultar pedido

## 🔒 Segurança

### Autenticação

- **API Keys**: Todas as integrações usam chaves de API seguras
- **Webhook Secret**: Webhooks são validados com chave secreta
- **HTTPS**: Recomendado para produção

### Validação

- **Dados de Entrada**: Todos os dados são validados com Marshmallow
- **Tipos de Dados**: Validação rigorosa de tipos e formatos
- **Sanitização**: Dados são sanitizados antes do processamento

## 📊 Monitoramento e Logs

### Sistema de Logs

```python
# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas Disponíveis

- Total de PIX criados
- Taxa de conversão de pagamentos
- Tempo médio de processamento
- Erros de integração

## 🧪 Testes

### Script de Teste Automatizado

```bash
python test_backend.py
```

### Testes Incluídos

1. ✅ Health Check
2. ✅ Criação de PIX
3. ✅ Consulta de Status
4. ✅ Simulação de Webhook
5. ✅ Integração ZapVoice
6. ✅ Listagem de Pedidos

### Exemplo de Teste Manual

```bash
# 1. Criar PIX
curl -X POST http://localhost:5000/pix/criar \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 19.90,
    "nome_cliente": "Teste",
    "descricao": "Pack Teste"
  }'

# 2. Consultar Status
curl http://localhost:5000/pix/status/ped_123456789
```

## 🚀 Deploy em Produção

### 1. Configuração do Servidor

```bash
# Instalar dependências
pip install -r requirements_backend.txt

# Configurar variáveis de ambiente
cp .env.backend.example .env.backend
# Editar .env.backend com dados reais

# Executar com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend_pix_zapvoice:app
```

### 2. Nginx (Proxy Reverso)

```nginx
server {
    listen 80;
    server_name seudominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL/HTTPS

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seudominio.com
```

## 🔧 Configuração de Webhook

### No Pushinpay

1. Acesse o painel do Pushinpay
2. Vá em "Configurações" → "Webhooks"
3. Adicione a URL: `https://seudominio.com/webhook/pushinpay`
4. Configure os eventos: `payment.paid`, `payment.failed`

### Teste de Webhook

```bash
# Simular webhook
curl -X POST http://localhost:5000/webhook/pushinpay \
  -H "Content-Type: application/json" \
  -d '{
    "id": "pix_test",
    "status": "paid",
    "external_id": "ped_123",
    "amount": 19.90
  }'
```

## 📈 Otimizações

### Performance

1. **Cache Redis**: Para consultas frequentes
2. **Pool de Conexões**: Para requests HTTP
3. **Async Processing**: Para webhooks
4. **Database Indexing**: Para consultas rápidas

### Escalabilidade

1. **Load Balancer**: Múltiplas instâncias
2. **Database Clustering**: Para alta disponibilidade
3. **CDN**: Para assets estáticos
4. **Monitoring**: APM e alertas

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Pushinpay
```
Erro: Connection timeout
Solução: Verificar API_KEY e conectividade
```

#### 2. Webhook não Recebido
```
Erro: Webhook não processado
Solução: Verificar URL e configuração no Pushinpay
```

#### 3. ZapVoice não Atualiza
```
Erro: ZapVoice API error
Solução: Verificar credenciais e endpoint
```

### Logs de Debug

```bash
# Ativar logs detalhados
export DEBUG=True
python backend_pix_zapvoice.py

# Verificar logs
tail -f backend.log
```

## 📞 Suporte

### Contatos

- **Desenvolvedor**: Equipe Backend
- **Email**: suporte@seudominio.com
- **Documentação**: https://docs.seudominio.com

### Recursos Adicionais

- [Documentação Pushinpay](https://docs.pushinpay.com.br)
- [Documentação ZapVoice](https://docs.zapvoice.com.br)
- [Flask Documentation](https://flask.palletsprojects.com)

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2024  
**Status**: ✅ Produção