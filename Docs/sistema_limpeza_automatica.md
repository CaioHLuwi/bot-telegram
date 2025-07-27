# Sistema de Limpeza Automática de Mensagens

## Visão Geral

Este documento explica o sistema de limpeza automática de mensagens implementado no bot Kyoko, que remove automaticamente mensagens indesejadas do grupo, mantendo apenas as mensagens da "Leticia Kyoko" e do próprio bot.

## Funcionalidades Implementadas

### 🧹 Limpeza Automática (A cada 5 minutos)

O bot executa uma limpeza automática a cada 5 minutos, removendo:

- **Mensagens de entrada de membros**: "João entrou no grupo"
- **Mensagens de saída de membros**: "Maria saiu do grupo" 
- **Notificações do grupo**:
  - Mudanças no nome do grupo
  - Alterações na foto do grupo
  - Remoção da foto do grupo
  - Mensagens fixadas
  - Criação de grupos/supergrupos
  - Migrações de chat
- **Mensagens de outros usuários** (exceto Leticia Kyoko e o bot)

### 📢 Mensagens Promocionais (A cada 1 hora)

O bot continua enviando mensagens promocionais automaticamente a cada hora:
```
Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor @kyoko_uwubot
```

## Como Funciona

### 1. Detecção de Mensagens

```python
# Handler específico para mensagens do grupo
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica se é do grupo configurado
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        return
    
    # Identifica tipos de mensagem para deletar
    should_delete = False
    
    # Mensagens de sistema (entrada/saída)
    if message.new_chat_members or message.left_chat_member:
        should_delete = True
    
    # Mensagens de usuários (exceto Leticia Kyoko e bot)
    elif not is_allowed_user(message.from_user):
        should_delete = True
```

### 2. Fila de Deleção

```python
# Lista global para armazenar mensagens marcadas
messages_to_delete = []

# Adiciona à fila
messages_to_delete.append({
    'chat_id': message.chat_id,
    'message_id': message.message_id,
    'timestamp': datetime.datetime.now()
})
```

### 3. Execução da Limpeza

```python
# Executa a cada 5 minutos
async def execute_message_cleanup(context: ContextTypes.DEFAULT_TYPE):
    for msg_info in messages_to_delete:
        try:
            await context.bot.delete_message(
                chat_id=msg_info['chat_id'],
                message_id=msg_info['message_id']
            )
        except Exception as e:
            # Log de erro e remoção de mensagens antigas
```

## Configuração dos Jobs

### APScheduler

O sistema utiliza o APScheduler para gerenciar tarefas automáticas:

```python
# Mensagens promocionais (1 hora)
job_queue.run_repeating(
    send_promotional_message,
    interval=3600,  # 1 hora
    first=10,       # Primeira em 10s
    name='promotional_messages'
)

# Limpeza de mensagens (5 minutos)
job_queue.run_repeating(
    execute_message_cleanup,
    interval=300,   # 5 minutos
    first=30,       # Primeira em 30s
    name='message_cleanup'
)
```

## Usuários Permitidos

### Critérios para Manter Mensagens

As mensagens são mantidas quando enviadas por:

1. **Leticia Kyoko**:
   - Username: `leticiakyoko`
   - Nome: `Leticia Kyoko`

2. **Bot Kyoko**:
   - Identificado pelo username do bot
   - Mensagens com `from_user.is_bot = True`

### Verificação de Usuário

```python
# Manter apenas mensagens permitidas
if (username.lower() != "leticiakyoko" and 
    first_name.lower() != "leticia kyoko" and 
    username != bot_username and 
    not message.from_user.is_bot):
    should_delete = True
```

## Monitoramento

### Comando /saude

O comando `/saude` foi atualizado para mostrar:

```
🤖 Status do Bot Kyoko

✅ Bot Online: Funcionando normalmente
⏰ Data/Hora: 27/07/2025 00:28:45
🕐 Uptime: 0:02:15
💾 Uso de Memória: 45.2%
🖥️ Uso de CPU: 12.1%
📢 Jobs Automáticos: ✅ Ativo
🧹 Mensagens p/ Limpeza: 3

🎯 Grupo Configurado: -4878162533
```

### Logs do Sistema

```
2025-07-27 00:28:45 - INFO - Jobs automáticos configurados para o grupo -4878162533:
2025-07-27 00:28:45 - INFO - - Mensagens promocionais: a cada 1 hora
2025-07-27 00:28:45 - INFO - - Limpeza de mensagens: a cada 5 minutos
2025-07-27 00:28:45 - INFO - Mensagem marcada para deleção: 12345
2025-07-27 00:28:50 - INFO - Limpeza concluída: 5 deletadas, 0 falharam
```

## Tratamento de Erros

### Mensagens Antigas

- Mensagens com mais de 48h são removidas da fila automaticamente
- Evita acúmulo de mensagens não deletáveis

### Falhas de Deleção

- Logs detalhados de falhas
- Retry automático na próxima execução
- Limpeza de mensagens expiradas

## Dependências

### Instalação Necessária

```bash
pip install python-telegram-bot[job-queue]
```

### Bibliotecas Utilizadas

- `APScheduler`: Agendamento de tarefas
- `python-telegram-bot`: API do Telegram
- `datetime`: Controle de tempo
- `logging`: Sistema de logs

## Configuração

### Variáveis de Ambiente

```env
GROUP_CHAT_ID=-4878162533  # ID do grupo para limpeza
BOT_TOKEN=seu_token_aqui   # Token do bot
```

### Personalização

```python
# Intervalo de limpeza (em segundos)
CLEANUP_INTERVAL = 300  # 5 minutos

# Intervalo promocional (em segundos)
PROMO_INTERVAL = 3600   # 1 hora

# Tempo limite para mensagens antigas (em segundos)
MESSAGE_EXPIRY = 172800 # 48 horas
```

## Benefícios

### Para o Grupo

- ✅ **Grupo sempre limpo**: Remove automaticamente spam de notificações
- ✅ **Foco no conteúdo**: Mantém apenas mensagens relevantes
- ✅ **Experiência melhorada**: Usuários veem apenas conteúdo da Leticia Kyoko

### Para o Negócio

- ✅ **Maior conversão**: Menos distrações no grupo
- ✅ **Profissionalismo**: Grupo sempre organizado
- ✅ **Automação completa**: Sem necessidade de moderação manual

### Para o Sistema

- ✅ **Performance otimizada**: Limpeza controlada e eficiente
- ✅ **Logs detalhados**: Monitoramento completo
- ✅ **Tratamento de erros**: Sistema robusto e confiável

## Próximos Passos

1. **Monitorar performance** do sistema em produção
2. **Ajustar intervalos** se necessário
3. **Adicionar métricas** de limpeza
4. **Implementar whitelist** de usuários se necessário
5. **Criar dashboard** de monitoramento

---

**Desenvolvido para otimizar a experiência do grupo e maximizar conversões do bot Kyoko.**