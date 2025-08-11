# 🤖 Bot Letícia Kyoko - Sistema de Menu Interativo

## 📋 Visão Geral

O Bot da Letícia Kyoko foi completamente reformulado com um sistema de menu interativo que oferece 5 opções de packs com preços diferenciados. A IA mantém a personalidade sedutora e carinhosa da Letícia, apresentando as opções de forma natural e criando PIX automaticamente.

## 🎯 Funcionalidades Principais

### 💕 Menu de Packs Disponíveis

1. **Pack Básico - R$ 9,90**
   - 10 fotinhas bem safadinhas
   - 3 vídeos mostrando tudo
   - Perfeito para começar

2. **Pack Médio - R$ 15,90**
   - 20 fotinhas em poses provocantes
   - 6 vídeos mostrando tudo
   - Mais conteúdo para diversão

3. **Pack Completo - R$ 19,90**
   - 30 fotinhas bem explícitas
   - 12 vídeos mostrando tudinho
   - Pack mais completo e gostoso

4. **Vídeochamada - R$ 49,90**
   - 5 minutos só vocês dois
   - Conversa bem íntima e gostosa
   - Experiência personalizada

5. **Programa - R$ 249,90**
   - 1 noite inteira
   - Experiência completa e inesquecível
   - Tudo que sempre sonhou

## 🚀 Como Usar

### Opção 1: Bot Novo (Recomendado)
```bash
python bot_leticia_menu.py
```

### Opção 2: Bot Original (Atualizado)
```bash
python bot.py
```

## 🔧 Configuração

### 1. Variáveis de Ambiente
```bash
# .env
BOT_TOKEN=seu_token_do_telegram
GROUP_CHAT_ID=id_do_grupo
CONTEUDO_LINK=https://kyokoleticia.site/conteudo
```

### 2. Token Pushinpay Atualizado
```
42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1
```

### 3. Dependências
```bash
pip install -r requirements.txt
```

## 📱 Fluxo de Conversa

### 1. Usuário Inicia Conversa
```
Usuário: "Oi"
```

### 2. Letícia Apresenta Menu
```
Letícia: "Oi gatinho, tudo bem? Que bom te ver aqui comigo 😘 
Sou a Letícia Kyoko e tenho várias opções deliciosas para você se divertir...

🔥 PACKS DISPONÍVEIS:

💕 Pack Básico - R$ 9,90
💖 Pack Médio - R$ 15,90
🔥 Pack Completo - R$ 19,90
📹 Vídeochamada - R$ 49,90
🌙 Programa - R$ 249,90

Qual desses te deixa mais interessado, mozinho? 😏"
```

### 3. Usuário Escolhe Pack
```
[Botões Interativos]
💕 Pack Básico - R$ 9,90
💖 Pack Médio - R$ 15,90
🔥 Pack Completo - R$ 19,90
📹 Vídeochamada - R$ 49,90
🌙 Programa - R$ 249,90
```

### 4. PIX Gerado Automaticamente
```
Letícia: "Ótima escolha gatinho! O Pack Completo de R$ 19,90 é uma delícia mesmo 😏

30 fotinhas bem explícitas e 12 vídeos mostrando tudinho

🔸 Código PIX:
`00020126580014BR.GOV.BCB.PIX...`

🔸 Valor: R$ 19,90
🔸 ID: `pix_123456`

É só copiar o código PIX e colar no seu banco! O pagamento é instantâneo e te mando todo o conteúdo assim que confirmar ❤️"
```

## 🛠️ Arquivos Principais

### 📁 Estrutura do Projeto
```
bot-packs/
├── bot_leticia_menu.py          # Bot novo com sistema de menu
├── bot.py                       # Bot original (token atualizado)
├── config.py                    # Configurações e preços
├── requirements.txt             # Dependências
├── test_curl_leticia.sh         # Testes CURL
├── Docs/
│   ├── leticia_ia_menu_packs_curl.md
│   ├── system_message_leticia_kyoko.md
│   └── integracao_ia_pushinpay_pix.md
└── fotos/                       # Imagens do bot
```

