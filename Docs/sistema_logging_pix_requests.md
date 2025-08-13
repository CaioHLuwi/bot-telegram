# Sistema de Logging PIX Requests - Documentação Completa

## 📋 Visão Geral

O Sistema de Logging PIX Requests é uma solução completa para registrar e monitorar todas as solicitações de PIX, webhooks da Pushinpay e integrações com UTMify. O sistema captura automaticamente todos os parâmetros relevantes e os armazena em formato JSON para análise posterior.

## 🎯 Funcionalidades Principais

### 1. **Logging Automático de PIX**
- Registra todas as solicitações de PIX com parâmetros UTM
- Captura dados do usuário, valor, descrição e resposta da Pushinpay
- Mede tempo de processamento em milissegundos
- Registra erros e exceções com detalhes

### 2. **Logging de Webhooks**
- Registra todos os webhooks recebidos da Pushinpay
- Captura dados de pagamento e status
- Registra tentativas de envio para UTMify
- Armazena respostas da UTMify

### 3. **Estatísticas e Relatórios**
- Contagem por status (success, error, pending)
- Análise por fonte UTM
- Valor total processado
- Relatórios por data e período

## 📁 Estrutura de Arquivos

```
bot-packs/
├── Logs/
│   └── pix_requests_log.json          # Arquivo principal de logs
├── logger_pix_requests.py              # Classe de logging
├── integracao_utmify_pushinpay.py     # Integração com logging
└── Docs/
    └── sistema_logging_pix_requests.md # Esta documentação
```

## 🔧 Configuração

### Pré-requisitos

```python
# Dependências necessárias
import json
import os
from datetime import datetime
import uuid
from typing import Dict, Any, Optional
```

### Inicialização

```python
from logger_pix_requests import PixRequestLogger

# Inicializa o logger
pix_logger = PixRequestLogger()

# Ou com caminho customizado
pix_logger = PixRequestLogger("custom_path/logs.json")
```

## 📊 Estrutura do JSON de Logs

### Arquivo Principal: `pix_requests_log.json`

```json
{
  "pix_requests": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "request_id": "req_123456789",
      "user_info": {
        "telegram_id": "123456789",
        "username": "@usuario",
        "email": "usuario@email.com",
        "phone": "+5511999999999"
      },
      "pix_data": {
        "valor_reais": 97.00,
        "descricao": "Pack Premium",
        "payment_id": "pix_abc123",
        "qr_code": "00020126580014BR.GOV.BCB.PIX...",
        "expires_at": "2024-01-01T12:30:00Z"
      },
      "utm_params": {
        "utm_source": "telegram",
        "utm_medium": "bot",
        "utm_campaign": "black_friday_2024",
        "utm_content": "pack_premium",
        "utm_term": "oferta_especial"
      },
      "pushinpay_response": {
        "success": true,
        "payment_id": "pix_abc123",
        "qr_code": "00020126580014BR.GOV.BCB.PIX...",
        "amount": 97.00,
        "status": "pending"
      },
      "utmify_data": {
        "order_id": "pix_abc123",
        "total_value": 97.00,
        "status": "pending"
      },
      "status": "success",
      "errors": [],
      "processing_time_ms": 1250
    }
  ],
  "webhooks": [
    {
      "timestamp": "2024-01-01T12:05:00Z",
      "webhook_id": "webhook_987654321",
      "type": "webhook_received",
      "payment_id": "pix_abc123",
      "webhook_data": {
        "status": "paid",
        "amount": 97.00,
        "payment_id": "pix_abc123"
      },
      "utm_params": {
        "utm_source": "telegram",
        "utm_medium": "bot"
      },
      "utmify_sent": true,
      "utmify_response": {
        "success": true,
        "message": "Conversão enviada com sucesso"
      },
      "status": "processed"
    }
  ],
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "description": "Log de PIX requests e webhooks",
    "version": "1.0"
  }
}
```

## 🚀 Uso Prático

### 1. Logging de Solicitação PIX

