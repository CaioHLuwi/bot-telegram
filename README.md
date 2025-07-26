# 🤖 Bot Kyoko - Chatbot para Telegram

Bot automatizado para Telegram que simula conversas de vendas de packs com integração ao sistema de pagamento PIX via Pushin Pay.

## 📋 Funcionalidades

- ✅ Conversa automatizada com sequência de mensagens
- ✅ Envio de fotos, vídeos e áudios
- ✅ Sistema de botões interativos
- ✅ Integração com API Pushin Pay para PIX
- ✅ Verificação automática de pagamentos
- ✅ Fluxo de desconto automático
- ✅ Timeout para perguntas (2 minutos)

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.9 ou superior
- Conta no Telegram
- Token de bot do BotFather
- Conta na Pushin Pay (opcional para testes)

### 2. Configuração do Bot no Telegram

1. Acesse [@BotFather](https://t.me/BotFather) no Telegram
2. Digite `/newbot` para criar um novo bot
3. Escolha um nome: `Kyoko uwu`
4. Escolha um username único (ex: `kyoko_pack_bot`)
5. Copie o token fornecido

### 3. Instalação das Dependências

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 4. Configuração

1. Edite o arquivo `.env`:
```env
BOT_TOKEN=SEU_TOKEN_DO_BOTFATHER_AQUI
```

2. Configure a foto do perfil:
   - A foto `bot-foot.png` já está na pasta `fotos/`
   - Execute o script de configuração:
```bash
python setup_bot.py
```

### 5. Adicionar Mídias

Coloque os arquivos na pasta `fotos/`:
- `1.jpg` - Primeira foto do pack
- `2.jpg` - Segunda foto do pack  
- `4.jpg` - Foto de despedida
- `1.mp4` - Vídeo do pack
- `audio.mp3` - Áudio (opcional)

## 🎯 Como Usar

### Iniciar o Bot

```bash
python bot.py
```

### Comandos Disponíveis

- `/start` - Inicia a conversa
- `/oi` - Inicia a conversa
- Qualquer mensagem também inicia a conversa

## 🔄 Fluxo de Conversa

1. **Saudação inicial** - Mensagem de boas-vindas
2. **Apresentação do conteúdo** - Áudio, fotos e vídeo
3. **Oferta principal** - R$ 12,90
4. **Aguarda resposta** - Sim/Não ou botões
5. **Se pergunta** - Aguarda 2 minutos antes dos botões
6. **Se "Sim"** - Gera PIX de R$ 12,90
7. **Se "Não"** - Oferece desconto para R$ 5,00
8. **Pagamento** - Verificação automática via Pushin Pay
9. **Entrega** - Link para download do conteúdo

## 💰 Sistema de Pagamentos

### Pushin Pay Integration

O bot usa a API da Pushin Pay para:
- Gerar códigos PIX automaticamente
- Verificar status dos pagamentos
- Confirmar pagamentos em tempo real

### Valores
- **Pack completo**: R$ 12,90
- **Pack com desconto**: R$ 5,00

## 📁 Estrutura do Projeto

```
bot-packs/
├── bot.py              # Código principal do bot
├── config.py           # Configurações e mensagens
├── setup_bot.py        # Script de configuração
├── requirements.txt    # Dependências Python
├── .env               # Variáveis de ambiente
├── README.md          # Este arquivo
└── fotos/             # Pasta de mídias
    ├── bot-foot.png   # Foto do perfil do bot
    ├── 1.jpg          # Primeira foto (adicionar)
    ├── 2.jpg          # Segunda foto (adicionar)
    ├── 4.jpg          # Foto final (adicionar)
    └── 1.mp4          # Vídeo (adicionar)
```

## ⚙️ Configurações Avançadas

### Personalizar Mensagens

Edite o arquivo `config.py` para alterar:
- Textos das mensagens
- Preços dos packs
- Timing entre mensagens
- Arquivos de mídia

### Logs

O bot gera logs detalhados para:
- Monitorar conversas
- Debug de erros
- Acompanhar pagamentos

## 🔧 Solução de Problemas

### Bot não responde
- Verifique se o token está correto no `.env`
- Confirme que o bot está rodando
- Verifique os logs de erro

### Pagamentos não funcionam
- Verifique a configuração da Pushin Pay
- Confirme se o token da API está válido
- Teste a conectividade com a API

### Mídias não enviam
- Verifique se os arquivos existem na pasta `fotos/`
- Confirme os nomes dos arquivos
- Verifique permissões de leitura

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do bot
2. Consulte a documentação da python-telegram-bot
3. Teste com o BotFather se o bot está ativo

## 🔒 Segurança

- ⚠️ Nunca compartilhe seu token do bot
- ⚠️ Mantenha o arquivo `.env` privado
- ⚠️ Use HTTPS em produção
- ⚠️ Monitore os logs regularmente

## 📄 Licença

Este projeto é para uso pessoal e educacional.