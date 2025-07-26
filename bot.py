import os
import asyncio
import logging
import requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode
from dotenv import load_dotenv
from metrics import bot_metrics

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
PUSHIN_PAY_TOKEN = '39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5'
PUSHIN_PAY_BASE_URL = 'https://api.pushinpay.com.br/api'
CONTEUDO_LINK = 'https://kyokoleticia.site/conteudo'

# Estados da conversa
user_states = {}

class ConversationState:
    WAITING_INITIAL = 'waiting_initial'
    WAITING_RESPONSE = 'waiting_response'
    WAITING_QUESTION_TIMEOUT = 'waiting_question_timeout'
    WAITING_PAYMENT_12 = 'waiting_payment_12'
    WAITING_PAYMENT_5 = 'waiting_payment_5'
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
            'value': value_in_cents,
            'webhook_url': None  # Opcional: adicione sua URL de webhook se tiver
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

def check_payment_status(payment_id: str) -> bool:
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
            return payment_data.get('status') == 'paid'
        else:
            logger.error(f'Erro ao verificar pagamento: {response.status_code} - {response.text}')
            return False
            
    except Exception as e:
        logger.error(f'Erro ao verificar pagamento: {e}')
        return False

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
    
    await asyncio.sleep(3)
    
    # Mensagem sobre o pack
    await update.message.reply_text(
        "O que acha? você vai receber isso e muito mais (rsrs) no seu telegram assim que fizer o pix para pegar seu packzinho comigo"
    )
    
    await asyncio.sleep(2)
    
    # Oferta
    await update.message.reply_text(
        "Hoje, para você eu consigo fazer por só R$ 12,90 algumas fotinhas, vou pensar se mando 10 fotinhas e 2 vídeos, ou quem sabe mais rsrsrs. O que acha? Quer minhas fotinhas?"
    )
    
    # Mudar estado para aguardar resposta
    user_states[user_id] = ConversationState.WAITING_RESPONSE

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar mensagens do usuário"""
    user_id = update.effective_user.id
    message_text = update.message.text.lower()
    
    # Se não há estado, iniciar conversa
    if user_id not in user_states:
        await start_conversation(update, context)
        return
    
    current_state = user_states[user_id]
    
    if current_state == ConversationState.WAITING_RESPONSE:
        # Verificar se é uma pergunta
        if '?' in update.message.text:
            user_states[user_id] = ConversationState.WAITING_QUESTION_TIMEOUT
            # Aguardar 2 minutos antes de responder
            context.job_queue.run_once(
                send_buttons_after_question,
                120,  # 2 minutos
                data={'chat_id': update.effective_chat.id, 'user_id': user_id}
            )
            return
        
        # Verificar resposta sim/não
        if 'sim' in message_text or 'si' in message_text:
            await handle_yes_response(update, context)
        elif 'não' in message_text or 'nao' in message_text or 'no' in message_text:
            await handle_no_response(update, context)
        else:
            # Enviar botões diretamente se não for sim/não claro
            await send_initial_buttons(update, context)

async def send_buttons_after_question(context: ContextTypes.DEFAULT_TYPE):
    """Enviar botões após timeout de pergunta"""
    job_data = context.job.data
    chat_id = job_data['chat_id']
    user_id = job_data['user_id']
    
    if user_id in user_states and user_states[user_id] == ConversationState.WAITING_QUESTION_TIMEOUT:
        await send_initial_buttons_to_chat(context, chat_id, user_id)

async def send_initial_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enviar botões iniciais"""
    user_id = update.effective_user.id
    await send_initial_buttons_to_chat(context, update.effective_chat.id, user_id)