```python
# Exemplo de uso na função gerar_pix_com_utm
def gerar_pix_com_utm(valor_reais, descricao, email, utm_params, user_info=None):
    start_time = time.time()
    
    try:
        # ... código da API Pushinpay ...
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            result = response.json()
            
            # Log automático da solicitação
            pix_logger.log_pix_request(
                user_info=user_info or {"email": email},
                pix_data={
                    "valor_reais": valor_reais,
                    "descricao": descricao,
                    "payment_id": result.get('payment_id'),
                    "qr_code": result.get('qr_code')
                },
                utm_params=utm_params,
                pushinpay_response=result,
                status="success",
                processing_time_ms=processing_time_ms
            )
            
            return result
    except Exception as e:
        # Log automático de erros
        pix_logger.log_pix_request(
            user_info=user_info,
            pix_data={"valor_reais": valor_reais, "descricao": descricao},
            utm_params=utm_params,
            pushinpay_response={"error": str(e)},
            status="error",
            errors=[str(e)],
            processing_time_ms=processing_time_ms
        )
```

### 2. Logging de Webhooks

```python
# Exemplo de uso no webhook da Pushinpay
@app.route('/webhook/pushinpay', methods=['POST'])
def webhook_pushinpay():
    try:
        data = request.get_json()
        
        # ... processamento do webhook ...
        
        # Log automático do webhook
        pix_logger.log_webhook_received(
            webhook_data=data,
            payment_id=payment_id,
            utm_params=utm_params,
            utmify_sent=result['success'],
            utmify_response=result
        )
        
    except Exception as e:
        # Log de erros no webhook
        pix_logger.log_webhook_received(
            webhook_data=request.get_json() or {},
            payment_id="unknown",
            utm_params={},
            utmify_sent=False,
            utmify_response={"error": str(e)}
        )
```

## 📈 Endpoints de Monitoramento

### 1. Estatísticas Gerais
```http
GET /logs/stats
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "total_requests": 150,
    "total_webhooks": 120,
    "status_count": {
      "success": 140,
      "error": 8,
      "pending": 2
    },
    "utm_sources": {
      "telegram": 100,
      "instagram": 30,
      "facebook": 20
    },
    "total_value": 14550.00
  },
  "timestamp": "2024-01-01T15:30:00Z"
}
```

### 2. Logs por Data
```http
GET /logs/date/2024-01-01
```

**Resposta:**
```json
{
  "success": true,
  "date": "2024-01-01",
  "count": 25,
  "data": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "request_id": "req_123456789",
      "status": "success",
      "pix_data": {
        "valor_reais": 97.00,
        "payment_id": "pix_abc123"
      }
    }
  ]
}
```

### 3. Logs por Status
```http
GET /logs/status/error
```

**Resposta:**
```json
{
  "success": true,
  "status": "error",
  "count": 8,
  "data": [
    {
      "timestamp": "2024-01-01T14:30:00Z",
      "request_id": "req_error123",
      "status": "error",
      "errors": ["HTTP 400: Invalid email format"],
      "processing_time_ms": 500
    }
  ]
}
```

## 🔍 Métodos da Classe PixRequestLogger

### `log_pix_request()`
Registra uma solicitação de PIX com todos os parâmetros.

**Parâmetros:**
- `user_info`: Informações do usuário
- `pix_data`: Dados do PIX (valor, descrição, etc.)
- `utm_params`: Parâmetros UTM
- `pushinpay_response`: Resposta da API Pushinpay
- `utmify_data`: Dados para UTMify (opcional)
- `status`: Status da operação
- `errors`: Lista de erros (opcional)
- `processing_time_ms`: Tempo de processamento

### `log_webhook_received()`
Registra o recebimento de um webhook da Pushinpay.

**Parâmetros:**
- `webhook_data`: Dados completos do webhook
- `payment_id`: ID do pagamento
- `utm_params`: Parâmetros UTM extraídos
- `utmify_sent`: Se foi enviado para UTMify
- `utmify_response`: Resposta da UTMify

### `get_logs_by_date(date_str)`
Recupera logs de uma data específica (formato: YYYY-MM-DD).

### `get_logs_by_status(status)`
Recupera logs por status (success, error, pending).

### `get_statistics()`
Retorna estatísticas completas dos logs.

## 📊 Análise e Relatórios

### Exemplo de Script de Análise

