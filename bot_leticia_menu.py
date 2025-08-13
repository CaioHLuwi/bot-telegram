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
from config import MESSAGES, PRICES, PACK_DESCRIPTIONS, PUSHIN_PAY_CONFIG, LINKS
from metrics import bot_metrics
from sistema_remarketing_pix import RemarketingPIX

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
PUSHIN_PAY_TOKEN = PUSHIN_PAY_CONFIG['token']
PUSHIN_PAY_BASE_URL = PUSHIN_PAY_CONFIG['base_url']
CONTEUDO_LINK = LINKS['content']
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

# Estados da conversa
user_states = {}

# Inicializar sistema de remarketing
remarketing_system = None
if BOT_TOKEN:
    try:
        remarketing_system = RemarketingPIX(BOT_TOKEN)
        logger.info("🎯 Sistema de remarketing inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema de remarketing: {e}")

# Controle de mensagens promocionais
promotional_messages_enabled = True

class ConversationState:
    WAITING_INITIAL = 'waiting_initial'
    WAITING_PACK_CHOICE = 'waiting_pack_choice'
    WAITING_PAYMENT = 'waiting_payment'
    CONVERSATION_ENDED = 'conversation_ended'

class LeticiaKyokoBot:
    """Classe principal do bot da Letícia Kyoko com sistema de menu"""
    
    def __init__(self):
        self.packs = {
            'pack_basico': {
                'nome': 'Pack Básico',
                'valor': PRICES['pack_basico'],
                'descricao': PACK_DESCRIPTIONS['pack_basico'],
                'emoji': '💕'
            },
            'pack_medio': {
                'nome': 'Pack Médio', 
                'valor': PRICES['pack_medio'],
                'descricao': PACK_DESCRIPTIONS['pack_medio'],
                'emoji': '💖'
            },
            'pack_completo': {
                'nome': 'Pack Completo',
                'valor': PRICES['pack_completo'], 
                'descricao': PACK_DESCRIPTIONS['pack_completo'],
                'emoji': '🔥'
            },
            'videochamada': {
                'nome': 'Vídeochamada',
                'valor': PRICES['videochamada'],
                'descricao': PACK_DESCRIPTIONS['videochamada'],
                'emoji': '📹'
            },
            'programa': {
                'nome': 'Programa',
                'valor': PRICES['programa'],
                'descricao': PACK_DESCRIPTIONS['programa'],
                'emoji': '🌙'
            }
        }
    
    def create_pix_payment(self, amount: float, pack_type: str) -> dict:
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
                pix_data = response.json()
                return {
                    'sucesso': True,
                    'id': pix_data.get('id'),
                    'qr_code': pix_data.get('qr_code'),
                    'qr_code_base64': pix_data.get('qr_code_base64'),
                    'valor': amount,
                    'pack_type': pack_type,
                    'status': pix_data.get('status'),
                    'criado_em': datetime.now().isoformat()
                }
            else:
                logger.error(f'Erro ao criar pagamento: {response.status_code} - {response.text}')
                return {'sucesso': False, 'erro': f'Erro da API: {response.status_code}'}
                
        except Exception as e:
            logger.error(f'Erro na API Pushin Pay: {e}')
            return {'sucesso': False, 'erro': str(e)}
    
    def get_menu_keyboard(self):
        """Criar teclado inline com opções de packs"""
        keyboard = []
        
        for pack_id, pack_info in self.packs.items():
            button_text = f"{pack_info['emoji']} {pack_info['nome']} - R$ {pack_info['valor']:.2f}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"pack_{pack_id}")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def process_message(self, user_id: int, message: str) -> tuple:
        """Processar mensagem do usuário e retornar resposta"""
        message_lower = message.lower()
        
        # Palavras-chave que indicam interesse
        interest_keywords = [
            'oi', 'olá', 'pack', 'conteudo', 'fotos', 'videos', 'quero',
            'interesse', 'comprar', 'ver', 'mostrar', 'menu', 'opções'
        ]
        
        # Verificar se há interesse
        if any(keyword in message_lower for keyword in interest_keywords):
            return self.show_menu(), True
        
        # Resposta padrão para mensagens não reconhecidas
        return self.show_menu(), True
    
    def show_menu(self) -> str:
        """Retornar texto do menu com saudação"""
        return MESSAGES['greeting'] + "\n\n" + MESSAGES['menu']
    
    def create_pix_for_pack(self, user_id: int, pack_id: str, context) -> str:
        """Criar PIX para um pack específico"""
        if pack_id not in self.packs:
            return "Ops! Pack não encontrado. Tente novamente."
        
        pack_info = self.packs[pack_id]
        valor = pack_info['valor']
        nome = pack_info['nome']
        descricao = pack_info['descricao']
        
        # Criar PIX
        resultado = self.create_pix_payment(valor, pack_id)
        
        if resultado['sucesso']:
            payment_id = resultado['id']
            
            # Salvar dados do pagamento no contexto
            context.user_data[f'payment_id_{pack_id}'] = payment_id
            context.user_data[f'pix_code_{pack_id}'] = resultado['qr_code']
            context.user_data['current_pack'] = pack_id
            
            # Iniciar campanha de remarketing
            if remarketing_system:
                try:
                    asyncio.create_task(remarketing_system.iniciar_campanha_remarketing(
                        user_id=str(user_id),
                        payment_id=payment_id,
                        valor_original=valor,
                        pack_name=nome
                    ))
                    logger.info(f"🎯 Campanha de remarketing iniciada para usuário {user_id} - Pack: {nome}")
                except Exception as e:
                    logger.error(f"Erro ao iniciar campanha de remarketing: {e}")
            
            return MESSAGES['pack_confirmation'].format(
                pack_type=nome,
                price=valor,
                description=descricao,
                qr_code=resultado['qr_code'],
                pix_id=payment_id
            )
        else:
            return MESSAGES['pix_error'].format(error=resultado['erro'])

