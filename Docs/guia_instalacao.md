# 🚀 Guia de Instalação - Bot Kyoko

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+)
- ✅ macOS 10.15+

### Software Necessário
- ✅ Python 3.9 ou superior
- ✅ pip (gerenciador de pacotes Python)
- ✅ Git (opcional, para clonagem)

## 🔧 Instalação Passo a Passo

### 1. Preparação do Ambiente

#### Windows (WSL Ubuntu)
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Verificar instalação
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3 python3-pip python3-venv git -y

# Verificar instalação
python3 --version
pip3 --version
```

#### macOS
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python3

# Verificar instalação
python3 --version
pip3 --version
```

### 2. Configuração do Bot no Telegram

#### Criar Bot no BotFather
1. Abra o Telegram e procure por `@BotFather`
2. Inicie conversa com `/start`
3. Digite `/newbot` para criar novo bot
4. **Nome do bot**: `Kyoko uwu`
5. **Username**: `kyoko_pack_bot` (ou outro disponível)
6. **Copie o token** fornecido (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Configurar Foto do Perfil
1. No BotFather, digite `/setuserpic`
2. Selecione seu bot
3. Envie a foto `bot-foot.png`

#### Configurar Descrição
1. Digite `/setdescription`
2. Selecione seu bot
3. Digite: `Bot da Kyoko para packs exclusivos 💕`

### 3. Instalação do Projeto

#### Opção A: Download Direto
1. Baixe todos os arquivos do projeto
2. Extraia para uma pasta (ex: `bot-kyoko`)
3. Navegue até a pasta:
```bash
cd bot-kyoko
```

#### Opção B: Git Clone (se disponível)
```bash
git clone <url-do-repositorio> bot-kyoko
cd bot-kyoko
```

### 4. Configuração do Ambiente Python

#### Criar Ambiente Virtual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### Instalar Dependências
```bash
# Instalar pacotes necessários
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 5. Configuração das Variáveis

#### Editar arquivo .env
```bash
# Abrir arquivo para edição
nano .env

# Ou usar editor de texto preferido
code .env  # VS Code
gedit .env # Linux GUI
notepad .env # Windows
```

#### Configurar Token
```env
# Substituir SEU_TOKEN_AQUI pelo token do BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Manter outras configurações
PUSHIN_PAY_TOKEN=39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5
CONTEUDO_LINK=https://kyokoleticia.site/conteudo
```

### 6. Adicionar Arquivos de Mídia

#### Estrutura da Pasta fotos/
```
fotos/
├── bot-foot.png  # ✅ Já incluído
├── 1.jpg         # ❌ Adicionar
├── 2.jpg         # ❌ Adicionar
├── 4.jpg         # ❌ Adicionar
├── 1.mp4         # ❌ Adicionar
└── audio.mp3     # ❌ Opcional
```

#### Adicionar Arquivos
1. Copie suas fotos e vídeos para a pasta `fotos/`
2. Renomeie conforme necessário:
   - Primeira foto → `1.jpg`
   - Segunda foto → `2.jpg`
   - Foto de despedida → `4.jpg`
   - Vídeo → `1.mp4`
   - Áudio (opcional) → `audio.mp3`

### 7. Configuração Inicial do Bot

#### Executar Script de Setup
```bash
# Configurar perfil do bot
python setup_bot.py
```

**Saída esperada:**
```
🤖 Configurando Bot Kyoko...

✅ Bot conectado: @kyoko_pack_bot
⚠️  Não foi possível definir a foto do perfil: Forbidden
✅ Comandos configurados

🎉 Bot configurado com sucesso!
Nome: Kyoko uwu
Username: @kyoko_pack_bot
ID: 123456789
```

### 8. Teste Inicial

#### Executar Bot
```bash
# Iniciar bot em modo de desenvolvimento
python bot.py
```

**Saída esperada:**
```
2024-01-15 10:30:00,123 - telegram.ext.Application - INFO - Application started
2024-01-15 10:30:00,124 - __main__ - INFO - Bot iniciado!
```

#### Testar no Telegram
1. Procure seu bot no Telegram pelo username
2. Inicie conversa com `/start`
3. Verifique se recebe a sequência de mensagens
4. Teste os botões interativos

## 🔧 Configuração para Produção

### Linux com Systemd

#### Criar Arquivo de Serviço
```bash
sudo nano /etc/systemd/system/kyoko-bot.service
```

#### Conteúdo do Arquivo
```ini
[Unit]
Description=Kyoko Telegram Bot
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/bot-kyoko
Environment=PATH=/caminho/para/bot-kyoko/venv/bin
ExecStart=/caminho/para/bot-kyoko/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Ativar Serviço
```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar serviço
sudo systemctl enable kyoko-bot

# Iniciar serviço
sudo systemctl start kyoko-bot

# Verificar status
sudo systemctl status kyoko-bot

# Ver logs
sudo journalctl -u kyoko-bot -f
```

### Windows com NSSM

#### Instalar NSSM
1. Baixe NSSM de https://nssm.cc/download
2. Extraia para `C:\nssm`
3. Adicione ao PATH do sistema

#### Criar Serviço
```cmd
# Abrir prompt como administrador
nssm install KyokoBot

# Configurar:
# Path: C:\caminho\para\bot-kyoko\venv\Scripts\python.exe
# Startup directory: C:\caminho\para\bot-kyoko
# Arguments: bot.py

# Iniciar serviço
nssm start KyokoBot
```

### Docker (Opcional)

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  kyoko-bot:
    build: .
    restart: unless-stopped
    volumes:
      - ./fotos:/app/fotos
      - ./logs:/app/logs
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
    env_file:
      - .env
```

#### Executar com Docker
```bash
# Build e start
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## 🔍 Verificação e Troubleshooting

### Checklist de Verificação

- [ ] Python 3.9+ instalado
- [ ] Dependências instaladas (`pip list`)
- [ ] Token do bot configurado no `.env`
- [ ] Bot criado no BotFather
- [ ] Arquivos de mídia na pasta `fotos/`
- [ ] Script `setup_bot.py` executado com sucesso
- [ ] Bot responde no Telegram

### Problemas Comuns

#### Bot não responde
```bash
# Verificar se o bot está rodando
ps aux | grep python

# Verificar logs
tail -f bot.log

# Testar token
curl "https://api.telegram.org/bot<SEU_TOKEN>/getMe"
```

#### Erro de dependências
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar versão do Python
python3 --version

# Verificar ambiente virtual
which python
```

#### Arquivos de mídia não encontrados
```bash
# Verificar estrutura de pastas
ls -la fotos/

# Verificar permissões
chmod 644 fotos/*
```

#### Erro de API Pushin Pay
```bash
# Testar conectividade
curl -H "Authorization: Bearer 39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5" \
     https://api.pushinpay.com.br/api/payments
```

### Logs e Monitoramento

#### Localização dos Logs
- **Desenvolvimento**: Console/terminal
- **Produção**: `/var/log/kyoko-bot.log`
- **Docker**: `docker-compose logs`

#### Monitorar em Tempo Real
```bash
# Linux
tail -f /var/log/kyoko-bot.log

# Systemd
journalctl -u kyoko-bot -f

# Docker
docker-compose logs -f kyoko-bot
```

## 📞 Suporte

### Recursos de Ajuda
1. **Documentação**: Consulte `README.md`
2. **Logs**: Sempre verifique os logs primeiro
3. **Telegram Bot API**: https://core.telegram.org/bots/api
4. **Python Telegram Bot**: https://python-telegram-bot.readthedocs.io/

### Informações para Suporte
Ao solicitar ajuda, inclua:
- Sistema operacional
- Versão do Python
- Logs de erro
- Passos que levaram ao problema
- Configurações (sem tokens)

## 🔄 Atualizações

### Processo de Atualização
1. **Backup**: Faça backup dos dados
2. **Parar**: Pare o bot
3. **Atualizar**: Baixe nova versão
4. **Testar**: Teste em desenvolvimento
5. **Deploy**: Atualize produção

### Versionamento
- **Major**: Mudanças incompatíveis
- **Minor**: Novas funcionalidades
- **Patch**: Correções de bugs

### Changelog
Sempre consulte o changelog antes de atualizar para entender as mudanças e possíveis impactos.