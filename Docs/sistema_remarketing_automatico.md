# 📱 Sistema de Remarketing Automático PIX

## 🎯 Visão Geral

Sistema automatizado de remarketing que envia mensagens promocionais em intervalos específicos após a geração do PIX, com o objetivo de aumentar a conversão de vendas através de ofertas progressivas e persuasivas.

## ⚡ Funcionalidades Principais

### 🕐 Cronograma de Mensagens
- **5 minutos**: Vídeo promocional com 50% de desconto
- **10 minutos**: Imagem promocional com oferta alternativa

### 🎬 Tipos de Mídia
- **Vídeo**: `media/1.mp4` - Conteúdo visual persuasivo
- **Imagem**: `media/2.jpg` - Material gráfico promocional

### 💬 Mensagens Persuasivas
- Textos provocativos e chamativas
- Ofertas progressivas de desconto
- Call-to-action diretos

## 🏗️ Arquitetura do Sistema

### Arquivos Principais
```
├── sistema_remarketing_pix.py     # Classe principal do sistema
├── bot_leticia_menu.py            # Integração com bot principal
├── integracao_utmify_pushinpay.py # Integração com APIs
├── media/
│   ├── 1.mp4                      # Vídeo promocional
│   └── 2.jpg                      # Imagem promocional
└── Docs/
    └── sistema_remarketing_automatico.md
```

### Classe RemarketingPIX
```python
class RemarketingPIX:
    def __init__(self, bot_token: str)
    async def iniciar_campanha_remarketing(...)
    async def enviar_video_promocional(...)
    async def enviar_imagem_promocional(...)
    def gerar_texto_video_remarketing(...)
    def gerar_texto_imagem_remarketing(...)
```

## 🚀 Implementação

### 1. Inicialização Automática
```python
# No bot_leticia_menu.py
remarketing_system = RemarketingPIX(BOT_TOKEN)

# Ativação automática após geração do PIX
asyncio.create_task(remarketing_system.iniciar_campanha_remarketing(
    user_id=str(user_id),
    payment_id=payment_id,
    valor_original=valor,
    pack_name=nome
))
```

### 2. Fluxo de Execução
1. **Usuário gera PIX** → Sistema detecta automaticamente
2. **Timer 5min** → Envia vídeo com 50% desconto
3. **Timer 10min** → Envia imagem com oferta alternativa
4. **Logs detalhados** → Registra todas as ações

## 📊 Mensagens de Remarketing

### 🎬 Primeira Mensagem (5 minutos)
```
🔥 OFERTA RELÂMPAGO! 🔥

Ei! Vi que você estava interessado no nosso pack premium...

💥 QUE TAL 50% DE DESCONTO?

Por apenas R$ 9,95 você leva TUDO que estava por R$ 19,90!

⏰ Essa oferta é LIMITADA e só vale pelos próximos minutos!

🎁 O que você vai receber:
✅ Pack completo premium
✅ Conteúdo exclusivo
✅ Acesso imediato
✅ Suporte VIP

💳 Clique aqui para garantir: [LINK_PAGAMENTO]

⚡ NÃO PERCA! Só restam poucas vagas!
```

### 🖼️ Segunda Mensagem (10 minutos)
```
🚨 ÚLTIMA CHANCE! 🚨

Olha... eu realmente não queria que você perdesse essa oportunidade!

💸 OFERTA FINAL: 60% OFF!

De R$ 19,90 por apenas R$ 7,96!

🔥 ISSO MESMO! Menos de 8 reais!

⏳ Esta é literalmente a ÚLTIMA chance!
Em 5 minutos essa oferta EXPIRA para sempre!

🎯 Por que você deveria aproveitar AGORA:
• Preço NUNCA mais será tão baixo
• Conteúdo premium completo
• Acesso vitalício
• Garantia de satisfação

💥 CLIQUE AGORA: [LINK_PAGAMENTO]

⚠️ Depois não diga que não avisei! 😉
```

## ⚙️ Configuração

