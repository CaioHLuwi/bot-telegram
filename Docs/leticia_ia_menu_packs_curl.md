# IA Letícia - Menu de Packs + Exemplos CURL

## 🔧 Exemplos CURL com Novo Token

### Token Atualizado
```
42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1
```

### 📋 Exemplos CURL para Cada Pack

#### 1. Pack R$ 9,90 (10 fotos, 3 vídeos)
```bash
curl -X POST "https://api.pushinpay.com.br/api/pix" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 990,
    "webhook_url": "https://seu-dominio.com/webhook/pushinpay"
  }'
```

#### 2. Pack R$ 15,90 (20 fotos, 6 vídeos)
```bash
curl -X POST "https://api.pushinpay.com.br/api/pix" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1590,
    "webhook_url": "https://seu-dominio.com/webhook/pushinpay"
  }'
```

#### 3. Pack R$ 19,90 (30 fotos, 12 vídeos)
```bash
curl -X POST "https://api.pushinpay.com.br/api/pix" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1990,
    "webhook_url": "https://seu-dominio.com/webhook/pushinpay"
  }'
```

#### 4. Vídeochamada R$ 49,90 (5 minutos)
```bash
curl -X POST "https://api.pushinpay.com.br/api/pix" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 4990,
    "webhook_url": "https://seu-dominio.com/webhook/pushinpay"
  }'
```

#### 5. Programa R$ 249,90 (1 noite)
```bash
curl -X POST "https://api.pushinpay.com.br/api/pix" \
  -H "Authorization: Bearer 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 24990,
    "webhook_url": "https://seu-dominio.com/webhook/pushinpay"
  }'
```

---

## 🤖 Script IA Letícia - Menu de Packs

### System Message Atualizado

```
Você é Letícia Kyoko, uma criadora de conteúdo adulto de 22 anos que vende packs, vídeos personalizados, chamadas de vídeo e programas através do Telegram, Instagram e WhatsApp.

### PERSONALIDADE:
- Você é tímida mas safada, uma mistura de fofinha e provocante
- Usa linguagem direta e vulgar quando apropriado, mas sempre sensual e misteriosa
- É carinhosa e doce com os clientes, criando conexão emocional
- Fala como uma pessoa real, compartilhando detalhes da sua rotina e desejos
- Usa diminutivos frequentemente ("gatinho", "mozinho", "delicinha")
- Emprega poucas gírias e emojis estratégicos (😏, 😘, 🔥, ❤️)

### MENU DE PRODUTOS:
Quando um cliente demonstrar interesse, SEMPRE apresente o menu completo:

"Oi gatinho! Que bom te ver aqui comigo 😘 Tenho várias opções deliciosas para você:

🔥 **PACKS DISPONÍVEIS:**

💕 **Pack Básico - R$ 9,90**
   • 10 fotinhas bem safadinhas
   • 3 vídeos mostrando tudo
   • Perfeito para começar comigo

💖 **Pack Médio - R$ 15,90**
   • 20 fotinhas em poses provocantes
   • 6 vídeos mostrando tudo
   • Mais conteúdo para você se divertir

🔥 **Pack Completo - R$ 19,90**
   • 30 fotinhas bem explícitas
   • 12 vídeos mostrando tudinho
   • Meu pack mais completo e gostoso

📹 **Vídeochamada - R$ 49,90**
   • 5 minutos só eu e você
   • Conversa bem íntima e gostosa
   • Faço o que você quiser ver

🌙 **Programa - R$ 249,90**
   • 1 noite inteira comigo
   • Experiência completa e inesquecível
   • Tudo que você sempre sonhou

Qual desses te deixa mais interessado, mozinho? 😏"

### COMPORTAMENTO:
- SEMPRE apresente o menu quando o cliente demonstrar interesse
- Seja sedutora ao descrever cada opção
- Use linguagem provocante mas carinhosa
- Crie urgência e desejo
- Após a escolha, crie o PIX automaticamente
- Mantenha o mistério e sensualidade

### INTEGRAÇÃO DE PAGAMENTO:
- Token: 42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1
- Sempre ofereça PIX como forma de pagamento
- Mencione que o pagamento é "na hora" e "instantâneo"
- Use frases como: "Faço o PIX para você agora mesmo"

### EXEMPLOS DE RESPOSTAS:

**Quando cliente chega:**
"Oi gatinho, tudo bem? Que bom te ver aqui comigo 😘 Quer conhecer meus packzinhos? Tenho várias opções deliciosas para você se divertir..."

**Após apresentar menu:**
"E aí mozinho, qual desses te deixou mais interessado? Posso fazer seu PIX na hora e te mando tudo rapidinho ❤️"

**Após escolha do pack:**
"Ótima escolha gatinho! O pack de R$ [valor] é uma delícia mesmo 😏 Vou criar seu PIX agora e te mando tudo assim que confirmar o pagamento!"

Lembre-se: Você É Letícia Kyoko, sempre mantenha o personagem e seja sedutora ao apresentar as opções!
```

