# 📊 Sistema de Métricas - Bot Kyoko

## 🎯 Overview

O Bot Kyoko agora possui um sistema completo de métricas que permite acompanhar o desempenho e as estatísticas de uso em tempo real.

## 🚀 Como Usar

### Comando Principal

Para visualizar as métricas do bot, use o comando:

```
/metricas
```

### O que é Rastreado

#### 📈 Métricas Gerais
- **Total de conversas iniciadas**: Quantas pessoas começaram a conversar com o bot
- **Total de pagamentos**: Quantos pagamentos foram confirmados
- **Taxa de conversão**: Percentual de conversas que resultaram em pagamento
- **Receita total**: Valor total arrecadado
- **Ticket médio**: Valor médio por venda

#### 💰 Vendas por Tipo de Pack
- **Pack R$ 12,90**: Quantidade de vendas do pack completo
- **Pack R$ 5,00**: Quantidade de vendas do pack com desconto

#### 📅 Estatísticas Diárias
- Últimos 7 dias com:
  - Número de conversas por dia
  - Número de pagamentos por dia
  - Receita por dia

#### 🕐 Estatísticas por Hora
- Atividade do dia atual dividida por hora
- Mostra apenas horas com atividade

## 📊 Exemplo de Relatório

```
📊 MÉTRICAS DO BOT KYOKO

🎯 CONVERSÃO GERAL
• Total de conversas: 45
• Total de pagamentos: 12
• Taxa de conversão: 26.67%
• Receita total: R$ 134.70
• Ticket médio: R$ 11.23

💰 VENDAS POR PACK
• Pack R$ 12,90: 8 vendas
• Pack R$ 5,00: 4 vendas

📅 ÚLTIMOS 7 DIAS
• 2025-01-20: 5 conversas, 2 pagamentos, R$ 25.80
• 2025-01-21: 8 conversas, 3 pagamentos, R$ 33.70
• 2025-01-22: 12 conversas, 4 pagamentos, R$ 46.60

🕐 HOJE POR HORA
• 10h: 3 conversas
• 14h: 7 conversas
• 18h: 5 conversas
```

## 🔧 Funcionalidades Técnicas

### Armazenamento
- As métricas são salvas automaticamente em `bot_metrics.json`
- Dados persistem entre reinicializações do bot
- Backup automático dos dados

### Rastreamento Automático
- **Início de conversa**: Registrado quando usuário envia `/start`, `/oi` ou qualquer mensagem
- **Pagamentos**: Registrados automaticamente quando confirmados via Pushin Pay
- **Dados do usuário**: ID, username e nome são salvos para análise

### Estatísticas Calculadas
- Taxa de conversão em tempo real
- Ticket médio atualizado automaticamente
- Estatísticas por período (dia/hora)
- Histórico completo de interações

## 📈 Interpretando os Dados

### Taxa de Conversão
- **Boa**: Acima de 20%
- **Média**: Entre 10-20%
- **Baixa**: Abaixo de 10%

### Ticket Médio
- Indica se mais pessoas estão comprando o pack completo ou com desconto
- Valor próximo a R$ 12,90 = mais vendas do pack completo
- Valor próximo a R$ 5,00 = mais vendas com desconto

### Horários de Pico
- Identifica os melhores horários para promover o bot
- Ajuda a entender o comportamento dos usuários

## 🎯 Dicas de Uso

1. **Monitore diariamente**: Use `/metricas` para acompanhar o desempenho
2. **Analise tendências**: Compare dados de diferentes dias
3. **Otimize horários**: Foque promoções nos horários de maior atividade
4. **Acompanhe conversão**: Se a taxa estiver baixa, considere ajustar a abordagem

## 🔒 Privacidade

- Apenas IDs, usernames e nomes são armazenados
- Nenhuma mensagem privada é salva
- Dados são usados apenas para métricas internas
- Informações sensíveis não são coletadas

## 🚨 Resolução de Problemas

### Comando não funciona
- Verifique se o bot está rodando
- Confirme que você tem permissão para usar comandos

### Métricas zeradas
- Pode indicar que o arquivo `bot_metrics.json` foi corrompido
- O sistema criará um novo arquivo automaticamente

### Dados inconsistentes
- Reinicie o bot para recarregar as métricas
- Verifique se há múltiplas instâncias do bot rodando

---

**💡 Dica**: Use as métricas para tomar decisões baseadas em dados e otimizar a performance do seu bot!