# Como Testar o Comando /metricas

## 🚀 Passo a Passo para Testar

### 1. Verificar se o Bot Está Rodando
- O bot deve estar executando (você verá logs no terminal)
- Procure por mensagens como "Bot iniciado!" e "Application started"

### 2. Abrir o Telegram
- Abra o aplicativo do Telegram no seu celular ou computador
- Procure pelo seu bot (nome que você configurou)

### 3. Testar o Comando /metricas
- Digite `/metricas` na conversa com o bot
- Pressione Enter ou toque em Enviar

### 4. O que Você Verá
O bot retornará um relatório completo com:

```
📊 MÉTRICAS DO BOT KYOKO

🎯 CONVERSÃO GERAL
• Total de conversas: X
• Total de pagamentos: X
• Taxa de conversão: X%
• Receita total: R$ X.XX
• Ticket médio: R$ X.XX

💰 VENDAS POR PACK
• Pack R$ 12,90: X vendas
• Pack R$ 5,00: X vendas

📅 ÚLTIMOS 7 DIAS
• 2025-01-26: X conversas, X pagamentos, R$ X.XX
• 2025-01-25: X conversas, X pagamentos, R$ X.XX
...

🕐 HOJE POR HORA
• 14:00: X conversas (X%)
• 15:00: X conversas (X%)
...
```

## 🧪 Como Gerar Dados para Teste

### Para Ter Dados nas Métricas:
1. **Inicie conversas**: Digite `/start` ou `/oi` várias vezes
2. **Simule pagamentos**: Complete o fluxo de compra (mesmo que seja teste)
3. **Aguarde**: As métricas são atualizadas em tempo real

### Comandos Úteis para Teste:
- `/start` - Inicia uma nova conversa
- `/oi` - Também inicia conversa
- `/metricas` - Visualiza as estatísticas

## 📱 Onde Usar o Comando

### No Telegram:
- **Chat privado** com o bot
- **Grupos** onde o bot foi adicionado (se configurado)
- **Canais** onde o bot tem permissões

### Quem Pode Usar:
- Por padrão, **qualquer usuário** pode usar `/metricas`
- Se quiser restringir, você pode modificar a função `show_metrics` no código

## 🔧 Solução de Problemas

### Se o comando não funcionar:
1. **Verifique se o bot está rodando**
2. **Confirme que não há erros no terminal**
3. **Teste outros comandos** como `/start`
4. **Reinicie o bot** se necessário

### Se aparecer "Erro ao carregar métricas":
1. Verifique se o arquivo `bot_metrics.json` existe
2. Confirme as permissões de escrita na pasta
3. Veja os logs no terminal para mais detalhes

## 📊 Interpretando os Dados

- **Taxa de conversão**: Percentual de usuários que pagaram
- **Ticket médio**: Valor médio por venda
- **Estatísticas por hora**: Mostra os horários de maior atividade
- **Dados diários**: Evolução das métricas ao longo dos dias

## 🎯 Dicas de Uso

1. **Monitore regularmente** para entender o comportamento dos usuários
2. **Compare dados diários** para identificar tendências
3. **Analise horários de pico** para otimizar campanhas
4. **Acompanhe a taxa de conversão** para melhorar o funil de vendas

---

**Nota**: As métricas são salvas automaticamente no arquivo `bot_metrics.json` e persistem mesmo após reiniciar o bot.