# Instância global do bot
leticia_bot = LeticiaKyokoBot()

async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Iniciar conversa com menu da Letícia"""
    user_id = update.effective_user.id
    user_states[user_id] = ConversationState.WAITING_PACK_CHOICE
    
    # Registrar métricas do usuário
    bot_metrics.log_user_start(
        user_id=user_id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name
    )
    
    # Mostrar menu
    menu_text = leticia_bot.show_menu()
    keyboard = leticia_bot.get_menu_keyboard()
    
    await update.message.reply_text(
        menu_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar mensagens do usuário"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Verificar se é um comando de métricas ou saúde (não ativar fluxo)
    if message_text.lower().startswith(('/metricas', '/saude', '/groupid')):
        return
    
    # Verificar mensagens de pagamento
    payment_keywords = ['paguei', 'já fiz o pix', 'ja fiz o pix', 'fiz o pix', 'pagamento feito', 'pix feito']
    if any(keyword in message_text.lower() for keyword in payment_keywords):
        await update.message.reply_text(
            "Se você já fez o pix me manda o comprovante em @leticiakyoko porfavorzinho, vou te mandar o pack assim que conseguir <3"
        )
        return
    
    # Se não há estado, iniciar conversa automaticamente
    if user_id not in user_states:
        await start_conversation(update, context)
        return
    
    # Processar mensagem
    response, show_keyboard = leticia_bot.process_message(user_id, message_text)
    
    if show_keyboard:
        keyboard = leticia_bot.get_menu_keyboard()
        await update.message.reply_text(
            response,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processar cliques nos botões inline"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # Processar seleção de pack
    if data.startswith('pack_'):
        pack_id = data.replace('pack_', '')
        
        # Criar PIX para o pack selecionado
        response = leticia_bot.create_pix_for_pack(user_id, pack_id, context)
        
        # Criar botões de ação
        pack_info = leticia_bot.packs.get(pack_id)
        if pack_info:
            keyboard = [
                [InlineKeyboardButton("📋 Copiar Código PIX", callback_data=f"copy_pix_{pack_id}")],
                [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data=f"confirm_payment_{pack_id}")],
                [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="show_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None
        
        await query.edit_message_text(
            response,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Atualizar estado
        user_states[user_id] = ConversationState.WAITING_PAYMENT
    
    # Voltar ao menu
    elif data == 'show_menu':
        menu_text = leticia_bot.show_menu()
        keyboard = leticia_bot.get_menu_keyboard()
        
        await query.edit_message_text(
            menu_text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
        user_states[user_id] = ConversationState.WAITING_PACK_CHOICE
    
    # Copiar código PIX
    elif data.startswith('copy_pix_'):
        pack_id = data.replace('copy_pix_', '')
        pix_code = context.user_data.get(f'pix_code_{pack_id}')
        
        if pix_code:
            await query.message.reply_text(
                f"📋 **Código PIX copiado:**\n\n`{pix_code}`\n\n"
                f"Cole este código no seu aplicativo bancário para fazer o pagamento!",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.message.reply_text("❌ Código PIX não encontrado. Tente gerar novamente.")
    
    # Confirmar pagamento
    elif data.startswith('confirm_payment_'):
        pack_id = data.replace('confirm_payment_', '')
        
        await query.message.reply_text(
            "✅ **Pagamento em análise!**\n\n"
            "Assim que o pagamento for confirmado, você receberá todo o conteúdo!\n\n"
            "Se já fez o PIX, me manda o comprovante em @leticiakyoko que eu te mando tudo rapidinho ❤️"
        )
        
        # Opcional: verificar status do pagamento
        payment_id = context.user_data.get(f'payment_id_{pack_id}')
        if payment_id:
            # Aqui você pode implementar verificação automática do pagamento
            pass

async def send_content_link(query, context):
    """Enviar link do conteúdo após confirmação de pagamento"""
    await query.message.reply_text(
        MESSAGES['content_link_message'] + f"\n\n{CONTEUDO_LINK}"
    )

# Comandos administrativos
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await start_conversation(update, context)

async def oi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /oi"""
    await start_conversation(update, context)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /menu para mostrar opções"""
    await start_conversation(update, context)

async def show_metrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar métricas do bot"""
    try:
        metrics = bot_metrics.get_metrics()
        
        message = "📊 **Métricas do Bot Letícia Kyoko**\n\n"
        message += f"👥 **Usuários únicos:** {metrics['unique_users']}\n"
        message += f"💬 **Total de conversas:** {metrics['total_conversations']}\n"
        message += f"🔄 **Conversas ativas:** {metrics['active_conversations']}\n"
        message += f"💰 **PIX gerados:** {metrics['pix_generated']}\n"
        message += f"✅ **Pagamentos confirmados:** {metrics['payments_confirmed']}\n"
        message += f"📈 **Taxa de conversão:** {metrics['conversion_rate']:.1f}%\n\n"
        message += f"🕐 **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f'Erro ao mostrar métricas: {e}')
        await update.message.reply_text("❌ Erro ao carregar métricas.")