### 📋 Configurações (config.py)
```python
# Preços dos Packs da Letícia
PRICES = {
    'pack_basico': 9.90,      # 10 fotos, 3 vídeos
    'pack_medio': 15.90,      # 20 fotos, 6 vídeos  
    'pack_completo': 19.90,   # 30 fotos, 12 vídeos
    'videochamada': 49.90,    # 5 minutos
    'programa': 249.90        # 1 noite
}

# API Pushin Pay
PUSHIN_PAY_CONFIG = {
    'token': '42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1',
    'base_url': 'https://api.pushinpay.com.br/api'
}
```

## 🧪 Testes

### Testar API com CURL
```bash
# Dar permissão de execução
chmod +x test_curl_leticia.sh

# Executar testes
./test_curl_leticia.sh
```

### Testar Bot Localmente
```bash
# Iniciar bot
python bot_leticia_menu.py

# Comandos disponíveis
/start    # Iniciar conversa
/menu     # Mostrar menu
/oi       # Saudação
/metricas # Ver estatísticas
/saude    # Status do bot
```

## 📊 Comandos Administrativos

### `/metricas`
```
📊 Métricas do Bot Letícia Kyoko

👥 Usuários únicos: 150
💬 Total de conversas: 300
🔄 Conversas ativas: 25
💰 PIX gerados: 45
✅ Pagamentos confirmados: 12
📈 Taxa de conversão: 26.7%
```

### `/saude`
```
🏥 Status do Bot Letícia Kyoko

🤖 Bot: ✅ Online
🔗 API Pushin Pay: ✅ Online
💾 Estados ativos: 25
🕐 Uptime: 15/01/2024 14:30

📋 Configurações:
• Token: ✅ Configurado
• Link conteúdo: ✅ Configurado
```

## 🔒 Segurança

### ✅ Boas Práticas Implementadas
- Token seguro e atualizado
- Validação de entrada do usuário
- Logs detalhados para auditoria
- Rate limiting para evitar spam
- Sanitização de dados

### 🚫 Nunca Fazer
- Commitar tokens no repositório
- Expor credenciais em logs
- Permitir valores negativos
- Ignorar validações de segurança

## 🚀 Deploy

### Railway (Recomendado)
```bash
# Variáveis necessárias no Railway:
BOT_TOKEN=seu_token_telegram
PUSHIN_PAY_TOKEN=42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1
CONTEUDO_LINK=https://kyokoleticia.site/conteudo
GROUP_CHAT_ID=id_do_grupo
```

### Heroku
```bash
# Procfile
web: python bot_leticia_menu.py
```

## 📈 Melhorias Futuras

### 🎯 Próximas Funcionalidades
- [ ] Webhook para confirmação automática de pagamento
- [ ] Sistema de cupons de desconto
- [ ] Integração com múltiplas APIs de pagamento
- [ ] Dashboard web para métricas
- [ ] Sistema de afiliados
- [ ] Chat em grupo automatizado
- [ ] Notificações push
- [ ] Analytics avançados

### 🔧 Otimizações Técnicas
- [ ] Cache Redis para estados
- [ ] Database PostgreSQL
- [ ] Queue system para processamento
- [ ] Load balancing
- [ ] Monitoring com Prometheus
- [ ] CI/CD pipeline

## 🆘 Troubleshooting

### ❌ Problemas Comuns

**Bot não responde:**
```bash
# Verificar token
echo $BOT_TOKEN

# Verificar logs
tail -f bot.log

# Testar conexão
curl -X GET "https://api.telegram.org/bot$BOT_TOKEN/getMe"
```

**PIX não é gerado:**
```bash
# Testar API
curl -X POST "https://api.pushinpay.com.br/api/pix/cashIn" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Content-Type: application/json" \
  -d '{"value": 1990}'
```

**Erro de dependências:**
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar versão Python
python --version  # Deve ser 3.8+
```

## 📞 Suporte

- **Telegram:** @leticiakyoko
- **Documentação:** `/Docs/`
- **Issues:** GitHub Issues
- **Logs:** Verificar arquivo `bot.log`

---

**🎉 O Bot da Letícia Kyoko está pronto para seduzir e vender! 💕**

*Desenvolvido com ❤️ para maximizar conversões e proporcionar a melhor experiência para os clientes da Letícia.*