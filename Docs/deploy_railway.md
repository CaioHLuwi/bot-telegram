# Deploy no Railway - Guia Completo

## 🚂 Configuração para Railway

### Problema Comum
**Erro**: `python: can't open file '/app/main.py': [Errno 2] No such file or directory`

**Causa**: O Railway por padrão procura por `main.py`, mas nosso arquivo principal é `bot.py`.

### ✅ Solução Implementada

Foram criados os seguintes arquivos de configuração:

#### 1. `Procfile`
```
web: python bot.py
```
- Especifica que o comando de inicialização é `python bot.py`

#### 2. `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- Configuração específica do Railway
- Define comando de inicialização
- Política de restart em caso de falha

#### 3. `runtime.txt`
```
python-3.11
```
- Especifica a versão do Python a ser usada

## 🚀 Passo a Passo para Deploy

### 1. Preparar Variáveis de Ambiente
No painel do Railway, configure as variáveis:

```bash
BOT_TOKEN=seu_token_aqui
CONTEUDO_LINK=seu_link_aqui
MERCADO_PAGO_ACCESS_TOKEN=seu_token_mp_aqui
```

### 2. Fazer Deploy
1. **Conecte seu repositório** ao Railway
2. **Faça push** dos arquivos de configuração
3. **Railway detectará** automaticamente as configurações
4. **Deploy será executado** com `python bot.py`

### 3. Verificar Logs
Após o deploy, verifique os logs:
- ✅ `Bot iniciado!`
- ✅ `Application started`
- ✅ Requisições HTTP para Telegram API

## 🔧 Configurações Importantes

### Variáveis de Ambiente Obrigatórias
```bash
# Token do bot do Telegram
BOT_TOKEN=8348887234:AAF0d2gLAE0KX3x-H5Iq-8mTxONhegNJ27Y

# Link do conteúdo a ser enviado
CONTEUDO_LINK=https://seu-site.com/conteudo

# Token do Mercado Pago (opcional)
MERCADO_PAGO_ACCESS_TOKEN=seu_token_aqui
```

### Arquivos Necessários
- ✅ `bot.py` - Arquivo principal
- ✅ `requirements.txt` - Dependências
- ✅ `Procfile` - Comando de inicialização
- ✅ `railway.json` - Configuração do Railway
- ✅ `runtime.txt` - Versão do Python
- ✅ `.env` - Variáveis locais (não fazer upload)

## 🐛 Solução de Problemas

### Erro: "No such file or directory"
**Solução**: Verifique se os arquivos `Procfile` e `railway.json` estão no repositório.

### Erro: "Module not found"
**Solução**: Verifique se `requirements.txt` está correto:
```txt
python-telegram-bot==20.3
requests==2.31.0
aiofiles==23.2.1
python-dotenv==1.0.0
```

### Bot não responde
**Verificações**:
1. ✅ `BOT_TOKEN` está correto
2. ✅ Bot está ativo no @BotFather
3. ✅ Logs mostram "Application started"
4. ✅ Não há conflito com outras instâncias

### Erro de Webhook
**Solução**: O bot usa polling, não webhook. Isso é normal.

## 📊 Monitoramento

### Logs Importantes
```bash
# Inicialização bem-sucedida
2025-01-26 10:00:00 - __main__ - INFO - Bot iniciado!
2025-01-26 10:00:01 - telegram.ext.Application - INFO - Application started

# Atividade normal
2025-01-26 10:00:02 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot.../getUpdates
2025-01-26 10:00:03 - metrics - INFO - Usuário 123456 iniciou conversa
```

### Comandos de Teste
Após deploy, teste:
- `/start` - Iniciar conversa
- `/oi` - Iniciar conversa
- `/metricas` - Ver estatísticas

## 💰 Custos Railway

### Plano Gratuito
- **$5 de crédito** por mês
- **500 horas** de execução
- Suficiente para bots pequenos

### Plano Pago
- **$5/mês** por serviço
- Execução ilimitada
- Melhor para produção

## 🔒 Segurança

### Boas Práticas
1. **Nunca commite** o arquivo `.env`
2. **Use variáveis de ambiente** no Railway
3. **Mantenha tokens seguros**
4. **Monitore logs** regularmente

### Arquivo .gitignore
```
.env
__pycache__/
*.pyc
bot_metrics.json
```

## 📈 Otimizações

### Para Melhor Performance
1. **Use webhook** em vez de polling (produção)
2. **Configure health checks**
3. **Monitore uso de recursos**
4. **Implemente rate limiting**

---

**✅ Com essas configurações, seu bot funcionará perfeitamente no Railway!**