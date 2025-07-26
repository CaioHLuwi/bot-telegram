# Comando /saude - Verificação de Status do Bot

## Visão Geral

O comando `/saude` permite verificar se o bot Kyoko está funcionando normalmente e obter informações detalhadas sobre seu status operacional.

## Como Usar

### Comando
```
/saude
```

### Onde Usar
- ✅ **Chat privado** com o bot
- ✅ **Grupos** onde o bot está presente
- ✅ **Canais** onde o bot tem permissões

## Informações Exibidas

### 🤖 Status Básico
- **Bot Online**: Confirmação de funcionamento
- **Data/Hora**: Timestamp atual do servidor
- **Uptime**: Tempo que o bot está rodando

### 📊 Informações do Sistema
- **Uso de Memória**: Percentual de RAM utilizada
- **Uso de CPU**: Percentual de processamento
- **Mensagens Automáticas**: Status da configuração

### 🎯 Configurações
- **Grupo Configurado**: ID do grupo para mensagens automáticas (se configurado)
- **Comandos Disponíveis**: Lista de todos os comandos do bot

## Exemplo de Resposta

```
🤖 Status do Bot Kyoko

✅ Bot Online: Funcionando normalmente
⏰ Data/Hora: 15/12/2024 14:30:25
🕐 Uptime: 2:15:30
💾 Uso de Memória: 45.2%
🖥️ Uso de CPU: 12.8%
📢 Mensagens Automáticas: ✅ Ativo

🎯 Grupo Configurado: `-1001234567890`

🔄 Comandos Disponíveis:
• /start - Iniciar bot
• /oi - Saudação
• /metricas - Ver estatísticas
• /groupid - ID do grupo
• /saude - Status do bot

💚 Tudo funcionando perfeitamente!
```

## Casos de Uso

### ✅ Para Administradores
- Verificar se o bot está respondendo
- Monitorar performance do sistema
- Confirmar configurações das mensagens automáticas
- Diagnosticar problemas de conectividade

### ✅ Para Usuários
- Verificar se o bot está online
- Ver lista de comandos disponíveis
- Confirmar funcionamento antes de usar outros recursos

## Tratamento de Erros

### Erro de Sistema
Se houver problemas ao coletar informações do sistema:

```
❌ Erro ao verificar status:

`[detalhes do erro]`

⚠️ O bot está online, mas houve um problema ao coletar informações do sistema.
```

### Possíveis Causas de Erro
- Falta da dependência `psutil`
- Permissões insuficientes do sistema
- Problemas temporários de memória

## Dependências

### Bibliotecas Necessárias
- `psutil`: Para informações do sistema
- `datetime`: Para timestamps (nativa do Python)
- `os`: Para informações do processo (nativa do Python)

### Instalação
A dependência `psutil` está incluída no `requirements.txt`:
```
psutil
```

## Logs

### Execução Bem-sucedida
```
Comando /saude executado por [Nome do Usuário]
```

### Execução com Erro
```
Erro no comando /saude: [detalhes do erro]
```

## Segurança

### ✅ Informações Seguras
- Não expõe dados sensíveis
- Não revela tokens ou chaves
- Mostra apenas estatísticas básicas do sistema

### ⚠️ Considerações
- O comando pode ser usado por qualquer usuário
- Informações do sistema são genéricas
- ID do grupo é mostrado apenas se configurado

## Troubleshooting

### Problema: Comando não responde
**Solução**: Verificar se o bot está online e tem permissões

### Problema: Erro de importação psutil
**Solução**: 
```bash
pip install psutil
```

### Problema: Informações incorretas
**Solução**: Reiniciar o bot para atualizar estatísticas

## Personalização

### Modificar Informações Exibidas
Edite a função `saude_command` em <mcfile name="bot.py" path="bot.py"></mcfile>:

```python
# Adicionar novas informações
message += f"🆔 **Bot ID:** {context.bot.id}\n"
message += f"👤 **Bot Username:** @{context.bot.username}\n"
```

### Alterar Formato da Resposta
```python
# Usar HTML em vez de Markdown
await update.message.reply_text(message, parse_mode='HTML')
```

---

**Nota**: Este comando é essencial para monitoramento e diagnóstico do bot. Use regularmente para garantir o funcionamento adequado do sistema.