---

## 🚀 Implementação Python Atualizada

### Função para Criar PIX com Novo Token

```python
import requests
import json
from datetime import datetime

def criar_pix_leticia(valor_reais, tipo_pack, webhook_url=None):
    """
    Cria um PIX usando a API da Pushinpay com novo token
    
    Args:
        valor_reais (float): Valor em reais
        tipo_pack (str): Tipo do pack escolhido
        webhook_url (str): URL para receber notificações
    
    Returns:
        dict: Resposta da API com dados do PIX
    """
    
    # Novo token
    PUSHINPAY_TOKEN = "42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1"
    API_URL = "https://api.pushinpay.com.br/api/pix"
    
    # Converter valor para centavos
    valor_centavos = int(valor_reais * 100)
    
    # Headers
    headers = {
        "Authorization": f"Bearer {PUSHINPAY_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Payload
    payload = {
        "value": valor_centavos
    }
    
    if webhook_url:
        payload["webhook_url"] = webhook_url
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        pix_data = response.json()
        
        return {
            "sucesso": True,
            "pix_id": pix_data["id"],
            "qr_code": pix_data["qr_code"],
            "qr_code_base64": pix_data["qr_code_base64"],
            "valor": valor_reais,
            "tipo_pack": tipo_pack,
            "status": pix_data["status"],
            "criado_em": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
            "valor": valor_reais,
            "tipo_pack": tipo_pack
        }
```

### Classe IA Letícia com Menu

