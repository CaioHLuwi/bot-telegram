import os
import sys
import asyncio
import logging
import requests
import tempfile
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode
from dotenv import load_dotenv
from metrics import bot_metrics

# Carregar configurações locais se existirem
def load_local_env():
    """Carregar variáveis do arquivo .env.local se existir"""
    env_local_path = os.path.join(os.path.dirname(__file__), '.env.local')
    if os.path.exists(env_local_path):
        with open(env_local_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    return False

# Carregar configurações locais
local_env_loaded = load_local_env()

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurações
BOT_TOKEN = os.getenv('BOT_TOKEN')
PUSHIN_PAY_TOKEN = '42079|U54azimwhSNYA6BLEZWhISWJNm5XGCVwOqzJoj0X842499b1'
PUSHIN_PAY_BASE_URL = 'https://api.pushinpay.com.br/api'
CONTEUDO_LINK = 'https://kyokoleticia.site/conteudo'
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

# Estados da conversa
user_states = {}

# Controle de mensagens promocionais
promotional_messages_enabled = True

class ConversationState:
    WAITING_INITIAL = 'waiting_initial'
    WAITING_RESPONSE = 'waiting_response'
    WAITING_QUESTION_TIMEOUT = 'waiting_question_timeout'
    WAITING_PAYMENT_12 = 'waiting_payment_12'
    WAITING_PAYMENT_5 = 'waiting_payment_5'
    WAITING_PAYMENT_10 = 'waiting_payment_10'
    WAITING_PIX_VALUE = 'waiting_pix_value'
    CONVERSATION_ENDED = 'conversation_ended'

def create_pix_payment(amount: float, description: str) -> dict:
    """Criar pagamento PIX usando Pushin Pay API"""
    try:
        headers = {
            'Authorization': f'Bearer {PUSHIN_PAY_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Converter valor para centavos (API espera valor em centavos)
        value_in_cents = int(amount * 100)
        
        payload = {
            'value': value_in_cents
            # webhook_url removido - pode ser adicionado quando necessário
        }
        
        response = requests.post(
            f'{PUSHIN_PAY_BASE_URL}/pix/cashIn',
            json=payload,
            headers=headers
        )
        
        logger.info(f'Resposta da API Pushin Pay: {response.status_code} - {response.text}')
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            logger.error(f'Erro ao criar pagamento: {response.status_code} - {response.text}')
            return None
            
    except Exception as e:
        logger.error(f'Erro na API Pushin Pay: {e}')
        return None

def create_paradise_pix_payment(amount: float, description: str) -> dict:
    """Criar pagamento PIX usando Paradise API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            'api_token': PARADISE_API_TOKEN,
            'offer_hash': PARADISE_OFFER_HASH,
            'amount': amount,
            'currency': 'BRL',
            'payment_method': 'pix',
            'description': description,
            'customer': {
                'name': 'Cliente',
                'email': 'cliente@exemplo.com'
            }
        }
        
        response = requests.post(
            f'{PARADISE_BASE_URL}/transactions',
            json=payload,
            headers=headers
        )
        
        logger.info(f'Resposta da API Paradise: {response.status_code} - {response.text}')
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            logger.error(f'Erro ao criar pagamento Paradise: {response.status_code} - {response.text}')
            return None
            
    except Exception as e:
        logger.error(f'Erro na API Paradise: {e}')
        return None

def check_payment_status(payment_id: str) -> dict:
    """Verificar status do pagamento"""
    try:
        headers = {
            'Authorization': f'Bearer {PUSHIN_PAY_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.get(
            f'{PUSHIN_PAY_BASE_URL}/transactions/{payment_id}',
            headers=headers
        )
        
        logger.info(f'Verificação de pagamento: {response.status_code} - {response.text}')
        
        if response.status_code == 200:
            payment_data = response.json()
            status = payment_data.get('status', 'unknown')
            return {
                'paid': status == 'paid',
                'status': status,
                'data': payment_data
            }
        else:
            logger.error(f'Erro ao verificar pagamento: {response.status_code} - {response.text}')
            return {'paid': False, 'status': 'error', 'data': None}
            
    except Exception as e:
        logger.error(f'Erro ao verificar pagamento: {e}')
        return {'paid': False, 'status': 'error', 'data': None}

async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Iniciar conversa com sequência de mensagens"""
    user_id = update.effective_user.id
    user_states[user_id] = ConversationState.WAITING_INITIAL
    
    # Registrar métricas do usuário
    bot_metrics.log_user_start(
        user_id=user_id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name
    )
    
    # Primeira mensagem
    await update.message.reply_text(
        "Oiii mo, tudo bem? sou a Leticia Kyoko ali do grupo de packzinhos, fico muito feliz que você tenha gostado de mim e do meu conteúdo e tenha se interessado mais nele"
    )
    
    # Aguardar um pouco antes da próxima mensagem
    await asyncio.sleep(2)
    
    # Oferta da call de vídeo
    keyboard = [
        [InlineKeyboardButton("💕 Sim, quero a call!", callback_data="call_video_yes")],
        [InlineKeyboardButton("❌ Não, obrigado", callback_data="call_video_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    call_message = "💕 **Oferta Especial!** 💕\n\n"
    call_message += "Que tal fazermos uma call de vídeo de 5 minutos bem gostosinha? ❤️‍🔥\n\n"
    call_message += "💰 **Apenas R$ 29,90**\n"
    call_message += "📱 **5 minutos de pura diversão**\n"
    call_message += "🔥 **Só eu e você, bem íntimo**\n\n"
    call_message += "O que você acha, amor?"
    
    await update.message.reply_text(
        call_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Aguardar resposta sobre a call
    await asyncio.sleep(1)
    
    # Enviar primeira foto
    try:
        if os.path.exists('fotos/4.jpg'):
            with open('fotos/4.jpg', 'rb') as photo:
                await update.message.reply_photo(photo=photo)
        else:
            await update.message.reply_text("📸 4.jpg (foto será adicionada)")
        
        await asyncio.sleep(2)
            
    except Exception as e:
        logger.error(f'Erro ao enviar mídia: {e}')
    
    # Oferta direta com PIX
    await update.message.reply_text(
        "Quer o vídeo sem censura mo? No meu pack eu te entrego 26 fotinhas deliciosas e 7 vídeos explicitos para você gozar comigo rsrsrs. Tudo isso por só R$ 19,90, te envio tudo na hora no privado do telegram."
    )
    
    await asyncio.sleep(2)
    
    # Gerar PIX de R$ 19,90 automaticamente
    payment_data = create_pix_payment(19.90, "Pack Kyoko - R$ 19,90")
    
    if payment_data:
        user_states[user_id] = ConversationState.WAITING_PAYMENT_12
        
        # Salvar dados do pagamento
        context.user_data['payment_id_12'] = payment_data.get('id')
        context.user_data['pix_code_12'] = payment_data.get('qr_code')
        
        await update.message.reply_text(
            f"Aqui está seu PIX de R$ 19,90:\n\n"
            f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
            f"Após o pagamento, clique em 'Confirmar Pagamento'!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_12_{payment_data.get('id')}")],
                [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_12")],
                [InlineKeyboardButton("Quero o de 5,90", callback_data="pode_ser_5")]
            ])
        )
    else:
        await update.message.reply_text(
            "Ops! Houve um erro ao gerar o PIX. Tente novamente em alguns minutos."
        )
    
    # Mudar estado para aguardar resposta
    user_states[user_id] = ConversationState.WAITING_RESPONSE

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar mensagens do usuário"""
    user_id = update.effective_user.id
    message_text = update.message.text.lower()
    
    # Verificar se é um comando de métricas ou saúde (não ativar fluxo)
    if message_text.startswith('/metricas') or message_text.startswith('/saude') or message_text.startswith('/groupid'):
        return
    
    # Verificar mensagens de pagamento em qualquer estado
    payment_keywords = ['paguei', 'já fiz o pix', 'ja fiz o pix', 'fiz o pix', 'pagamento feito', 'pix feito']
    if any(keyword in message_text for keyword in payment_keywords):
        await update.message.reply_text(
            "Se você já fez o pix me manda o comprovante em @leticiakyoko porfavorzinho, vou te mandar o pack assim que conseguir <3"
        )
        return
    
    # Se não há estado, iniciar conversa automaticamente para qualquer mensagem
    if user_id not in user_states:
        await start_conversation(update, context)
        return
    
    current_state = user_states[user_id]
    
    if current_state == ConversationState.WAITING_PIX_VALUE:
        # Processar valor digitado para gerar PIX personalizado
        try:
            # Remover espaços e substituir vírgula por ponto
            value_text = update.message.text.strip().replace(',', '.')
            
            # Tentar converter para float
            value = float(value_text)
            
            # Validar limites
            if value < 1.00:
                await update.message.reply_text(
                    "❌ **Valor muito baixo!**\n\n"
                    "O valor mínimo é R$ 1,00.\n\n"
                    "Digite um valor válido:",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            if value > 1000.00:
                await update.message.reply_text(
                    "❌ **Valor muito alto!**\n\n"
                    "O valor máximo é R$ 1.000,00.\n\n"
                    "Digite um valor válido:",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Gerar PIX com o valor especificado
            payment_data = create_pix_payment(value, f"PIX Personalizado - R$ {value:.2f}")
            
            if payment_data:
                # Resetar estado
                user_states[user_id] = ConversationState.WAITING_RESPONSE
                
                # Salvar dados do pagamento
                context.user_data['payment_id_custom'] = payment_data.get('id')
                context.user_data['pix_code_custom'] = payment_data.get('qr_code')
                context.user_data['pix_value_custom'] = value
                
                message = f"✅ **PIX Gerado com Sucesso!**\n\n"
                message += f"💰 **Valor:** R$ {value:.2f}\n\n"
                message += f"📋 **Código PIX:**\n"
                message += f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
                message += f"⏰ **Válido por:** 30 minutos\n\n"
                message += f"📱 **Como pagar:**\n"
                message += f"1. Copie o código PIX\n"
                message += f"2. Abra seu app bancário\n"
                message += f"3. Escolha PIX > Copia e Cola\n"
                message += f"4. Cole o código e confirme"
                
                await update.message.reply_text(
                    message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_custom_{payment_data.get('id')}")],
                        [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_custom")]
                    ])
                )
                
                logger.info(f"PIX personalizado gerado: R$ {value:.2f} para {update.effective_user.first_name}")
            else:
                await update.message.reply_text(
                    "❌ **Erro ao gerar PIX**\n\n"
                    "Houve um problema ao processar seu pagamento.\n"
                    "Tente novamente em alguns minutos."
                )
                # Resetar estado em caso de erro
                user_states[user_id] = ConversationState.WAITING_RESPONSE
                
        except ValueError:
            await update.message.reply_text(
                "❌ **Valor inválido!**\n\n"
                "Digite apenas números. Exemplos:\n"
                "• `15.50`\n"
                "• `25`\n"
                "• `100.00`\n\n"
                "Tente novamente:",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Erro ao processar valor do PIX: {e}")
            await update.message.reply_text(
                "❌ **Erro interno**\n\n"
                "Tente novamente mais tarde."
            )
            # Resetar estado em caso de erro
            user_states[user_id] = ConversationState.WAITING_RESPONSE
        
        return
    
    elif current_state == 'waiting_paradise_pix_value':
        # Processar valor digitado para gerar PIX Paradise
        try:
            # Remover espaços e substituir vírgula por ponto
            value_text = update.message.text.strip().replace(',', '.')
            
            # Tentar converter para float
            value = float(value_text)
            
            # Validar limites
            if value < 1.00:
                await update.message.reply_text(
                    "❌ **Valor muito baixo!**\n\n"
                    "O valor mínimo é R$ 1,00.\n\n"
                    "Digite um valor válido:",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            if value > 1000.00:
                await update.message.reply_text(
                    "❌ **Valor muito alto!**\n\n"
                    "O valor máximo é R$ 1.000,00.\n\n"
                    "Digite um valor válido:",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Gerar PIX Paradise com o valor especificado
            payment_data = create_paradise_pix_payment(value, f"PIX Paradise - R$ {value:.2f}")
            
            if payment_data:
                # Resetar estado
                user_states[user_id] = ConversationState.WAITING_RESPONSE
                
                # Salvar dados do pagamento
                context.user_data['payment_id_paradise'] = payment_data.get('id')
                context.user_data['pix_code_paradise'] = payment_data.get('pix_code')
                context.user_data['pix_value_paradise'] = value
                
                message = f"✅ **PIX Paradise Gerado!**\n\n"
                message += f"💰 **Valor:** R$ {value:.2f}\n\n"
                message += f"📋 **Código PIX:**\n"
                message += f"`{payment_data.get('pix_code', 'Código PIX não disponível')}`\n\n"
                message += f"⏰ **Válido por:** 30 minutos\n\n"
                message += f"📱 **Como pagar:**\n"
                message += f"1. Copie o código PIX\n"
                message += f"2. Abra seu app bancário\n"
                message += f"3. Escolha PIX > Copia e Cola\n"
                message += f"4. Cole o código e confirme"
                
                await update.message.reply_text(
                    message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_paradise_{payment_data.get('id')}")],
                        [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_paradise")]
                    ])
                )
                
                logger.info(f"PIX Paradise gerado: R$ {value:.2f} para {update.effective_user.first_name}")
            else:
                await update.message.reply_text(
                    "❌ **Erro ao gerar PIX Paradise**\n\n"
                    "Houve um problema ao processar seu pagamento.\n"
                    "Tente novamente em alguns minutos."
                )
                # Resetar estado em caso de erro
                user_states[user_id] = ConversationState.WAITING_RESPONSE
                
        except ValueError:
            await update.message.reply_text(
                "❌ **Valor inválido!**\n\n"
                "Digite apenas números. Exemplos:\n"
                "• `15.50`\n"
                "• `25`\n"
                "• `100.00`\n\n"
                "Tente novamente:",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Erro ao processar valor do PIX Paradise: {e}")
            await update.message.reply_text(
                "❌ **Erro interno**\n\n"
                "Tente novamente mais tarde."
            )
            # Resetar estado em caso de erro
            user_states[user_id] = ConversationState.WAITING_RESPONSE
        
        return
    
    elif current_state == ConversationState.WAITING_RESPONSE:
        # Com o novo fluxo, as respostas são tratadas pelos botões inline
        await update.message.reply_text(
            "Use os botões acima para escolher sua opção! 😊"
        )

# Funções de botões removidas - não são mais necessárias com o novo fluxo

# Funções removidas - fluxo agora é direto na start_conversation

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar cliques nos botões"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "call_video_yes":
        # Usuário aceitou a call de vídeo
        try:
            payment_data = create_pix_payment(29.90, "Call de Vídeo 5min - R$ 29,90")
            
            if payment_data:
                user_states[user_id] = ConversationState.WAITING_PAYMENT_12  # Reutilizando estado
                
                context.user_data['payment_id_12'] = payment_data.get('id')
                context.user_data['pix_code_12'] = payment_data.get('qr_code')
                
                message = f"💕 **Que delícia, amor!** 💕\n\n"
                message += f"**PIX de R$ 29,90 para nossa call:**\n"
                message += f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
                message += f"📱 **Como pagar:**\n"
                message += f"1. Copie o código PIX\n"
                message += f"2. Abra seu banco\n"
                message += f"3. Cole o código na área PIX\n"
                message += f"4. Confirme o pagamento\n"
                message += f"5. Clique em 'Confirmar pagamento'\n\n"
                message += f"🔥 **Após o pagamento, te mando o link da call!**\n"
                message += f"⏰ **Pagamento expira em 30 minutos**"
                
                await query.edit_message_text(
                    message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📋 Copiar código PIX", callback_data=f"copy_pix_12_{payment_data.get('id')}")],
                        [InlineKeyboardButton("✅ Confirmar pagamento", callback_data="confirm_payment_12")]
                    ])
                )
            else:
                await query.edit_message_text("❌ Erro ao gerar pagamento. Tente novamente.")
        except Exception as e:
            logger.error(f"Erro ao gerar PIX da call: {e}")
            await query.edit_message_text("❌ Erro interno. Tente novamente mais tarde.")
    
    elif data == "call_video_no":
        # Usuário recusou a call, continuar com fluxo normal
        await query.edit_message_text(
            "Tudo bem, amor! Vamos para as outras opções então 😊\n\n"
            "Aguarde que vou te mostrar meus conteúdos..."
        )
        
        # Aguardar um pouco e continuar com o fluxo normal
        await asyncio.sleep(2)
        
        # Continuar com o fluxo normal (enviar foto)
        try:
            if os.path.exists('fotos/4.jpg'):
                with open('fotos/4.jpg', 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=photo,
                        caption="Olha uma fotinha minha para você 😘"
                    )
            
            await asyncio.sleep(3)
            
            # Continuar com a pergunta sobre o pack
            keyboard = [
                [InlineKeyboardButton("💕 Sim", callback_data="sim_12")],
                [InlineKeyboardButton("❌ Não", callback_data="nao_12")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Gostou? Tenho um pack completo com 26 fotos e 8 vídeos bem safadinhos por apenas R$ 19,90! Quer?",
                reply_markup=reply_markup
            )
            
        except Exception as e:
            logger.error(f"Erro ao continuar fluxo normal: {e}")
    
    elif data == "sim_12":
        # Gerar PIX de R$ 19,90
        payment_data = create_pix_payment(19.90, "Pack Kyoko - R$ 19,90")
        
        if payment_data:
            user_states[user_id] = ConversationState.WAITING_PAYMENT_12
            
            context.user_data['payment_id_12'] = payment_data.get('id')
            context.user_data['pix_code_12'] = payment_data.get('qr_code')
            
            await query.edit_message_text(
                f"Perfeito amor! 💕\n\n"
                f"Aqui está seu PIX de R$ 19,90:\n\n"
                f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
                f"Após o pagamento, clique em 'Confirmar Pagamento' abaixo!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_12_{payment_data.get('id')}")],
                    [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_12")]
                ])
            )
        else:
            await query.edit_message_text(
                "Ops! Houve um erro ao gerar o PIX. Tente novamente em alguns minutos."
            )
    
    elif data == "nao_12":
        await query.edit_message_text(
            "E se eu fizer mais baratinho para você mo? o que acha? consigo fazer até por R$ 5,90 porque realmente gostei muito de ter vc aqui comigo <3",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Pode ser", callback_data="pode_ser_5")],
                [InlineKeyboardButton("Não quero mesmo", callback_data="nao_quero")]
            ])
        )
    
    elif data == "pode_ser_5":
        # Gerar PIX de R$ 5,90
        payment_data = create_pix_payment(5.90, "Pack Kyoko - R$ 5,90")
        
        if payment_data:
            user_states[user_id] = ConversationState.WAITING_PAYMENT_5
            
            context.user_data['payment_id_5'] = payment_data.get('id')
            context.user_data['pix_code_5'] = payment_data.get('qr_code')
            
            await query.edit_message_text(
                f"Eba! Que bom que aceitou! 💕\n\n"
                f"Aqui está seu PIX de R$ 5,90:\n\n"
                f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
                f"Após o pagamento, clique em 'Confirmar Pagamento' abaixo!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_5_{payment_data.get('id')}")],
                    [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_5")]
                ])
            )
        else:
            await query.edit_message_text(
                "Ops! Houve um erro ao gerar o PIX. Tente novamente em alguns minutos."
            )
    
    elif data == "hoje_nao":
        user_states[user_id] = ConversationState.CONVERSATION_ENDED
        
        await query.edit_message_text(
            "Tudo bem amor, sem problemas!"
        )
        
        # Enviar vídeo 1.mp4
        try:
            if os.path.exists('fotos/1.mp4'):
                with open('fotos/1.mp4', 'rb') as video:
                    await context.bot.send_video(
                        chat_id=query.message.chat_id,
                        video=video
                    )
            else:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="🎥 1.mp4 (vídeo será adicionado)"
                )
        except Exception as e:
            logger.error(f'Erro ao enviar vídeo: {e}')
        
        # Enviar mensagem final
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="ok, se mudar de ideia... já sabe mo"
        )
    
    elif data == "nao_quero":
        user_states[user_id] = ConversationState.CONVERSATION_ENDED
        
        await query.edit_message_text(
            "Aaaaah, tudo bem então gatinho, obrigada. Caso mude de ideia só me falar aqui"
        )
        
        # Enviar foto 1.jpg
        try:
            if os.path.exists('fotos/1.jpg'):
                with open('fotos/1.jpg', 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=photo
                    )
            else:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="📸 1.jpg (foto será adicionada)"
                )
        except Exception as e:
            logger.error(f'Erro ao enviar foto final: {e}')
        
        # Enviar vídeo 1.mp4
        try:
            if os.path.exists('fotos/1.mp4'):
                with open('fotos/1.mp4', 'rb') as video:
                    await context.bot.send_video(
                        chat_id=query.message.chat_id,
                        video=video
                    )
            else:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="🎥 1.mp4 (vídeo será adicionado)"
                )
        except Exception as e:
            logger.error(f'Erro ao enviar vídeo final: {e}')
        
        # Enviar mensagem final de suporte
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Se você tiver algum problema para receber o pack me chama no @leticiakyoko, vou te responder assim que puder <3"
        )
    
    elif data.startswith("copy_pix_12_") or data.startswith("copy_pix_5_") or data.startswith("copy_pix_10_"):
        # Extrair o código PIX dos dados do usuário
        if data.startswith("copy_pix_12_"):
            pix_code = context.user_data.get('pix_code_12', 'Código não disponível')
            valor = "R$ 19,90"
        elif data.startswith("copy_pix_10_"):
            pix_code = context.user_data.get('pix_code_10', 'Código não disponível')
            valor = "R$ 10,00"
        else:
            pix_code = context.user_data.get('pix_code_5', 'Código não disponível')
            valor = "R$ 5,90"
        
        await query.answer(f"Código PIX de {valor} enviado abaixo! Selecione e copie.", show_alert=True)
        
        # Enviar apenas o código PIX sem texto adicional para facilitar a cópia
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"`{pix_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "payment_method_pix_10":
        # Usuário escolheu PIX para R$ 10,00
        try:
            payment_data = create_pix_payment(10.00, "Pack Kyoko Especial - 10 fotos + 2 vídeos - R$ 10,00")
            
            if payment_data:
                user_states[user_id] = ConversationState.WAITING_PAYMENT_10
                
                context.user_data['payment_id_10'] = payment_data.get('id')
                context.user_data['pix_code_10'] = payment_data.get('qr_code')
                
                message = f"💰 **PIX Pack Especial - R$ 10,00 gerado!**\n\n"
                message += f"🎁 **10 fotos + 2 vídeos exclusivos**\n\n"
                message += f"**Código PIX:**\n`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
                message += "📱 **Como pagar:**\n"
                message += "1. Copie o código PIX\n"
                message += "2. Abra seu banco\n"
                message += "3. Cole o código na área PIX\n"
                message += "4. Confirme o pagamento\n"
                message += "5. Clique em 'Confirmar pagamento'\n\n"
                message += "✅ Se quiser, pode usar esse link também, é 100% seguro e te dou 7 dias de garantia no meu pack:\n"
                message += "`https://pay.cakto.com.br/35ehh7w_498700`\n\n"
                message += "⏰ **Pagamento expira em 30 minutos**"
                
                await query.edit_message_text(
                    message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📋 Copiar código PIX", callback_data=f"copy_pix_10_{payment_data.get('id')}")],
                        [InlineKeyboardButton("✅ Confirmar pagamento", callback_data="confirm_payment_10")]
                    ])
                )
            else:
                await query.edit_message_text("❌ Erro ao gerar pagamento. Tente novamente.")
        except Exception as e:
            logger.error(f"Erro ao gerar PIX de R$ 10,00: {e}")
            await query.edit_message_text("❌ Erro interno. Tente novamente mais tarde.")
    
    elif data == "payment_method_card_10":
        # Usuário escolheu cartão para R$ 10,00
        message = "💳 **Pagamento com Cartão de Crédito**\n\n"
        message += "✅ **Benefícios da Cakto:**\n"
        message += "✅ Pagamento 100% seguro\n"
        message += "✅ 7 dias de garantia\n"
        message += "✅ Parcelamento disponível\n"
        message += "✅ Processamento instantâneo\n"
        message += "✅ Suporte 24h\n\n"
        message += "🔗 **Link para pagamento:**\n"
        message += "`https://pay.cakto.com.br/35ehh7w_498700`\n\n"
        message += "Após o pagamento, você receberá o pack automaticamente!"
        
        await query.edit_message_text(message, parse_mode=ParseMode.MARKDOWN)
    
    elif data == "confirm_payment_12":
        payment_id = context.user_data.get('payment_id_12')
        if payment_id:
            payment_status = check_payment_status(payment_id)
            if payment_status['paid']:
                await send_content_link(query, context)
            else:
                status = payment_status['status']
                if status == 'pending' or status == 'CRIADO':
                    await query.answer("Pagamento ainda não foi processado. Aguarde alguns minutos e tente novamente.", show_alert=True)
                else:
                    await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)
        else:
            await query.answer("Erro: ID do pagamento não encontrado.", show_alert=True)
    
    elif data == "confirm_payment_5":
        payment_id = context.user_data.get('payment_id_5')
        if payment_id:
            payment_status = check_payment_status(payment_id)
            if payment_status['paid']:
                await send_content_link(query, context)
            else:
                status = payment_status['status']
                if status == 'pending' or status == 'CRIADO':
                    await query.answer("Pagamento ainda não foi processado. Aguarde alguns minutos e tente novamente.", show_alert=True)
                else:
                    await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)
        else:
            await query.answer("Erro: ID do pagamento não encontrado.", show_alert=True)
    
    elif data == "confirm_payment_10":
        payment_id = context.user_data.get('payment_id_10')
        if payment_id:
            payment_status = check_payment_status(payment_id)
            if payment_status['paid']:
                await send_content_link(query, context)
            else:
                status = payment_status['status']
                if status == 'pending' or status == 'CRIADO':
                    await query.answer("Pagamento ainda não foi processado. Aguarde alguns minutos e tente novamente.", show_alert=True)
                else:
                    await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)
        else:
            await query.answer("Erro: ID do pagamento não encontrado.", show_alert=True)
    
    elif data.startswith("copy_pix_custom_"):
        # Copiar código PIX personalizado
        payment_id = data.replace("copy_pix_custom_", "")
        pix_code = context.user_data.get('pix_code_custom')
        if pix_code:
            await query.answer("Código PIX copiado!", show_alert=True)
        else:
            await query.answer("Erro: Código PIX não encontrado.", show_alert=True)
        
        # Enviar código PIX em mensagem separada para facilitar cópia
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"`{pix_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "confirm_payment_custom":
        payment_id = context.user_data.get('payment_id_custom')
        if payment_id:
            payment_status = check_payment_status(payment_id)
            if payment_status['paid']:
                await send_content_link(query, context)
            else:
                status = payment_status['status']
                if status == 'pending' or status == 'CRIADO':
                    await query.answer("Pagamento ainda não foi processado. Aguarde alguns minutos e tente novamente.", show_alert=True)
                else:
                    await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)
        else:
            await query.answer("Erro: ID do pagamento não encontrado.", show_alert=True)
    
    elif data.startswith("copy_pix_paradise_"):
        # Copiar código PIX Paradise
        payment_id = data.replace("copy_pix_paradise_", "")
        pix_code = context.user_data.get('pix_code_paradise')
        if pix_code:
            await query.answer("Código PIX Paradise copiado!", show_alert=True)
        else:
            await query.answer("Erro: Código PIX não encontrado.", show_alert=True)
        
        # Enviar código PIX em mensagem separada para facilitar cópia
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"`{pix_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "confirm_payment_paradise":
        payment_id = context.user_data.get('payment_id_paradise')
        if payment_id:
            # Para Paradise API, vamos simular confirmação (adapte conforme API real)
            await query.edit_message_text(
                f"✅ **Pagamento Paradise Confirmado!**\n\n"
                f"💰 **Valor:** R$ {context.user_data.get('pix_value_paradise', 0):.2f}\n\n"
                f"🎉 **Obrigado pela preferência!**\n\n"
                f"📱 **Entre em contato para receber seu conteúdo:**\n"
                f"wa.me/5583999620663"
            )
            
            # Registrar pagamento nas métricas
            user_id = query.from_user.id
            amount = context.user_data.get('pix_value_paradise', 0)
            bot_metrics.log_payment(user_id, amount, "paradise_pix")
            
            # Finalizar conversa
            user_states[user_id] = ConversationState.CONVERSATION_ENDED
        else:
            await query.answer("Erro: ID do pagamento não encontrado.", show_alert=True)

async def send_content_link(query, context):
    """Enviar link do conteúdo após pagamento confirmado"""
    user_id = query.from_user.id
    user_states[user_id] = ConversationState.CONVERSATION_ENDED
    
    # Verificar se é pagamento de call de vídeo baseado na descrição do pagamento
    payment_id = context.user_data.get('payment_id_12')
    is_video_call = False
    
    # Verificar se é call de vídeo (valor R$ 29,90)
    if payment_id and "12" in query.data:
        # Assumir que se o valor for 29.90, é call de vídeo
        # (podemos melhorar isso salvando o tipo no context.user_data)
        try:
            payment_status = check_payment_status(payment_id)
            if payment_status.get('data') and payment_status['data'].get('amount') == 29.90:
                is_video_call = True
        except:
            # Se não conseguir verificar, assumir que não é call
            pass
    
    # Determinar tipo de pagamento baseado no callback
    if "12" in query.data:
        if is_video_call:
            payment_type = "call_video"
            amount = 29.90
        else:
            payment_type = "pack_12"
            amount = 19.90
    elif "10" in query.data:
        payment_type = "pack_10"
        amount = 10.00
    else:
        payment_type = "pack_5"
        amount = 5.90
    
    # Registrar pagamento nas métricas
    bot_metrics.log_payment(user_id, amount, payment_type)
    
    if is_video_call:
        # Mensagem para call de vídeo
        await query.edit_message_text(
            f"💕 **Pagamento confirmado!** 💕\n\n"
            f"🔥 **Nossa call de vídeo está confirmada!**\n\n"
            f"📱 **Entre no WhatsApp para marcarmos:**\n"
            f"wa.me/5583999620663\n\n"
            f"💋 Te espero lá, amor! Vai ser delicioso... ❤️‍🔥"
        )
    else:
        # Mensagem para packs
        await query.edit_message_text(
            f"Pagamento confirmado! 🎉\n\n"
            f"Entre no meu site de packzinho e baixe diretamente de lá, obrigado por comprar gatinho, caso queira mais só me chamar rsrs. Espero que goste...\n\n"
            f"🔗 Link: {CONTEUDO_LINK}"
        )
        
        # Enviar mensagem final de suporte apenas para packs
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Se você tiver algum problema para receber o pack me chama no @leticiakyoko, vou te responder assim que puder <3"
        )

async def show_metrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibir métricas do bot"""
    try:
        # Obter estatísticas de conversão
        conversion_stats = bot_metrics.get_conversion_rate()
        
        # Obter estatísticas diárias dos últimos 7 dias
        daily_stats = bot_metrics.get_daily_stats(days=7)
        
        # Obter estatísticas por hora de hoje
        hourly_stats = bot_metrics.get_hourly_distribution()
        
        # Montar mensagem de métricas
        metrics_message = f"📊 **MÉTRICAS DO BOT KYOKO**\n\n"
        
        # Estatísticas gerais
        metrics_message += f"🎯 **CONVERSÃO GERAL**\n"
        metrics_message += f"• Total de conversas: {conversion_stats['total_conversations']}\n"
        metrics_message += f"• Total de pagamentos: {conversion_stats['total_payments']}\n"
        metrics_message += f"• Taxa de conversão: {conversion_stats['conversion_rate']}%\n"
        metrics_message += f"• Receita total: R$ {conversion_stats['total_revenue']:.2f}\n"
        metrics_message += f"• Ticket médio: R$ {conversion_stats['average_ticket']:.2f}\n\n"
        
        # Detalhes por tipo de pack
        metrics_message += f"💰 **VENDAS POR PACK**\n"
        metrics_message += f"• Pack R$ 19,90: {conversion_stats['payments_12']} vendas\n"
        metrics_message += f"• Pack R$ 5,90: {conversion_stats['payments_5']} vendas\n\n"
        
        # Estatísticas diárias (últimos 7 dias)
        if daily_stats and daily_stats['days']:
            metrics_message += f"📅 **ÚLTIMOS 7 DIAS**\n"
            for day_data in daily_stats['days']:
                if day_data['total_conversations'] > 0:  # Só mostrar dias com atividade
                    metrics_message += f"• {day_data['date']}: {day_data['total_conversations']} conversas, {day_data['payments']} pagamentos, R$ {day_data['revenue']:.2f}\n"
            metrics_message += "\n"
        
        # Estatísticas por hora (hoje)
        if hourly_stats and hourly_stats['hourly_data']:
            metrics_message += f"🕐 **HOJE POR HORA**\n"
            for hour_data in hourly_stats['hourly_data']:
                if hour_data['count'] > 0:  # Só mostrar horas com atividade
                    metrics_message += f"• {hour_data['hour']}: {hour_data['count']} conversas ({hour_data['percentage']}%)\n"
        
        await update.message.reply_text(
            metrics_message,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f'Erro ao exibir métricas: {e}')
        await update.message.reply_text(
            "❌ Erro ao carregar métricas. Tente novamente."
        )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await start_conversation(update, context)

async def oi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /oi"""
    await start_conversation(update, context)

async def send_promotional_message(context: ContextTypes.DEFAULT_TYPE):
    """Enviar mensagem promocional automática para o grupo mencionando todos os membros"""
    global promotional_messages_enabled
    
    try:
        if not promotional_messages_enabled:
            logger.info("Mensagens promocionais desabilitadas - pulando envio")
            return
            
        if GROUP_CHAT_ID:
            # Obter lista de membros do grupo
            try:
                chat = await context.bot.get_chat(GROUP_CHAT_ID)
                
                # Obter administradores do grupo (única forma de obter alguns membros via API)
                administrators = await context.bot.get_chat_administrators(GROUP_CHAT_ID)
                
                # Criar lista de menções para administradores
                mentions = []
                for admin in administrators:
                    if admin.user.username:
                        mentions.append(f"@{admin.user.username}")
                    else:
                        mentions.append(f"[{admin.user.first_name}](tg://user?id={admin.user.id})")
                
                # Mensagem promocional
                promotional_text = (
                    "Tem alguma dúvida sobre meus packs amor? Me manda mensagem no @leticiakyoko que vou te responder na hora"
                )
                
                # Adicionar menções se houver
                if mentions:
                    promotional_text += f"📢 {' '.join(mentions[:10])}"  # Limitar a 10 menções para evitar spam
                
                await context.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=promotional_text,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                logger.info(f'Mensagem promocional com {len(mentions)} menções enviada para o grupo {GROUP_CHAT_ID}')
                
            except Exception as e:
                # Fallback: enviar mensagem sem menções específicas
                logger.warning(f'Não foi possível obter membros do grupo: {e}. Enviando mensagem geral.')
                
                promotional_text = (
                    "Tem alguma dúvida sobre meus packs amor? Me manda mensagem no @leticiakyoko que vou te responder na hora"
                )
                
                await context.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=promotional_text,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                logger.info(f'Mensagem promocional geral enviada para o grupo {GROUP_CHAT_ID}')
                
        else:
            logger.warning('GROUP_CHAT_ID não configurado - mensagem promocional não enviada')
            
    except Exception as e:
        logger.error(f'Erro ao enviar mensagem promocional: {e}')

async def clean_group_messages(context: ContextTypes.DEFAULT_TYPE):
    """Limpar mensagens de entrada/saída de membros e notificações do grupo a cada 5 minutos"""
    try:
        if not GROUP_CHAT_ID:
            logger.warning('GROUP_CHAT_ID não configurado - limpeza de mensagens desabilitada')
            return
            
        # Obter informações do bot para identificar suas mensagens
        bot_info = await context.bot.get_me()
        bot_username = bot_info.username
        
        # Obter as últimas 100 mensagens do grupo
        try:
            # Usar o método get_chat para verificar se temos acesso ao grupo
            chat = await context.bot.get_chat(GROUP_CHAT_ID)
            
            # Como não podemos obter histórico de mensagens diretamente,
            # vamos armazenar IDs de mensagens para deletar posteriormente
            # Esta implementação será feita através de um handler de mensagens
            logger.info(f'Verificação de limpeza executada para o grupo {GROUP_CHAT_ID}')
            
        except Exception as e:
            logger.error(f'Erro ao acessar o grupo {GROUP_CHAT_ID}: {e}')
            
    except Exception as e:
        logger.error(f'Erro na limpeza de mensagens: {e}')

# Lista global para armazenar IDs de mensagens que devem ser deletadas
messages_to_delete = []

def ensure_single_instance():
    """Garantir que apenas uma instância do bot rode por vez"""
    lock_file_path = os.path.join(tempfile.gettempdir(), 'bot_kyoko_packs.lock')
    
    try:
        # Verificar se arquivo de lock existe e se o processo ainda está rodando
        if os.path.exists(lock_file_path):
            with open(lock_file_path, 'r') as f:
                try:
                    old_pid = int(f.read().strip())
                    # Verificar se o processo ainda existe (Windows)
                    import psutil
                    if psutil.pid_exists(old_pid):
                        logger.error(f"❌ Outra instância do bot já está rodando (PID: {old_pid})!")
                        logger.error("💡 Para parar: Get-Process python | Stop-Process -Force")
                        sys.exit(1)
                    else:
                        # Processo não existe mais, remover lock antigo
                        os.remove(lock_file_path)
                except (ValueError, ImportError):
                    # Se não conseguir verificar, remover lock antigo
                    os.remove(lock_file_path)
        
        # Criar novo arquivo de lock
        with open(lock_file_path, 'w') as f:
            f.write(str(os.getpid()))
        
        logger.info(f"🔒 Lock criado: PID {os.getpid()}")
        return lock_file_path
        
    except Exception as e:
        logger.warning(f"⚠️ Não foi possível criar lock: {e}")
        return None

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens do grupo - identifica mensagens para deletar"""
    try:
        # Verificar se a mensagem é do grupo configurado
        if update.effective_chat.id != int(GROUP_CHAT_ID):
            return
            
        message = update.message
        if not message:
            return
            
        # Obter informações do bot
        bot_info = await context.bot.get_me()
        bot_username = bot_info.username
        
        should_delete = False
        
        # Verificar se é mensagem de entrada/saída de membros
        if (message.new_chat_members or 
            message.left_chat_member or 
            message.group_chat_created or 
            message.supergroup_chat_created or 
            message.channel_chat_created or 
            message.migrate_to_chat_id or 
            message.migrate_from_chat_id or 
            message.pinned_message or 
            message.new_chat_title or 
            message.new_chat_photo or 
            message.delete_chat_photo):
            should_delete = True
            
        # Verificar se é mensagem de usuário (não é da Leticia Kyoko nem do bot)
        elif message.from_user:
            username = message.from_user.username or ""
            first_name = message.from_user.first_name or ""
            
            # Manter apenas mensagens da "Leticia Kyoko" e do bot
            if (username.lower() != "leticiakyoko" and 
                first_name.lower() != "leticia kyoko" and 
                username != bot_username and 
                not message.from_user.is_bot):
                should_delete = True
                
        # Adicionar à lista de mensagens para deletar
        if should_delete:
            messages_to_delete.append({
                'chat_id': message.chat_id,
                'message_id': message.message_id,
                'timestamp': datetime.datetime.now()
            })
            logger.info(f'Mensagem marcada para deleção: {message.message_id}')
            
    except Exception as e:
        logger.error(f'Erro ao processar mensagem do grupo: {e}')

async def execute_message_cleanup(context: ContextTypes.DEFAULT_TYPE):
    """Executar limpeza das mensagens marcadas para deleção"""
    global messages_to_delete
    
    try:
        if not messages_to_delete:
            logger.info('Nenhuma mensagem para deletar')
            return
            
        deleted_count = 0
        failed_count = 0
        
        # Criar uma cópia da lista para iterar
        messages_copy = messages_to_delete.copy()
        
        for msg_info in messages_copy:
            try:
                await context.bot.delete_message(
                    chat_id=msg_info['chat_id'],
                    message_id=msg_info['message_id']
                )
                deleted_count += 1
                messages_to_delete.remove(msg_info)
                
            except Exception as e:
                failed_count += 1
                # Remover mensagens antigas que falharam (mais de 48h)
                if (datetime.datetime.now() - msg_info['timestamp']).total_seconds() > 172800:
                    messages_to_delete.remove(msg_info)
                    logger.warning(f'Removendo mensagem antiga da lista: {msg_info["message_id"]}')
                else:
                    logger.warning(f'Falha ao deletar mensagem {msg_info["message_id"]}: {e}')
                    
        if deleted_count > 0 or failed_count > 0:
            logger.info(f'Limpeza concluída: {deleted_count} deletadas, {failed_count} falharam')
            
    except Exception as e:
        logger.error(f'Erro na execução da limpeza: {e}')

async def get_group_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para obter o ID do grupo atual"""
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title or "Chat Privado"
    
    message = f"📋 **Informações do Chat:**\n\n"
    message += f"🆔 **ID:** `{chat_id}`\n"
    message += f"📝 **Tipo:** {chat_type}\n"
    message += f"🏷️ **Nome:** {chat_title}\n\n"
    
    if chat_type in ['group', 'supergroup']:
        message += "✅ Este é um grupo! Você pode usar este ID na variável GROUP_CHAT_ID do arquivo .env"
    else:
        message += "ℹ️ Este não é um grupo. Para obter o ID de um grupo, execute este comando dentro do grupo desejado."
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def pix_10_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para gerar pagamento de R$ 10,00 - pergunta forma de pagamento"""
    try:
        user_id = update.effective_user.id
        
        # Criar botões para escolher forma de pagamento
        keyboard = [
            [InlineKeyboardButton("💳 PIX", callback_data="payment_method_pix_10")],
            [InlineKeyboardButton("💰 Cartão de Crédito", callback_data="payment_method_card_10")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = "💰 **Pack Especial - R$ 10,00**\n\n"
        message += "🎁 **10 fotos + 2 vídeos exclusivos**\n\n"
        message += "Escolha sua forma de pagamento preferida:\n\n"
        message += "✅ **PIX** - Instantâneo e seguro\n"
        message += "✅ **Cartão** - Parcelamento disponível\n\n"
        message += "Qual você prefere?"
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /10: {e}")
        await update.message.reply_text("❌ Erro interno. Tente novamente mais tarde.")

async def gerar_pix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /gerarpix - solicita valor e gera PIX personalizado"""
    try:
        user_id = update.effective_user.id
        
        # Definir estado para aguardar valor
        user_states[user_id] = ConversationState.WAITING_PIX_VALUE
        
        message = "💰 **Gerar PIX Personalizado**\n\n"
        message += "Digite o valor desejado para o PIX:\n\n"
        message += "📝 **Exemplos:**\n"
        message += "• `15.50`\n"
        message += "• `25`\n"
        message += "• `100.00`\n\n"
        message += "⚠️ **Valor mínimo:** R$ 1,00\n"
        message += "⚠️ **Valor máximo:** R$ 1.000,00"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Comando /gerarpix iniciado por {update.effective_user.first_name}")
        
    except Exception as e:
        logger.error(f"Erro no comando /gerarpix: {e}")
        await update.message.reply_text("❌ Erro interno. Tente novamente mais tarde.")

async def pix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pix - gerar PIX com Paradise API"""
    try:
        user_id = update.effective_user.id
        
        # Definir estado para aguardar valor
        user_states[user_id] = 'waiting_paradise_pix_value'
        
        message = "💰 **Gerar PIX com Paradise**\n\n"
        message += "Digite o valor desejado para o PIX:\n\n"
        message += "📝 **Exemplos:**\n"
        message += "• `15.50`\n"
        message += "• `25`\n"
        message += "• `100.00`\n\n"
        message += "⚠️ **Valor mínimo:** R$ 1,00\n"
        message += "⚠️ **Valor máximo:** R$ 1.000,00"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Comando /pix iniciado por {update.effective_user.first_name}")
        
    except Exception as e:
        logger.error(f"Erro no comando /pix: {e}")
        await update.message.reply_text("❌ Erro interno. Tente novamente mais tarde.")

async def parar_promo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para parar/iniciar mensagens promocionais automáticas"""
    global promotional_messages_enabled
    
    try:
        # Verificar se é mensagem privada
        if update.effective_chat.type != 'private':
            await update.message.reply_text(
                "❌ Este comando só pode ser usado no chat privado."
            )
            return
        
        # Alternar estado das mensagens promocionais
        promotional_messages_enabled = not promotional_messages_enabled
        
        status = "✅ ATIVADAS" if promotional_messages_enabled else "❌ DESATIVADAS"
        action = "ativadas" if promotional_messages_enabled else "desativadas"
        
        message = f"""🔧 **Controle de Mensagens Promocionais**

**Status atual:** {status}

As mensagens promocionais automáticas foram {action}.

**Intervalo:** A cada 1 hora (quando ativas)
**Comando:** /pararpromo (para alternar)

**Última alteração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"""
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f'Mensagens promocionais {action} por usuário {update.effective_user.id}')
        
    except Exception as e:
        logger.error(f'Erro no comando /pararpromo: {e}')
        await update.message.reply_text(
            "❌ Erro ao alterar configuração. Tente novamente."
        )

async def saude_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para verificar se o bot está funcionando normalmente"""
    import datetime
    import psutil
    import os
    
    try:
        # Informações básicas com fuso horário de Brasília (UTC-3)
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        brasilia_offset = datetime.timedelta(hours=-3)
        now = utc_now + brasilia_offset
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.Process(os.getpid()).create_time())
        
        # Status do sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Verifica se os jobs automáticos estão configurados
        job_queue_status = "✅ Ativo" if GROUP_CHAT_ID else "⚠️ Não configurado"
        
        # Contar mensagens pendentes para limpeza
        pending_cleanup = len(messages_to_delete)
        
        message = f"🤖 **Status do Bot Kyoko**\n\n"
        message += f"✅ **Bot Online:** Funcionando normalmente\n"
        message += f"⏰ **Data/Hora:** {now.strftime('%d/%m/%Y %H:%M:%S')}\n"
        message += f"🕐 **Uptime:** {str(uptime).split('.')[0]}\n"
        message += f"💾 **Uso de Memória:** {memory.percent:.1f}%\n"
        message += f"🖥️ **Uso de CPU:** {cpu_percent:.1f}%\n"
        message += f"📢 **Jobs Automáticos:** {job_queue_status}\n"
        message += f"🧹 **Mensagens p/ Limpeza:** {pending_cleanup}\n\n"
        
        if GROUP_CHAT_ID:
            message += f"🎯 **Grupo Configurado:** `{GROUP_CHAT_ID}`\n"
        
        # Status das mensagens promocionais
        promo_status = "✅ Ativas" if promotional_messages_enabled else "❌ Desativadas"
        message += f"📢 **Mensagens Promocionais:** {promo_status}\n\n"
        
        message += "🔄 **Comandos Disponíveis:**\n"
        message += "• `/start` - Iniciar bot\n"
        message += "• `/oi` - Saudação\n"
        message += "• `/10` - Pack Especial: 10 fotos + 2 vídeos por R$ 10,00\n"
        message += "• `/gerarpix` - Gerar PIX personalizado\n"
        message += "• `/metricas` - Ver estatísticas\n"
        message += "• `/groupid` - ID do grupo\n"
        message += "• `/pararpromo` - Controlar promoções (privado)\n"
        message += "• `/saude` - Status do bot\n\n"
        message += "💚 **Tudo funcionando perfeitamente!**"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"Comando /saude executado por {update.effective_user.first_name}")
        
    except Exception as e:
        error_message = f"❌ **Erro ao verificar status:**\n\n`{str(e)}`\n\n"
        error_message += "⚠️ O bot está online, mas houve um problema ao coletar informações do sistema."
        await update.message.reply_text(error_message, parse_mode='Markdown')
        logger.error(f"Erro no comando /saude: {e}")

def main():
    """Função principal"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não encontrado! Configure a variável de ambiente.")
        return
    
    # Verificar instância única
    lock_file = ensure_single_instance()
    
    # Log de configurações
    environment = os.getenv('ENVIRONMENT', 'production')
    logger.info(f"🌍 Ambiente: {environment}")
    if local_env_loaded:
        logger.info("📁 Configurações locais carregadas (.env.local)")
    logger.info(f"🤖 Bot Token: ...{BOT_TOKEN[-10:]}")
    logger.info(f"👥 Grupo ID: {GROUP_CHAT_ID}")
    
    # Criar aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("oi", oi_command))
    application.add_handler(CommandHandler("10", pix_10_command))
    application.add_handler(CommandHandler("gerarpix", gerar_pix_command))
    application.add_handler(CommandHandler("pix", pix_command))
    application.add_handler(CommandHandler("metricas", show_metrics))
    application.add_handler(CommandHandler("saude", saude_command))
    application.add_handler(CommandHandler("pararpromo", parar_promo_command))
    application.add_handler(CommandHandler("groupid", get_group_id_command))
    
    # Handler para mensagens privadas (conversas do bot)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, handle_message))
    
    # Handler para mensagens do grupo (para limpeza automática)
    application.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, handle_group_message))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Configurar jobs automáticos
    if GROUP_CHAT_ID:
        try:
            job_queue = application.job_queue
            if job_queue is not None:
                # Mensagens promocionais (a cada 1 hora)
                job_queue.run_repeating(
                    send_promotional_message,
                    interval=3600,  # 3600 segundos = 1 hora
                    first=10,       # Primeira execução após 10 segundos (teste de deploy)
                    name='promotional_messages'
                )
                
                # Limpeza de mensagens (a cada 5 minutos)
                job_queue.run_repeating(
                    execute_message_cleanup,
                    interval=300,   # 300 segundos = 5 minutos
                    first=30,       # Primeira execução após 30 segundos
                    name='message_cleanup'
                )
                
                logger.info(f"Jobs automáticos configurados para o grupo {GROUP_CHAT_ID}:")
                logger.info("- Mensagens promocionais: a cada 1 hora")
                logger.info("- Limpeza de mensagens: a cada 5 minutos")
                logger.info("Primeira mensagem promocional será enviada em 10 segundos como teste de deploy")
                logger.info("Primeira limpeza será executada em 30 segundos")
            else:
                logger.error("JobQueue não disponível. Instale com: pip install python-telegram-bot[job-queue]")
        except Exception as e:
            logger.error(f"Erro ao configurar jobs automáticos: {e}")
            logger.error("Para usar jobs automáticos, instale: pip install python-telegram-bot[job-queue]")
    else:
        logger.warning("GROUP_CHAT_ID não configurado - jobs automáticos desabilitados")
    
    # Iniciar bot
    logger.info("Bot iniciado!")
    application.run_polling()

if __name__ == '__main__':
    main()