### Variáveis de Ambiente
```bash
# .env
TELEGRAM_BOT_TOKEN=seu_token_aqui
PUSHINPAY_API_KEY=sua_chave_api
UTMIFY_API_TOKEN=seu_token_utmify
```

### Dependências
```python
# requirements.txt
python-telegram-bot>=20.0
aiofiles>=23.0
aiohttp>=3.8
requests>=2.28
python-dotenv>=1.0
```

## 📈 Métricas e Monitoramento

### Logs Automáticos
- ✅ Campanhas iniciadas
- 📤 Mensagens enviadas
- ❌ Erros de envio
- ⏱️ Tempos de execução
- 👤 Dados do usuário

### Exemplo de Log
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "123456789",
  "payment_id": "pix_abc123",
  "action": "video_sent",
  "pack_name": "Pack Premium",
  "valor_original": 19.90,
  "desconto_oferecido": 50,
  "status": "success"
}
```

## 🎨 Personalização

### Modificar Textos
```python
# Em sistema_remarketing_pix.py
def gerar_texto_video_remarketing(self, pack_name, valor_original, desconto):
    # Personalize aqui os textos do vídeo
    return texto_personalizado

def gerar_texto_imagem_remarketing(self, pack_name, valor_original, desconto):
    # Personalize aqui os textos da imagem
    return texto_personalizado
```

### Alterar Timings
```python
# Modificar intervalos de tempo
VIDEO_DELAY = 300  # 5 minutos em segundos
IMAGEM_DELAY = 600  # 10 minutos em segundos
```

### Trocar Mídias
1. Substitua `media/1.mp4` pelo seu vídeo
2. Substitua `media/2.jpg` pela sua imagem
3. Mantenha os nomes dos arquivos

## 🔧 Troubleshooting

### Problemas Comuns

#### ❌ Sistema não inicia
```bash
# Verificar token do bot
echo $TELEGRAM_BOT_TOKEN

# Verificar logs
tail -f logs/remarketing.log
```

#### ❌ Mensagens não são enviadas
- Verificar se o bot tem permissão para enviar mídias
- Confirmar se os arquivos de mídia existem
- Checar se o user_id é válido

#### ❌ Arquivos de mídia não encontrados
```bash
# Verificar se existem
ls -la media/

# Verificar permissões
chmod 644 media/*
```

### Logs de Debug
```python
# Ativar logs detalhados
logging.basicConfig(level=logging.DEBUG)
```

## 📋 Checklist de Implementação

### ✅ Pré-requisitos
- [ ] Token do bot Telegram configurado
- [ ] Arquivos de mídia (`1.mp4`, `2.jpg`) no lugar
- [ ] Dependências Python instaladas
- [ ] Variáveis de ambiente configuradas

### ✅ Testes
- [ ] Gerar PIX de teste
- [ ] Verificar se campanha inicia automaticamente
- [ ] Confirmar envio do vídeo em 5 minutos
- [ ] Confirmar envio da imagem em 10 minutos
- [ ] Verificar logs de execução

### ✅ Produção
- [ ] Sistema integrado ao bot principal
- [ ] Monitoramento ativo
- [ ] Backup dos arquivos de mídia
- [ ] Documentação atualizada

## 🚀 Próximos Passos

### Melhorias Futuras
1. **A/B Testing**: Testar diferentes textos e ofertas
2. **Segmentação**: Campanhas personalizadas por perfil
3. **Analytics**: Dashboard de conversão
4. **Automação**: Ajuste automático de descontos
5. **Integração**: CRM e ferramentas de marketing

### Expansões Possíveis
- 📧 Email marketing integrado
- 📱 Push notifications
- 🎯 Retargeting avançado
- 📊 Relatórios detalhados
- 🤖 IA para otimização de textos

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte os logs em `logs/remarketing.log`
2. Verifique a documentação técnica
3. Teste em ambiente de desenvolvimento primeiro
4. Monitore métricas de conversão

---

**🎯 Objetivo**: Maximizar conversões através de remarketing automatizado e persuasivo.

**⚡ Resultado**: Aumento significativo na taxa de conversão de PIX gerados para vendas efetivadas.