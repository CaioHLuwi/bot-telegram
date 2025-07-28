# Comando /gerarpix - PIX Personalizado

## Visão Geral

O comando `/gerarpix` permite que os usuários gerem códigos PIX com valores personalizados, oferecendo flexibilidade para diferentes necessidades de pagamento.

## Como Funciona

### 1. Iniciação do Comando
- Usuário digita `/gerarpix`
- Bot solicita o valor desejado
- Estado do usuário é definido como `WAITING_PIX_VALUE`

### 2. Entrada do Valor
- Usuário informa o valor (ex: `25.50`, `100`, `15.90`)
- Bot valida se o valor está dentro dos limites permitidos
- Valor mínimo: R$ 1,00
- Valor máximo: R$ 1.000,00

### 3. Geração do PIX
- Bot gera código PIX via API Pushin Pay
- Exibe código PIX formatado
- Fornece instruções de pagamento
- Oferece botões para copiar código e confirmar pagamento

## Fluxo Técnico

### Estados de Conversação
```python
class ConversationState(Enum):
    WAITING_PIX_VALUE = "waiting_pix_value"  # Aguardando valor do PIX
```

### Validação de Entrada
- Aceita valores com vírgula ou ponto como separador decimal
- Converte automaticamente vírgula para ponto
- Valida range de R$ 1,00 a R$ 1.000,00
- Trata erros de formato inválido

### Integração com API
- Utiliza função `create_pix_payment(valor, descricao)`
- Descrição automática: "Pack Kyoko - PIX Personalizado - R$ {valor}"
- Armazena `payment_id` e `pix_code` no contexto do usuário

## Callbacks e Botões

### Botão "Copiar código PIX"
- Callback: `copy_pix_custom_{payment_id}`
- Exibe alerta de confirmação
- Envia código PIX em mensagem separada para facilitar cópia

### Botão "Confirmar pagamento"
- Callback: `confirm_payment_custom`
- Verifica status do pagamento via API
- Redireciona para envio do conteúdo se pago
- Informa status se pendente

## Tratamento de Erros

### Valor Inválido
- Formato incorreto: "❌ Valor inválido..."
- Fora do range: "❌ Valor deve estar entre R$ 1,00 e R$ 1.000,00"

### Erro na API
- Falha na geração: "❌ Erro ao gerar PIX personalizado..."
- Log detalhado do erro para debugging

### Dados Perdidos
- Payment ID não encontrado: "Erro: ID do pagamento não encontrado"
- Código PIX não encontrado: "Erro: Código PIX não encontrado"

## Mensagens do Bot

### Solicitação de Valor
```
💰 **Gerar PIX Personalizado**

Digite o valor desejado para o PIX:

📝 **Exemplos:**
• `15.50`
• `25`
• `100.00`

⚠️ **Valor mínimo:** R$ 1,00
⚠️ **Valor máximo:** R$ 1.000,00
```

### Confirmação do PIX
```
💰 **PIX Personalizado de R$ {valor} gerado!**

**Código PIX:**
`{codigo_pix}`

📱 **Como pagar:**
1. Copie o código PIX
2. Abra seu banco
3. Cole o código na área PIX
4. Confirme o pagamento
5. Clique em 'Confirmar pagamento'

⏰ **Pagamento expira em 30 minutos**
```

## Segurança e Validações

### Limites de Valor
- Mínimo: R$ 1,00 (evita valores muito baixos)
- Máximo: R$ 1.000,00 (controle de risco)

### Validação de Formato
- Aceita números inteiros e decimais
- Suporte a vírgula e ponto decimal
- Rejeita caracteres não numéricos

### Timeout de Pagamento
- PIX expira em 30 minutos (padrão Pushin Pay)
- Estado do usuário é resetado após processamento

## Métricas e Logs

### Logs Registrados
- Início do comando com nome do usuário
- Valor solicitado e validação
- Sucesso/falha na geração do PIX
- Erros de API ou validação

### Integração com Métricas
- Pagamentos personalizados são registrados no sistema de métricas
- Valor e tipo de pagamento são armazenados
- Contribui para estatísticas de conversão

## Casos de Uso

### Valores Comuns
- R$ 15,00 - Promoções especiais
- R$ 25,00 - Pacotes intermediários
- R$ 50,00 - Pacotes premium
- R$ 100,00 - Pacotes VIP

### Flexibilidade
- Permite testes com diferentes preços
- Adaptação a promoções sazonais
- Personalização por cliente
- Facilita negociações individuais

## Manutenção

### Ajustes de Limites
Para alterar os limites de valor, modifique as constantes em `handle_message()`:
```python
if valor < 1.00 or valor > 1000.00:
    # Alterar valores conforme necessário
```

### Personalização de Mensagens
As mensagens podem ser customizadas nas funções:
- `gerar_pix_command()` - Mensagem inicial
- `handle_message()` - Mensagens de validação e confirmação

### Monitoramento
- Acompanhar logs para identificar valores mais solicitados
- Monitorar taxa de conversão por faixa de valor
- Ajustar limites baseado no comportamento dos usuários

## Integração com Outros Comandos

O comando `/gerarpix` complementa:
- `/10` - PIX fixo de R$ 10,00
- `/start` - Fluxo principal com PIX de R$ 12,90
- Sistema de métricas para análise de performance

## Próximas Melhorias

### Funcionalidades Futuras
- Histórico de PIX gerados por usuário
- Desconto automático para valores altos
- Integração com sistema de cupons
- Notificações de pagamento em tempo real

### Otimizações
- Cache de códigos PIX para evitar regeneração
- Validação de CPF para valores altos
- Integração com outros métodos de pagamento
- Dashboard de valores mais solicitados