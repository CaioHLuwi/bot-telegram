# Controle de Promoções - Intervalo de 1 Hora

## Visão Geral

Este documento detalha as modificações implementadas no sistema de mensagens promocionais automáticas, incluindo a alteração do intervalo para 1 hora, a nova mensagem promocional de suporte e a adição do comando `/pararpromo` para controle manual.

## Funcionalidades Implementadas

### 1. Intervalo Reduzido
- **Intervalo anterior:** 12 horas (43.200 segundos)
- **Novo intervalo:** 1 hora (3600 segundos)
- **Objetivo:** Maior frequência de exposição da oferta promocional

### 2. Comando de Controle `/pararpromo`
- **Acesso:** Apenas em chat privado
- **Função:** Alternar entre ativar/desativar mensagens promocionais
- **Feedback:** Status atual e histórico de alterações

## Implementação Técnica

### Variável de Controle Global
```python
promotional_messages_enabled = True
```

### Função de Controle
```python
async def parar_promo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para parar/iniciar mensagens promocionais automáticas"""
    global promotional_messages_enabled
    
    # Verificação de chat privado
    if update.effective_chat.type != 'private':
        return
    
    # Alternar estado
    promotional_messages_enabled = not promotional_messages_enabled
```

### Verificação na Função Promocional
```python
async def send_promotional_message(context: ContextTypes.DEFAULT_TYPE):
    global promotional_messages_enabled
    
    if not promotional_messages_enabled:
        logger.info("Mensagens promocionais desabilitadas - pulando envio")
        return
```

### Configuração do Job
```python
job_queue.run_repeating(
    send_promotional_message,
    interval=3600,  # 1 hora
    first=10,
    name='promotional_messages'
)
```

## Rotas e Comandos

### Comando `/pararpromo`
- **Método:** CommandHandler
- **Restrição:** Chat privado apenas
- **Resposta:** Status atual das promoções
- **Log:** Registra alterações com ID do usuário

### Comando `/saude` (Atualizado)
- **Nova informação:** Status das mensagens promocionais
- **Formato:** "📢 **Mensagens Promocionais:** ✅ Ativas / ❌ Desativadas"
- **Comando adicional listado:** `/pararpromo`

## Fluxo de Funcionamento

### 1. Envio Automático (A cada 1 hora)
```
1. Job scheduler executa send_promotional_message
2. Verifica promotional_messages_enabled
3. Se True: envia mensagem com menções
4. Se False: pula envio e registra log
```

### 2. Controle Manual
```
1. Usuário envia /pararpromo no privado
2. Sistema alterna promotional_messages_enabled
3. Retorna status atual e timestamp
4. Registra ação no log
```

## Segurança e Validações

### Restrições de Acesso
- `/pararpromo` funciona apenas em chat privado
- Previne uso acidental em grupos
- Mensagem de erro clara para tentativas em grupo

### Tratamento de Erros
- Try/catch em todas as operações
- Logs detalhados de erros
- Mensagens de erro amigáveis ao usuário

## Monitoramento e Logs

### Logs Implementados
```
- "Mensagens promocionais ativadas/desativadas por usuário {user_id}"
- "Mensagens promocionais desabilitadas - pulando envio"
- "- Mensagens promocionais: a cada 1 hora"
```

### Métricas de Acompanhamento
- Frequência de uso do comando `/pararpromo`
- Tempo médio entre ativação/desativação
- Taxa de engajamento com intervalo de 1 hora

## Impacto no Desempenho

### Considerações
- **Frequência moderada:** 24 mensagens por dia
- **Controle de spam:** Comando de desativação disponível
- **Recursos:** Mínimo impacto adicional no servidor

### Otimizações
- Verificação rápida da variável global
- Early return quando desabilitado
- Logs eficientes

## Estratégia de Marketing

### Nova Mensagem Promocional
- **Conteúdo:** Mensagem de suporte e direcionamento
- **Objetivo:** Direcionar dúvidas para atendimento personalizado
- **Canal:** @leticiakyoko para atendimento direto

### Benefícios do Intervalo de 1 Hora
- Lembrança constante do canal de suporte
- Captura de usuários em diferentes horários
- Direcionamento eficaz para atendimento personalizado

### Controle de Experiência do Usuário
- Comando de desativação para usuários sensíveis
- Transparência no status das promoções
- Flexibilidade de controle

## Configurações de Ambiente

### Variáveis Necessárias
- `GROUP_CHAT_ID`: ID do grupo para envio
- `BOT_TOKEN`: Token do bot Telegram

### Dependências
- `python-telegram-bot[job-queue]`
- Módulos de logging e datetime

## Melhorias Futuras

### Possíveis Implementações
1. **Horários específicos:** Configurar horários de pico
2. **Intervalos dinâmicos:** Ajustar baseado em engajamento
3. **Controle por usuário:** Preferências individuais
4. **Analytics avançados:** Métricas de conversão
5. **A/B Testing:** Diferentes intervalos para grupos

## Comandos de Teste

### Verificação de Funcionamento
```bash
# Verificar status
/saude

# Controlar promoções (privado)
/pararpromo

# Verificar logs
tail -f bot.log | grep "promocional"
```

## Conclusão

A implementação do intervalo de 1 hora com controle manual oferece:
- **Flexibilidade:** Controle total sobre as promoções
- **Agressividade:** Marketing mais frequente
- **Usabilidade:** Comando simples de controle
- **Transparência:** Status sempre visível

Essas modificações permitem uma estratégia de marketing mais dinâmica enquanto mantêm o controle sobre a experiência do usuário.