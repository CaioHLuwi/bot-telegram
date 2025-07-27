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
PUSHIN_PAY_TOKEN = '39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5'
PUSHIN_PAY_BASE_URL = 'https://api.pushinpay.com.br/api'
CONTEUDO_LINK = 'https://kyokoleticia.site/conteudo'
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

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
        "Que legal, você é meu primeiro cliente hoje! No meu pack eu te entrego 26 fotinhas deliciosas e 7 vídeos explicitos para você gozar comigo rsrsrs. Tudo isso por só R$ 12,90, te envio tudo na hora no privado do telegram. Quer meu anjo?"
    )
    
    # Mensagem adicional sobre o bônus
    await update.message.reply_text(
        "Você ainda recebe o link de um grupo com vários packs de amigas minhas do onlyfans e privacy como BÔNUS mo."
    )
    
    # Aguardar 5 segundos antes de enviar os botões
    await asyncio.sleep(5)
    
    # Enviar botões automaticamente
    keyboard = [
        [InlineKeyboardButton("simm amor", callback_data="sim_12")],
        [InlineKeyboardButton("hoje não", callback_data="nao_12")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "O que me diz?",
        reply_markup=reply_markup
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
        "E se eu fizer mais baratinho para você mo? o que acha? consigo fazer até por R$ 5,90 porque realmente gostei muito de ter vc aqui comigo <3"
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
            valor = "R$ 5,90"
        
        await query.answer(f"Código PIX de {valor} copiado! Cole no seu app de pagamento.", show_alert=True)
        
        # Enviar o código PIX em uma mensagem separada para facilitar a cópia
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"📋 **Código PIX para copiar ({valor}):**\n\n`{pix_code}`",
            parse_mode=ParseMode.MARKDOWN
        )
    
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
    """Enviar mensagem promocional automática para o grupo"""
    try:
        if GROUP_CHAT_ID:
            promotional_text = "Super promo, pack apenas hoje por R$ 12,90 ❤️‍🔥 Vem se divertir comigo amor @kyoko_uwubot"
            
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=promotional_text
            )
            
            logger.info(f'Mensagem promocional enviada para o grupo {GROUP_CHAT_ID}')
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
        
        message += "🔄 **Comandos Disponíveis:**\n"
        message += "• `/start` - Iniciar bot\n"
        message += "• `/oi` - Saudação\n"
        message += "• `/metricas` - Ver estatísticas\n"
        message += "• `/groupid` - ID do grupo\n"
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
    application.add_handler(CommandHandler("metricas", show_metrics))
    application.add_handler(CommandHandler("groupid", get_group_id_command))
    application.add_handler(CommandHandler("saude", saude_command))
    
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