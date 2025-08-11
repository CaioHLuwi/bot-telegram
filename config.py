# Configurações do Bot Kyoko

# Informações do Bot
BOT_NAME = "Kyoko uwu"
BOT_PHOTO_PATH = "fotos/bot-foot.png"

# Mensagens do Bot
MESSAGES = {
    'greeting': "Oi gatinho, tudo bem? Que bom te ver aqui comigo 😘 Sou a Letícia Kyoko e tenho várias opções deliciosas para você se divertir...",
    'menu': """
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

Qual desses te deixa mais interessado, mozinho? 😏""",
    'pack_confirmation': "Ótima escolha gatinho! O {pack_type} de R$ {price:.2f} é uma delícia mesmo 😏\n\n{description}\n\n🔸 **Código PIX:**\n`{qr_code}`\n\n🔸 **Valor:** R$ {price:.2f}\n🔸 **ID:** `{pix_id}`\n\nÉ só copiar o código PIX e colar no seu banco! O pagamento é instantâneo e te mando todo o conteúdo assim que confirmar ❤️\n\nEstou ansiosa para você ver tudo que preparei para você, mozinho 😘",
    'pix_error': "Ai que pena gatinho, deu um probleminha para criar seu PIX 😔\n\nErro: {error}\n\nTenta de novo em alguns minutinhos ou me chama que a gente resolve juntos ❤️\n\nEnquanto isso, que tal dar uma olhada nos outros packs? 😘",
    'goodbye': "Aaaaah, tudo bem então gatinho, obrigada. Caso mude de ideia só me falar aqui ❤️",
    'content_link_message': "Entre no meu site de packzinho e baixe diretamente de lá, obrigado por comprar gatinho, caso queira mais só me chamar rsrs. Espero que goste..."
}

# Preços dos Packs da Letícia
PRICES = {
    'pack_basico': 9.90,      # 10 fotos, 3 vídeos
    'pack_medio': 15.90,      # 20 fotos, 6 vídeos  
    'pack_completo': 19.90,   # 30 fotos, 12 vídeos
    'videochamada': 49.90,    # 5 minutos
    'programa': 249.90        # 1 noite
}

# Descrições dos Packs
PACK_DESCRIPTIONS = {
    'pack_basico': '10 fotinhas bem safadinhas e 3 vídeos mostrando tudo',
    'pack_medio': '20 fotinhas em poses provocantes e 6 vídeos mostrando tudo',
    'pack_completo': '30 fotinhas bem explícitas e 12 vídeos mostrando tudinho',
    'videochamada': '5 minutos só eu e você, conversa bem íntima e gostosa',
    'programa': '1 noite inteira comigo, experiência completa e inesquecível'
}

# Arquivos de mídia
MEDIA_FILES = {
    'photos': ['1.jpg', '2.jpg', '4.jpg'],
    'videos': ['1.mp4'],
}

# Configurações de timing (em segundos)
TIMING = {
    'message_delay': 2,
    'media_delay': 2,
    'question_timeout': 120  # 2 minutos
}

# API Pushin Pay
PUSHIN_PAY_CONFIG = {
    'token': '42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1',
    'base_url': 'https://api.pushinpay.com.br/api'
}

# API Paradise Pay
PARADISE_PAY_CONFIG = {
    'api_token': '27Gwhqe0OW5aP7HaatdRPtOqFIjx9yPo3yXFzv2OXWzCL2YgHkr83PV6jc39',
    'base_url': 'https://api.paradisepagbr.com/api',
    'offer_hash': 's7b5e'  # Hash da oferta padrão
}

# Links
LINKS = {
    'content': 'https://kyokoleticia.site/conteudo'
}