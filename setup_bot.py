import os
import requests
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def setup_bot_profile():
    """Configurar perfil do bot com foto e nome"""
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token or bot_token == 'SEU_TOKEN_AQUI':
        print("❌ Token do bot não configurado!")
        print("Configure o BOT_TOKEN no arquivo .env")
        print("Obtenha seu token em: https://t.me/BotFather")
        return False
    
    try:
        bot = Bot(token=bot_token)
        
        # Verificar se o bot está funcionando
        bot_info = bot.get_me()
        print(f"✅ Bot conectado: @{bot_info.username}")
        
        # Configurar foto do perfil
        photo_path = "fotos/bot-foot.png"
        if os.path.exists(photo_path):
            try:
                with open(photo_path, 'rb') as photo:
                    bot.set_chat_photo(chat_id=bot_info.id, photo=photo)
                print("✅ Foto do perfil configurada")
            except TelegramError as e:
                print(f"⚠️  Não foi possível definir a foto do perfil: {e}")
                print("Nota: Apenas o criador do bot pode alterar a foto via BotFather")
        else:
            print(f"⚠️  Foto não encontrada: {photo_path}")
        
        # Configurar comandos do bot
        commands = [
            ("start", "Iniciar conversa com a Kyoko"),
            ("oi", "Dizer oi para a Kyoko")
        ]
        
        bot.set_my_commands(commands)
        print("✅ Comandos configurados")
        
        print("\n🎉 Bot configurado com sucesso!")
        print(f"Nome: Kyoko uwu")
        print(f"Username: @{bot_info.username}")
        print(f"ID: {bot_info.id}")
        
        return True
        
    except TelegramError as e:
        print(f"❌ Erro ao configurar bot: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == '__main__':
    print("🤖 Configurando Bot Kyoko...\n")
    setup_bot_profile()