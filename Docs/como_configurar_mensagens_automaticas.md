# 🚀 Como Configurar Mensagens Automáticas - Guia Simples

## 📱 O que são as Mensagens Automáticas?

As mensagens automáticas fazem o bot enviar a seguinte mensagem promocional **a cada 1 hora** no grupo "Kyoko Packs 👄❤️‍🔥":

> "Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor"

Isso ajuda a manter o grupo ativo e promover as vendas automaticamente, sem você precisar ficar enviando mensagens manualmente.

## 🔧 Passo a Passo para Configurar

### Passo 1: Adicionar o Bot ao Grupo

1. **Abra o grupo** "Kyoko Packs 👄❤️‍🔥" no Telegram
2. **Clique no nome do grupo** (no topo)
3. **Clique em "Adicionar Membros"**
4. **Procure pelo seu bot** (o nome que você deu quando criou)
5. **Adicione o bot ao grupo**
6. **Torne o bot administrador** (recomendado):
   - Clique no bot na lista de membros
   - Clique em "Promover a Administrador"
   - Marque apenas "Enviar Mensagens"

### Passo 2: Obter o ID do Grupo

1. **No grupo**, digite o comando: `/groupid`
2. **O bot vai responder** com algo como:
   ```
   📋 ID deste grupo: -1001234567890
   
   Copie este ID e adicione no arquivo .env como GROUP_CHAT_ID para ativar as mensagens automáticas.
   ```
3. **Copie o número** (exemplo: `-1001234567890`)

### Passo 3: Configurar o Arquivo .env

1. **Abra o arquivo `.env`** na pasta do bot
2. **Procure pela linha** que começa com `GROUP_CHAT_ID=`
3. **Substitua o número** pelo ID que você copiou:
   ```
   GROUP_CHAT_ID=-1001234567890
   ```
   *(Use o ID real do seu grupo)*
4. **Salve o arquivo**

### Passo 4: Reiniciar o Bot

1. **Pare o bot** (se estiver rodando)
2. **Inicie o bot novamente**
3. **Verifique se apareceu a mensagem**:
   ```
   Mensagens automáticas configuradas para o grupo -1001234567890 (a cada 1 hora)
   ```

## ✅ Como Saber se Está Funcionando

### Sinais de Sucesso:

1. **No console/terminal**, você verá:
   ```
   Mensagens automáticas configuradas para o grupo [ID] (a cada 1 hora)
   ```

2. **Após 1 minuto**, a primeira mensagem será enviada

3. **A cada hora**, uma nova mensagem promocional aparecerá no grupo

4. **Nos logs**, você verá:
   ```
   Mensagem promocional enviada para o grupo [ID]
   ```

### Se Não Estiver Funcionando:

1. **Verifique se o ID está correto** no arquivo `.env`
2. **Confirme se o bot é administrador** do grupo
3. **Reinicie o bot** após fazer alterações
4. **Verifique os logs** para mensagens de erro

## 🎯 Perguntas Frequentes

### ❓ Posso mudar a mensagem?
**Sim!** Edite o arquivo `bot.py`, procure por:
```python
promotional_text = "Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor"
```
E substitua pela mensagem que desejar.

### ❓ Posso mudar o horário?
**Sim!** No arquivo `bot.py`, procure por:
```python
interval=3600,  # 3600 segundos = 1 hora
```
E altere para:
- `1800` = 30 minutos
- `7200` = 2 horas
- `900` = 15 minutos

### ❓ Posso enviar para vários grupos?
**Sim!** Você pode configurar múltiplos grupos editando o código. Consulte a documentação técnica para detalhes.

### ❓ Como parar as mensagens automáticas?
**Opção 1:** Remova ou comente a linha `GROUP_CHAT_ID=` no arquivo `.env`
**Opção 2:** Remova o bot do grupo
**Opção 3:** Pare o bot completamente

### ❓ O bot vai enviar mensagens 24 horas?
**Sim!** Enquanto o bot estiver rodando, ele enviará mensagens a cada hora, 24/7.

## 🛡️ Dicas Importantes

### ✅ Faça:
- Mantenha o bot como administrador do grupo
- Monitore se as mensagens estão sendo bem recebidas
- Faça backup do arquivo `.env`
- Teste primeiro em um grupo de teste

### ❌ Não faça:
- Não compartilhe o ID do grupo publicamente
- Não remova o bot do grupo se quiser manter as mensagens
- Não altere outros valores no arquivo `.env` sem saber o que faz

## 📞 Precisa de Ajuda?

Se algo não estiver funcionando:

1. **Verifique os logs** do bot para mensagens de erro
2. **Confirme todas as configurações** seguindo este guia
3. **Teste o comando `/groupid`** no grupo
4. **Reinicie o bot** após qualquer alteração

---

**🎉 Pronto! Agora seu bot enviará mensagens promocionais automaticamente a cada hora no grupo!**