async def saude_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de saúde do bot"""
    try:
        # Testar conexão com API
        test_response = requests.get(f'{PUSHIN_PAY_BASE_URL}/health', timeout=5)
        api_status = "✅ Online" if test_response.status_code == 200 else "❌ Offline"
    except:
        api_status = "❌ Offline"
    
    message = "🏥 **Status do Bot Letícia Kyoko**\n\n"
    message += f"🤖 **Bot:** ✅ Online\n"
    message += f"🔗 **API Pushin Pay:** {api_status}\n"
    message += f"💾 **Estados ativos:** {len(user_states)}\n"
    message += f"🕐 **Uptime:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    message += f"📋 **Configurações:**\n"
    message += f"• Token: {'✅ Configurado' if PUSHIN_PAY_TOKEN else '❌ Não configurado'}\n"
    message += f"• Link conteúdo: {'✅ Configurado' if CONTEUDO_LINK else '❌ Não configurado'}"
    
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def main():
    """Função principal"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não encontrado nas variáveis de ambiente")
        sys.exit(1)
    
    # Criar aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("oi", oi_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("metricas", show_metrics))
    application.add_handler(CommandHandler("saude", saude_command))
    
    # Handler para botões inline
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Handler para mensagens de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🚀 Bot Letícia Kyoko iniciado com sistema de menu!")
    logger.info(f"📋 Packs disponíveis: {len(leticia_bot.packs)}")
    logger.info(f"💰 Token configurado: {'✅' if PUSHIN_PAY_TOKEN else '❌'}")
    
    # Iniciar bot
    application.run_polling()

if __name__ == '__main__':
    main()