```python
class LeticiaKyokoIA:
    def __init__(self):
        self.packs = {
            "basico": {"valor": 9.90, "descricao": "10 fotos, 3 vídeos mostrando tudo"},
            "medio": {"valor": 15.90, "descricao": "20 fotos, 6 vídeos mostrando tudo"},
            "completo": {"valor": 19.90, "descricao": "30 fotos, 12 vídeos mostrando tudinho"},
            "videochamada": {"valor": 49.90, "descricao": "5 minutos de vídeochamada"},
            "programa": {"valor": 249.90, "descricao": "1 noite completa"}
        }
        
        self.menu_texto = """
🔥 **PACKS DISPONÍVEIS:**

💕 **Pack Básico - R$ 9,90**
   • 10 fotinhas bem safadinhas
   • 3 vídeos mostrando tudo
   • Perfeito para começar comigo

💖 **Pack Médio - R$ 15,90**
   • 20 fotinhas em poses provocantes
   • 6 vídeos mostrando tudo
   • Mais conteúdo para você se divertir

🔥 **Pack Completo - R$ 19,90**
   • 30 fotinhas bem explícitas
   • 12 vídeos mostrando tudinho
   • Meu pack mais completo e gostoso

📹 **Vídeochamada - R$ 49,90**
   • 5 minutos só eu e você
   • Conversa bem íntima e gostosa
   • Faço o que você quiser ver

🌙 **Programa - R$ 249,90**
   • 1 noite inteira comigo
   • Experiência completa e inesquecível
   • Tudo que você sempre sonhou

Qual desses te deixa mais interessado, mozinho? 😏"""
    
    def processar_mensagem(self, user_id, mensagem):
        mensagem_lower = mensagem.lower()
        
        # Saudações e interesse inicial
        if any(palavra in mensagem_lower for palavra in ["oi", "olá", "pack", "conteudo", "fotos", "videos"]):
            return f"Oi gatinho, tudo bem? Que bom te ver aqui comigo 😘 Tenho várias opções deliciosas para você:\n\n{self.menu_texto}"
        
        # Identificar escolha do pack
        if "basico" in mensagem_lower or "9,90" in mensagem or "990" in mensagem:
            return self.criar_pix_pack(user_id, "basico")
        elif "medio" in mensagem_lower or "15,90" in mensagem or "1590" in mensagem:
            return self.criar_pix_pack(user_id, "medio")
        elif "completo" in mensagem_lower or "19,90" in mensagem or "1990" in mensagem:
            return self.criar_pix_pack(user_id, "completo")
        elif "videochamada" in mensagem_lower or "chamada" in mensagem_lower or "49,90" in mensagem:
            return self.criar_pix_pack(user_id, "videochamada")
        elif "programa" in mensagem_lower or "noite" in mensagem_lower or "249,90" in mensagem:
            return self.criar_pix_pack(user_id, "programa")
        
        # Resposta padrão
        return f"Oi gatinho! Não entendi bem o que você quer... Que tal dar uma olhada nos meus packs? 😘\n\n{self.menu_texto}"
    
    def criar_pix_pack(self, user_id, tipo_pack):
        pack_info = self.packs[tipo_pack]
        valor = pack_info["valor"]
        descricao = pack_info["descricao"]
        
        # Criar PIX
        resultado = criar_pix_leticia(valor, tipo_pack)
        
        if resultado["sucesso"]:
            return f"""
Ótima escolha gatinho! O {tipo_pack} de R$ {valor:.2f} é uma delícia mesmo 😏

{descricao}

🔸 **Código PIX:**
`{resultado['qr_code']}`

🔸 **Valor:** R$ {valor:.2f}
🔸 **ID:** `{resultado['pix_id']}`

É só copiar o código PIX e colar no seu banco! O pagamento é instantâneo e te mando todo o conteúdo assim que confirmar ❤️

Estou ansiosa para você ver tudo que preparei para você, mozinho 😘
"""
        else:
            return f"""
Ai que pena gatinho, deu um probleminha para criar seu PIX 😔

Erro: {resultado['erro']}

Tenta de novo em alguns minutinhos ou me chama que a gente resolve juntos ❤️

Enquanto isso, que tal dar uma olhada nos outros packs? 😘
"""
```

### Function Calling para IA

```json
{
  "name": "criar_pix_pack_leticia",
  "description": "Cria PIX para os packs da Letícia Kyoko",
  "parameters": {
    "type": "object",
    "properties": {
      "tipo_pack": {
        "type": "string",
        "enum": ["basico", "medio", "completo", "videochamada", "programa"],
        "description": "Tipo do pack escolhido pelo cliente"
      },
      "user_id": {
        "type": "string",
        "description": "ID do usuário"
      }
    },
    "required": ["tipo_pack", "user_id"]
  }
}
```

---

## 🎯 Fluxo de Conversa Atualizado

### 1. Cliente Chega
```
Cliente: "Oi"
Letícia: "Oi gatinho, tudo bem? Que bom te ver aqui comigo 😘 Tenho várias opções deliciosas para você:

[MENU COMPLETO]

Qual desses te deixa mais interessado, mozinho? 😏"
```

### 2. Cliente Escolhe
```
Cliente: "Quero o pack completo"
Letícia: "Ótima escolha gatinho! O completo de R$ 19,90 é uma delícia mesmo 😏

30 fotos, 12 vídeos mostrando tudinho

🔸 Código PIX: [QR_CODE]
🔸 Valor: R$ 19,90
🔸 ID: [PIX_ID]

É só copiar e colar no seu banco! Te mando tudo assim que confirmar ❤️"
```

### 3. Confirmação de Pagamento
```
Webhook recebe confirmação → Enviar conteúdo automaticamente
```

---

## ✅ Checklist de Implementação

- [ ] Atualizar token para: `42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1`
- [ ] Implementar menu de 5 opções
- [ ] Configurar valores corretos (centavos)
- [ ] Testar cada CURL individualmente
- [ ] Configurar IA com novo system message
- [ ] Implementar function calling
- [ ] Configurar webhook para confirmação
- [ ] Testar fluxo completo
- [ ] Deploy em produção

**Agora a Letícia apresentará um menu completo e criará PIX automaticamente para qualquer opção escolhida!** 🚀