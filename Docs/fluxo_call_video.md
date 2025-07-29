# Fluxo Call de Vídeo - Bot Kyoko

## Visão Geral

O bot agora prioriza a venda de calls de vídeo de 5 minutos por R$ 29,90 como primeira oferta, antes de apresentar os packs tradicionais. Esta estratégia visa aumentar o ticket médio e oferecer uma experiência mais personalizada.

## Fluxo de Conversação

### 1. Mensagem Inicial
- Usuário inicia conversa com `/start` ou `/oi`
- Bot envia saudação padrão
- **NOVA:** Imediatamente após, apresenta oferta da call de vídeo

### 2. Oferta da Call de Vídeo
```
💕 **Oferta Especial!** 💕

Que tal fazermos uma call de vídeo de 5 minutos bem gostosinha? ❤️‍🔥

💰 **Apenas R$ 29,90**
📱 **5 minutos de pura diversão**
🔥 **Só eu e você, bem íntimo**

O que você acha, amor?
```

**Botões:**
- `💕 Sim, quero a call!` → Gera PIX de R$ 29,90
- `❌ Não, obrigado` → Continua fluxo normal dos packs

### 3. Fluxos Possíveis

#### 3.1 Usuário Aceita Call (callback: `call_video_yes`)
- Gera PIX de R$ 29,90 via API Pushin Pay
- Descrição: "Call de Vídeo 5min - R$ 29,90"
- Exibe código PIX com instruções
- Botões: "Copiar código PIX" e "Confirmar pagamento"
- Após pagamento confirmado: Redireciona para WhatsApp

#### 3.2 Usuário Recusa Call (callback: `call_video_no`)
- Mensagem: "Tudo bem, amor! Vamos para as outras opções então 😊"
- Continua fluxo normal: envia foto + oferta pack R$ 12,90
- Mantém toda a sequência original do bot

## Implementação Técnica

### Estados de Conversação
- Reutiliza `WAITING_PAYMENT_12` para call de vídeo
- Diferenciação feita pelo valor do pagamento (R$ 29,90 vs R$ 12,90)

### Callbacks Implementados
```python
# Aceitar call de vídeo
if data == "call_video_yes":
    payment_data = create_pix_payment(29.90, "Call de Vídeo 5min - R$ 29,90")
    # Gera PIX e exibe instruções

# Recusar call de vídeo  
elif data == "call_video_no":
    # Continua fluxo normal com foto e pack R$ 12,90
```

### Detecção de Tipo de Pagamento
Na função `send_content_link()`, o sistema:
1. Verifica o valor do pagamento via API
2. Se R$ 29,90 → É call de vídeo
3. Se R$ 12,90 → É pack normal
4. Envia mensagem apropriada

## Mensagens de Confirmação

### Call de Vídeo Paga
```
💕 **Pagamento confirmado!** 💕

🔥 **Nossa call de vídeo está confirmada!**

📱 **Entre no WhatsApp para marcarmos:**
wa.me/5583999620663

💋 Te espero lá, amor! Vai ser delicioso... ❤️‍🔥
```

### Pack Normal Pago
- Mantém mensagem original
- Link para o site de conteúdo
- Mensagem de suporte

## Mensagem Promocional Atualizada

A mensagem promocional automática no grupo foi alterada para:
```
"Vem fazer uma call de vídeo comigo amor ❤️‍🔥 eu faço um descontinho na hora para você rsrs - wa.me/5583999620663"
```

## Métricas e Acompanhamento

### Novos Tipos de Pagamento
- `call_video`: R$ 29,90 (call de vídeo)
- `pack_12`: R$ 12,90 (pack normal)
- `pack_10`: R$ 10,00 (comando /10)
- `pack_5`: R$ 5,90 (pack desconto)

### KPIs a Acompanhar
1. **Taxa de Conversão Call vs Pack**
   - % usuários que escolhem call
   - % usuários que escolhem pack após recusar call

2. **Ticket Médio**
   - Impacto da call de R$ 29,90 no ticket médio
   - Comparação antes/depois da implementação

3. **Funil de Conversão**
   - Conversas iniciadas
   - Ofertas de call apresentadas
   - Calls aceitas vs recusadas
   - Pagamentos efetivados

## Vantagens da Estratégia

### Para o Negócio
- **Maior ticket médio:** R$ 29,90 vs R$ 12,90 (+132%)
- **Experiência premium:** Call personalizada
- **Diferenciação:** Serviço único no mercado
- **Fidelização:** Contato direto com cliente

### Para o Cliente
- **Experiência exclusiva:** Interação personalizada
- **Flexibilidade:** Pode escolher entre call ou pack
- **Valor percebido:** Serviço premium por preço acessível

## Fluxo de Fallback

Se usuário recusa call:
1. Não há pressão ou insistência
2. Transição suave para ofertas de pack
3. Mantém toda experiência original
4. Preserva taxa de conversão dos packs

## Configurações Técnicas

### Arquivos Modificados
- `bot.py`: Lógica principal e callbacks
- Mensagem promocional atualizada
- Função `send_content_link()` adaptada

### Integração com API
- Pushin Pay para PIX de R$ 29,90
- Mesma infraestrutura dos outros pagamentos
- Timeout padrão de 30 minutos

### WhatsApp Integration
- Link direto: `wa.me/5583999620663`
- Redirecionamento automático após pagamento
- Facilita agendamento da call

## Monitoramento e Otimização

### Logs Importantes
```python
logger.info(f"Call de vídeo aceita por {user_name}")
logger.info(f"Call de vídeo recusada por {user_name}")
logger.info(f"Pagamento call confirmado: {payment_id}")
```

### Métricas de Sucesso
- Taxa de aceitação da call: > 15%
- Ticket médio geral: > R$ 18,00
- Satisfação do cliente (feedback WhatsApp)

### Possíveis Otimizações
1. **A/B Testing:** Diferentes valores para call
2. **Horários:** Ofertas em horários específicos
3. **Segmentação:** Ofertas baseadas no histórico
4. **Upsell:** Call + pack em combo

## Próximos Passos

### Implementações Futuras
1. **Sistema de Agendamento**
   - Calendário integrado
   - Slots de horário disponíveis
   - Confirmação automática

2. **Pacotes Combo**
   - Call + Pack por R$ 35,00
   - Desconto progressivo
   - Fidelização de clientes

3. **Feedback System**
   - Avaliação pós-call
   - Melhoria contínua
   - Testimonials para marketing

### Análise de Performance
- Acompanhar métricas por 30 dias
- Comparar com período anterior
- Ajustar estratégia conforme resultados
- Documentar learnings e insights

## Considerações de Segurança

### Proteção de Dados
- Não armazenar dados pessoais da call
- WhatsApp como canal seguro
- Logs apenas de métricas agregadas

### Compliance
- Respeitar horários comerciais
- Política clara de cancelamento
- Termos de uso transparentes

Esta implementação posiciona o bot para capturar maior valor por cliente enquanto mantém a flexibilidade e experiência positiva para todos os tipos de usuário.