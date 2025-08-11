# Integração Paradise API - Comando /pix

## Visão Geral

Este documento descreve a implementação da integração com a Paradise API para geração de pagamentos PIX através do comando `/pix` no bot do Telegram.

## Funcionalidades Implementadas

### Comando /pix
- **Descrição**: Gera PIX personalizado usando a Paradise API
- **Uso**: `/pix`
- **Fluxo**: Solicita valor → Gera PIX → Exibe código → Confirma pagamento

### Características
- ✅ Valores personalizados (R$ 1,00 a R$ 1.000,00)
- ✅ Geração automática de código PIX
- ✅ Interface com botões interativos
- ✅ Validação de valores
- ✅ Registro de métricas
- ✅ Tratamento de erros

## Configuração

### Variáveis de Ambiente (.env)
```env
# Paradise API
PARADISE_API_TOKEN=27Gwhqe0OW5aP7HaatdRPtOqFIjx9yPo3yXFzv2OXWzCL2YgHkr83PV6jc39
PARADISE_BASE_URL=https://api.paradisepagbr.com/api
PARADISE_OFFER_HASH=seu_offer_hash_aqui
```

### Arquivo config.py
```python
# Paradise API
PARADISE_API_TOKEN = os.getenv('PARADISE_API_TOKEN', '27Gwhqe0OW5aP7HaatdRPtOqFIjx9yPo3yXFzv2OXWzCL2YgHkr83PV6jc39')
PARADISE_BASE_URL = os.getenv('PARADISE_BASE_URL', 'https://api.paradisepagbr.com/api')
PARADISE_OFFER_HASH = os.getenv('PARADISE_OFFER_HASH', 'hash_da_oferta')
```

## Implementação Técnica

### Função de Criação de PIX
```python
def create_paradise_pix_payment(amount: float, description: str) -> dict:
    """Criar pagamento PIX usando Paradise API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            'api_token': PARADISE_API_TOKEN,
            'offer_hash': PARADISE_OFFER_HASH,
            'amount': amount,
            'currency': 'BRL',
            'payment_method': 'pix',
            'description': description,
            'customer': {
                'name': 'Cliente',
                'email': 'cliente@exemplo.com'
            }
        }
        
        response = requests.post(
            f'{PARADISE_BASE_URL}/transactions',
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            return None
            
    except Exception as e:
        logger.error(f'Erro na API Paradise: {e}')
        return None
```

### Comando /pix
```python
async def pix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pix - gerar PIX com Paradise API"""
    try:
        user_id = update.effective_user.id
        
        # Definir estado para aguardar valor
        user_states[user_id] = 'waiting_paradise_pix_value'
        
        message = "💰 **Gerar PIX com Paradise**\n\n"
        message += "Digite o valor desejado para o PIX:\n\n"
        message += "📝 **Exemplos:**\n"
        message += "• `15.50`\n"
        message += "• `25`\n"
        message += "• `100.00`\n\n"
        message += "⚠️ **Valor mínimo:** R$ 1,00\n"
        message += "⚠️ **Valor máximo:** R$ 1.000,00"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /pix: {e}")
        await update.message.reply_text("❌ Erro interno. Tente novamente mais tarde.")
```

## Estados da Conversa

### Estado: waiting_paradise_pix_value
- **Descrição**: Aguardando o usuário digitar o valor do PIX
- **Validações**:
  - Valor mínimo: R$ 1,00
  - Valor máximo: R$ 1.000,00
  - Formato numérico válido
- **Próximo estado**: `WAITING_RESPONSE` (após gerar PIX)

## Interface do Usuário

### Mensagem de Solicitação de Valor
```
💰 **Gerar PIX com Paradise**

Digite o valor desejado para o PIX:

📝 **Exemplos:**
• 15.50
• 25
• 100.00

⚠️ **Valor mínimo:** R$ 1,00
⚠️ **Valor máximo:** R$ 1.000,00
```

### Mensagem de PIX Gerado
```
✅ **PIX Paradise Gerado!**

💰 **Valor:** R$ XX,XX

📋 **Código PIX:**
`codigo_pix_aqui`

⏰ **Válido por:** 30 minutos

📱 **Como pagar:**
1. Copie o código PIX
2. Abra seu app bancário
3. Escolha PIX > Copia e Cola
4. Cole o código e confirme
```

### Botões Interativos
- **📋 Copiar Código PIX**: Copia o código PIX para facilitar o pagamento
- **✅ Confirmar Pagamento**: Confirma o pagamento e finaliza o processo

## Tratamento de Erros

### Validação de Valores
- **Valor muito baixo**: Mensagem de erro + nova solicitação
- **Valor muito alto**: Mensagem de erro + nova solicitação
- **Formato inválido**: Mensagem de erro + nova solicitação

### Erros da API
- **Falha na requisição**: Log do erro + mensagem amigável ao usuário
- **Resposta inválida**: Tratamento gracioso + reset do estado

## Métricas e Logs

### Registros de Log
- Início do comando `/pix`
- Resposta da API Paradise
- Erros de processamento
- PIX gerado com sucesso

### Métricas do Bot
- Comando `/pix` utilizado
- Pagamentos Paradise confirmados
- Valores dos pagamentos

## Diferenças da Pushinpay

### Semelhanças
- Interface idêntica para o usuário
- Mesmo fluxo de validação
- Mesmos limites de valor
- Botões interativos iguais

### Diferenças Técnicas
- **API Endpoint**: Paradise vs Pushinpay
- **Autenticação**: Token vs Bearer
- **Payload**: Estrutura diferente
- **Resposta**: Campos diferentes

## Comandos Disponíveis

| Comando | API | Descrição |
|---------|-----|-----------|
| `/gerarpix` | Pushinpay | PIX personalizado com Pushinpay |
| `/pix` | Paradise | PIX personalizado com Paradise |
| `/10` | Pushinpay | Pack R$ 10,00 |
| `/start` | Pushinpay | Fluxo completo com packs |

## Próximos Passos

### Melhorias Sugeridas
1. **Verificação de Status**: Implementar consulta real de pagamento
2. **Webhook**: Configurar webhook para confirmação automática
3. **Timeout**: Implementar expiração de PIX
4. **Histórico**: Salvar histórico de transações

### Configurações Adicionais
1. **Offer Hash**: Configurar hash da oferta correto
2. **Webhook URL**: Configurar URL de callback
3. **Ambiente**: Configurar para produção

## Suporte

Para dúvidas sobre a integração Paradise API:
- Documentação: Paradise API Docs
- Suporte: Contato Paradise
- Logs: Verificar logs do bot para erros

---

**Última atualização**: $(date)
**Versão**: 1.0
**Responsável**: Bot Kyoko Team