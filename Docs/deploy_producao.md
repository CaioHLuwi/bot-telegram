# 🚀 Deploy em Produção - Bot Kyoko 24/7

## 🎯 Como Manter o Bot Rodando 24/7

### Opção 1: VPS/Servidor (Recomendado)

#### 1. Contratar um VPS
**Provedores Recomendados:**
- **DigitalOcean** - A partir de $5/mês
- **Vultr** - A partir de $2.50/mês
- **Linode** - A partir de $5/mês
- **AWS EC2** - Nível gratuito disponível
- **Google Cloud** - Créditos gratuitos

**Especificações Mínimas:**
- 1GB RAM
- 1 vCPU
- 25GB SSD
- Ubuntu 20.04 LTS

#### 2. Configurar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3 python3-pip git -y

# Clonar o projeto
git clone <seu-repositorio>
cd bot-packs

# Instalar dependências
pip3 install -r requirements.txt

# Configurar variáveis de ambiente
nano .env
# Adicionar: BOT_TOKEN=seu_token_aqui
```

#### 3. Usar Screen ou Tmux (Método Simples)

```bash
# Instalar screen
sudo apt install screen -y

# Criar sessão para o bot
screen -S bot-kyoko

# Dentro da sessão, rodar o bot
python3 bot.py

# Sair da sessão (bot continua rodando)
# Pressione: Ctrl + A, depois D

# Para voltar à sessão
screen -r bot-kyoko

# Para listar sessões
screen -ls
```

#### 4. Usar Systemd (Método Profissional)

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/bot-kyoko.service
```

**Conteúdo do arquivo:**
```ini
[Unit]
Description=Bot Kyoko Telegram
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bot-packs
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 /home/ubuntu/bot-packs/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar e iniciar o serviço
sudo systemctl daemon-reload
sudo systemctl enable bot-kyoko
sudo systemctl start bot-kyoko

# Verificar status
sudo systemctl status bot-kyoko

# Ver logs
sudo journalctl -u bot-kyoko -f
```

### Opção 2: Heroku (Gratuito com Limitações)

#### 1. Preparar Arquivos

**Criar `Procfile`:**
```
worker: python bot.py
```

**Criar `runtime.txt`:**
```
python-3.9.16
```

#### 2. Deploy no Heroku

```bash
# Instalar Heroku CLI
# Fazer login
heroku login

# Criar app
heroku create bot-kyoko-seu-nome

# Configurar variável de ambiente
heroku config:set BOT_TOKEN=seu_token_aqui

# Deploy
git add .
git commit -m "Deploy para Heroku"
git push heroku main

# Ativar worker
heroku ps:scale worker=1
```

### Opção 3: Raspberry Pi (Casa)

#### Vantagens:
- Custo baixo (uma vez)
- Controle total
- Sem mensalidades

#### Configuração:
```bash
# Instalar Raspberry Pi OS
# Configurar SSH e WiFi
# Seguir passos similares ao VPS

# Para auto-inicialização
sudo nano /etc/rc.local
# Adicionar antes de "exit 0":
cd /home/pi/bot-packs && python3 bot.py &
```

## 📊 Como Usar o Comando /metricas

### 1. No Telegram

**Onde usar:**
- Diretamente no chat privado com o bot
- Em qualquer conversa onde o bot esteja presente

**Como usar:**
1. Abra o Telegram
2. Vá para o chat do seu bot
3. Digite: `/metricas`
4. Pressione Enter

### 2. Exemplo de Uso

```
Você: /metricas

Bot Kyoko: 📊 MÉTRICAS DO BOT KYOKO

🎯 CONVERSÃO GERAL
• Total de conversas: 127
• Total de pagamentos: 34
• Taxa de conversão: 26.77%
• Receita total: R$ 387.30
• Ticket médio: R$ 11.39

💰 VENDAS POR PACK
• Pack R$ 12,90: 22 vendas
• Pack R$ 5,00: 12 vendas

📅 ÚLTIMOS 7 DIAS
• 2025-01-20: 15 conversas, 4 pagamentos, R$ 46.60
• 2025-01-21: 23 conversas, 7 pagamentos, R$ 85.30
• 2025-01-22: 18 conversas, 5 pagamentos, R$ 59.50

🕐 HOJE POR HORA
• 09h: 3 conversas
• 14h: 8 conversas
• 19h: 12 conversas
```

### 3. Interpretando os Dados

**Taxa de Conversão:**
- ✅ **Excelente**: Acima de 25%
- 🟡 **Boa**: 15-25%
- 🔴 **Precisa melhorar**: Abaixo de 15%

**Ticket Médio:**
- Próximo a R$ 12,90 = Mais vendas do pack completo
- Próximo a R$ 5,00 = Mais vendas com desconto
- Entre R$ 8-10 = Equilíbrio bom

**Horários de Pico:**
- Use para saber quando promover o bot
- Foque marketing nos horários com mais atividade

## 🔧 Monitoramento e Manutenção

### 1. Verificar se o Bot está Online

**Método 1: Comando de Status**
```bash
# No servidor
sudo systemctl status bot-kyoko
```

**Método 2: Teste Manual**
- Envie uma mensagem para o bot
- Se responder = está funcionando
- Se não responder = verificar logs

### 2. Ver Logs de Erro

```bash
# Systemd
sudo journalctl -u bot-kyoko -f

# Screen
screen -r bot-kyoko

# Arquivo de log (se configurado)
tail -f bot.log
```

### 3. Reiniciar o Bot

```bash
# Systemd
sudo systemctl restart bot-kyoko

# Screen
screen -r bot-kyoko
# Ctrl+C para parar
# python3 bot.py para reiniciar
```

## 🚨 Resolução de Problemas

### Bot Para de Responder

1. **Verificar conexão com internet**
2. **Verificar se o processo está rodando**
3. **Verificar logs de erro**
4. **Reiniciar o serviço**

### Erro "Conflict: terminated by other getUpdates"

```bash
# Parar todas as instâncias
sudo pkill -f bot.py

# Aguardar 30 segundos
sleep 30

# Reiniciar
sudo systemctl start bot-kyoko
```

### Métricas Não Funcionam

1. **Verificar se o arquivo metrics.py existe**
2. **Verificar permissões de escrita**
3. **Verificar se bot_metrics.json foi criado**

## 💡 Dicas Importantes

### Segurança
- ✅ Nunca compartilhe seu BOT_TOKEN
- ✅ Use firewall no servidor
- ✅ Mantenha o sistema atualizado
- ✅ Faça backups regulares

### Performance
- 📊 Monitore uso de CPU e RAM
- 📊 Use `/metricas` diariamente
- 📊 Analise horários de pico
- 📊 Otimize baseado nos dados

### Backup
```bash
# Backup dos dados
cp bot_metrics.json backup_metrics_$(date +%Y%m%d).json

# Backup do código
git add . && git commit -m "Backup $(date)"
git push
```

---

**🎯 Resumo Rápido:**
1. **Para 24/7**: Use VPS + Systemd (mais confiável)
2. **Para métricas**: Digite `/metricas` no chat do bot
3. **Para monitorar**: Use logs e teste manual
4. **Para problemas**: Reinicie o serviço

**💰 Custo estimado para 24/7**: $2.50-5.00/mês (VPS básico)