async def send_initial_buttons_to_chat(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int):
    """Enviar botões para um chat específico"""
    keyboard = [
        [InlineKeyboardButton("simm amor", callback_data="sim_12")],
        [InlineKeyboardButton("hoje não", callback_data="nao_12")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text="Aguardando sua resposta...",
        reply_markup=reply_markup
    )
    
    user_states[user_id] = ConversationState.WAITING_RESPONSE

async def handle_yes_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar resposta positiva"""
    user_id = update.effective_user.id
    
    # Gerar PIX de R$ 12,90
    payment_data = create_pix_payment(12.90, "Pack Kyoko - R$ 12,90")
    
    if payment_data:
        user_states[user_id] = ConversationState.WAITING_PAYMENT_12
        
        # Salvar dados do pagamento
        context.user_data['payment_id_12'] = payment_data.get('id')
        context.user_data['pix_code_12'] = payment_data.get('qr_code')
        
        await update.message.reply_text(
            f"Perfeito amor! 💕\n\n"
            f"Aqui está seu PIX de R$ 12,90:\n\n"
            f"`{payment_data.get('qr_code', 'Código PIX não disponível')}`\n\n"
            f"Após o pagamento, clique em 'Confirmar Pagamento' abaixo!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_12_{payment_data.get('id')}")],
                [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data="confirm_payment_12")]
            ])
        )
    else:
        await update.message.reply_text(
            "Ops! Houve um erro ao gerar o PIX. Tente novamente em alguns minutos."
        )

async def handle_no_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar resposta negativa"""
    user_id = update.effective_user.id
    
    await update.message.reply_text(
        "E se eu fizer mais baratinho para você mo? o que acha? consigo fazer até por R$ 05,00 porque realmente gostei muito de ter vc aqui comigo <3"
    )
    
    keyboard = [
        [InlineKeyboardButton("Pode ser", callback_data="pode_ser_5")],
        [InlineKeyboardButton("Não quero mesmo", callback_data="nao_quero")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "O que me diz?",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar cliques nos botões"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "sim_12":
        # Gerar PIX de R$ 12,90
        payment_data = create_pix_payment(12.90, "Pack Kyoko - R$ 12,90")
        
        if payment_data:
            user_states[user_id] = ConversationState.WAITING_PAYMENT_12
            
            context.user_data['payment_id_12'] = payment_data.get('id')
            context.user_data['pix_code_12'] = payment_data.get('qr_code')
            
            await query.edit_message_text(
                f"Perfeito amor! 💕\n\n"
                f"Aqui está seu PIX de R$ 12,90:\n\n"
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
            "E se eu fizer mais baratinho para você mo? o que acha? consigo fazer até por R$ 05,00 porque realmente gostei muito de ter vc aqui comigo <3",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Pode ser", callback_data="pode_ser_5")],
                [InlineKeyboardButton("Não quero mesmo", callback_data="nao_quero")]
            ])
        )
    
    elif data == "pode_ser_5":
        # Gerar PIX de R$ 5,00
        payment_data = create_pix_payment(5.00, "Pack Kyoko - R$ 5,00")
        
        if payment_data:
            user_states[user_id] = ConversationState.WAITING_PAYMENT_5
            
            context.user_data['payment_id_5'] = payment_data.get('id')
            context.user_data['pix_code_5'] = payment_data.get('qr_code')
            
            await query.edit_message_text(
                f"Eba! Que bom que aceitou! 💕\n\n"
                f"Aqui está seu PIX de R$ 5,00:\n\n"
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
        
        # Enviar mensagem final de suporte
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Se você tiver algum problema para receber o pack me chama no @leticiakyoko, vou te responder assim que puder <3"
        )
    
    elif data.startswith("copy_pix_12_") or data.startswith("copy_pix_5_"):
        # Extrair o código PIX dos dados do usuário
        if data.startswith("copy_pix_12_"):
            pix_code = context.user_data.get('pix_code_12', 'Código não disponível')
            valor = "R$ 12,90"
        else:
            pix_code = context.user_data.get('pix_code_5', 'Código não disponível')
            valor = "R$ 5,00"
        
        await query.answer(f"Código PIX de {valor} copiado! Cole no seu app de pagamento.", show_alert=True)
        
        # Enviar o código PIX em uma mensagem separada para facilitar a cópia
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"📋 **Código PIX para copiar ({valor}):**\n\n`{pix_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "confirm_payment_12":
        payment_id = context.user_data.get('payment_id_12')
        if payment_id and check_payment_status(payment_id):
            await send_content_link(query, context)
        else:
            await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)
    
    elif data == "confirm_payment_5":
        payment_id = context.user_data.get('payment_id_5')
        if payment_id and check_payment_status(payment_id):
            await send_content_link(query, context)
        else:
            await query.answer("Você ainda não pagou amor, verifica aí e tenta de novo.", show_alert=True)

async def send_content_link(query, context):
    """Enviar link do conteúdo após pagamento confirmado"""
    user_id = query.from_user.id
    user_states[user_id] = ConversationState.CONVERSATION_ENDED
    
    # Determinar tipo de pagamento baseado no callback
    payment_type = "pack_12" if "12" in query.data else "pack_5"
    amount = 12.90 if payment_type == "pack_12" else 5.00
    
    # Registrar pagamento nas métricas
    bot_metrics.log_payment(user_id, amount, payment_type)
    
    await query.edit_message_text(
        f"Pagamento confirmado! 🎉\n\n"
        f"Entre no meu site de packzinho e baixe diretamente de lá, obrigado por comprar gatinho, caso queira mais só me chamar rsrs. Espero que goste...\n\n"
        f"🔗 Link: {CONTEUDO_LINK}"
    )
    
    # Enviar mensagem final de suporte
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
        metrics_message += f"• Pack R$ 12,90: {conversion_stats['payments_12']} vendas\n"
        metrics_message += f"• Pack R$ 5,00: {conversion_stats['payments_5']} vendas\n\n"
        
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

def main():
    """Função principal"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não encontrado! Configure a variável de ambiente.")
        return
    
    # Criar aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("oi", oi_command))
    application.add_handler(CommandHandler("metricas", show_metrics))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Iniciar bot
    logger.info("Bot iniciado!")
    application.run_polling()

if __name__ == '__main__':
    main()