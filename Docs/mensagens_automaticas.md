# 📢 Sistema de Mensagens Automáticas

## 📋 Visão Geral

O bot Kyoko agora possui um sistema de mensagens automáticas que envia mensagens promocionais para grupos do Telegram a cada hora. Este sistema é ideal para manter o engajamento e promover os packs de forma consistente.

## ⚙️ Configuração

### 1. Obter o ID do Grupo

Para configurar as mensagens automáticas, você precisa do ID do grupo "Kyoko Packs 👄❤️‍🔥":

1. **Adicione o bot ao grupo** onde deseja enviar as mensagens
2. **No grupo**, envie o comando `/groupid`
3. **Copie o ID** que o bot retornará (formato: `-1001234567890`)

### 2. Configurar o Arquivo .env

Edite o arquivo `.env` e adicione/atualize a linha:

```env
GROUP_CHAT_ID=-1001234567890
```

*Substitua `-1001234567890` pelo ID real do seu grupo.*

### 3. Reiniciar o Bot

Após configurar o `GROUP_CHAT_ID`, reinicie o bot para ativar as mensagens automáticas.

## 🚀 Funcionalidades

### Mensagem Promocional

**Texto enviado:**
```
Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor
```

### Frequência

- **Intervalo:** A cada 1 hora (3600 segundos)
- **Primeira execução:** 1 minuto após iniciar o bot
- **Funcionamento:** 24/7 enquanto o bot estiver ativo

## 🔧 Comandos Relacionados

### `/groupid`

**Função:** Obter o ID do grupo atual

**Uso:**
- Execute no grupo onde deseja ativar as mensagens
- Retorna o ID do grupo para configuração
- Só funciona em grupos (não em conversas privadas)

**Exemplo de resposta:**
```
📋 ID deste grupo: -1001234567890

Copie este ID e adicione no arquivo .env como GROUP_CHAT_ID para ativar as mensagens automáticas.
```

## 📊 Logs e Monitoramento

### Logs de Sucesso
```
2025-01-26 10:00:00 - __main__ - INFO - Mensagens automáticas configuradas para o grupo -1001234567890 (a cada 1 hora)
2025-01-26 10:01:00 - __main__ - INFO - Mensagem promocional enviada para o grupo -1001234567890
```

### Logs de Erro
```
2025-01-26 10:00:00 - __main__ - WARNING - GROUP_CHAT_ID não configurado - mensagens automáticas desabilitadas
2025-01-26 10:01:00 - __main__ - ERROR - Erro ao enviar mensagem promocional: [erro]
```

## 🛠️ Solução de Problemas

### Mensagens não estão sendo enviadas

1. **Verifique o arquivo .env:**
   - Confirme se `GROUP_CHAT_ID` está configurado
   - Verifique se o ID está correto (formato: `-1001234567890`)

2. **Verifique as permissões do bot:**
   - O bot deve ser administrador do grupo
   - O bot deve ter permissão para enviar mensagens

3. **Verifique os logs:**
   - Procure por mensagens de erro no console
   - Confirme se o bot foi iniciado corretamente

### Bot não consegue obter ID do grupo

1. **Adicione o bot ao grupo:**
   - Use @[nome_do_bot] para adicionar
   - Torne o bot administrador (recomendado)

2. **Execute o comando no grupo:**
   - `/groupid` deve ser executado dentro do grupo
   - Não funciona em conversas privadas

## 🔒 Segurança

### Boas Práticas

1. **Mantenha o ID do grupo seguro:**
   - Não compartilhe o `GROUP_CHAT_ID` publicamente
   - Use variáveis de ambiente para armazenar

2. **Monitore o uso:**
   - Acompanhe os logs regularmente
   - Verifique se as mensagens estão sendo bem recebidas

3. **Permissões mínimas:**
   - O bot só precisa de permissão para enviar mensagens
   - Evite dar permissões desnecessárias

## 📈 Personalização

### Alterar Frequência

Para alterar o intervalo das mensagens, edite o arquivo `bot.py`:

```python
# Alterar de 1 hora (3600) para outro intervalo
job_queue.run_repeating(
    send_promotional_message,
    interval=1800,  # 30 minutos
    first=60,
    name='promotional_messages'
)
```

### Alterar Mensagem

Para personalizar a mensagem promocional, edite a função `send_promotional_message` em `bot.py`:

```python
promotional_text = "Sua nova mensagem promocional aqui!"
```

### Múltiplos Grupos

Para enviar para múltiplos grupos, você pode:

1. **Configurar múltiplos IDs no .env:**
```env
GROUP_CHAT_ID_1=-1001234567890
GROUP_CHAT_ID_2=-1009876543210
```

2. **Modificar a função para enviar para todos os grupos**

## ✅ Teste

### Verificar Configuração

1. **Inicie o bot**
2. **Verifique os logs** para confirmar:
   ```
   Mensagens automáticas configuradas para o grupo [ID] (a cada 1 hora)
   ```
3. **Aguarde 1 minuto** para a primeira mensagem
4. **Confirme no grupo** se a mensagem foi enviada

---

**✅ Com essas configurações, o bot enviará mensagens promocionais automaticamente para o grupo a cada hora!**