```python
from logger_pix_requests import PixRequestLogger
from datetime import datetime, timedelta

logger = PixRequestLogger()

# Estatísticas gerais
stats = logger.get_statistics()
print(f"Total de requests: {stats['total_requests']}")
print(f"Taxa de sucesso: {stats['status_count'].get('success', 0) / stats['total_requests'] * 100:.2f}%")
print(f"Valor total: R$ {stats['total_value']:.2f}")

# Logs de hoje
today = datetime.now().strftime('%Y-%m-%d')
today_logs = logger.get_logs_by_date(today)
print(f"PIX requests hoje: {len(today_logs)}")

# Logs com erro
error_logs = logger.get_logs_by_status('error')
print(f"Requests com erro: {len(error_logs)}")

# Análise por fonte UTM
for source, count in stats['utm_sources'].items():
    print(f"Fonte {source}: {count} requests")
```

## 🛠️ Manutenção e Backup

### Rotação de Logs

```python
import shutil
from datetime import datetime

def backup_logs():
    """Cria backup dos logs com timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"Logs/backup/pix_requests_log_{timestamp}.json"
    
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy("Logs/pix_requests_log.json", backup_path)
    
    print(f"Backup criado: {backup_path}")

# Executar backup diário
backup_logs()
```

### Limpeza de Logs Antigos

```python
def clean_old_logs(days_to_keep=30):
    """Remove logs mais antigos que X dias"""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    with open("Logs/pix_requests_log.json", 'r') as f:
        data = json.load(f)
    
    # Filtra requests recentes
    recent_requests = []
    for request in data.get('pix_requests', []):
        request_date = datetime.fromisoformat(request['timestamp'].replace('Z', '+00:00'))
        if request_date > cutoff_date:
            recent_requests.append(request)
    
    data['pix_requests'] = recent_requests
    
    with open("Logs/pix_requests_log.json", 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Logs limpos. Mantidos: {len(recent_requests)} requests")
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Arquivo de log não encontrado**
   - O sistema cria automaticamente o arquivo na primeira execução
   - Verifique permissões da pasta `Logs/`

2. **JSON corrompido**
   - Faça backup antes de modificações
   - Use `json.loads()` para validar estrutura

3. **Performance com muitos logs**
   - Implemente rotação de logs
   - Use índices para consultas frequentes

4. **Espaço em disco**
   - Configure limpeza automática
   - Comprima logs antigos

### Monitoramento de Saúde

```python
def check_log_health():
    """Verifica saúde do sistema de logs"""
    try:
        logger = PixRequestLogger()
        stats = logger.get_statistics()
        
        # Verifica se há logs recentes
        today_logs = logger.get_logs_by_date(datetime.now().strftime('%Y-%m-%d'))
        
        health = {
            "status": "healthy",
            "total_requests": stats.get('total_requests', 0),
            "today_requests": len(today_logs),
            "error_rate": stats.get('status_count', {}).get('error', 0) / max(stats.get('total_requests', 1), 1) * 100
        }
        
        if health["error_rate"] > 10:  # Mais de 10% de erro
            health["status"] = "warning"
            health["message"] = "Taxa de erro elevada"
        
        return health
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
```

## 📋 Checklist de Implementação

- [ ] ✅ Arquivo `logger_pix_requests.py` criado
- [ ] ✅ Pasta `Logs/` criada
- [ ] ✅ Integração com `integracao_utmify_pushinpay.py`
- [ ] ✅ Endpoints de monitoramento implementados
- [ ] ✅ Logging de PIX requests ativo
- [ ] ✅ Logging de webhooks ativo
- [ ] ✅ Documentação completa
- [ ] 🔄 Testes de funcionamento
- [ ] 🔄 Configuração de backup automático
- [ ] 🔄 Monitoramento em produção

## 🎯 Próximos Passos

1. **Implementar Dashboard Web**
   - Interface visual para análise de logs
   - Gráficos de performance e conversão
   - Alertas em tempo real

2. **Integração com Ferramentas de Monitoramento**
   - Prometheus/Grafana
   - Alertas via Telegram/Email
   - Métricas customizadas

3. **Análise Avançada**
   - Machine Learning para detecção de anomalias
   - Previsão de conversões
   - Otimização de campanhas UTM

---

**Sistema de Logging PIX Requests** - Versão 1.0  
*Documentação atualizada em: Janeiro 2024*  
*Desenvolvido para integração UTMify + Pushinpay + Bot Telegram*