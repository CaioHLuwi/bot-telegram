import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
import os
from telegram import Bot
from telegram.error import TelegramError
from logger_pix_requests import PixRequestLogger

class RemarketingPIX:
    """
    Sistema de remarketing automático para PIX gerados
    Envia mensagens promocionais em intervalos específicos
    """
    
    def __init__(self, bot_token: str, logger_path: str = "Logs/pix_requests_log.json"):
        self.bot = Bot(token=bot_token)
        self.logger_path = logger_path
        self.pix_logger = PixRequestLogger(logger_path)
        self.active_campaigns = {}  # Armazena campanhas ativas
        
        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def iniciar_campanha_remarketing(self, 
                                          user_id: str, 
                                          payment_id: str, 
                                          valor_original: float,
                                          pack_name: str = "Pack Premium"):
        """
        Inicia uma campanha de remarketing para um usuário específico
        
        Args:
            user_id: ID do usuário no Telegram
            payment_id: ID do pagamento PIX
            valor_original: Valor original do pack
            pack_name: Nome do pack vendido
        """
        try:
            campaign_id = f"remarketing_{payment_id}_{user_id}"
            
            # Registra campanha ativa
            self.active_campaigns[campaign_id] = {
                "user_id": user_id,
                "payment_id": payment_id,
                "valor_original": valor_original,
                "pack_name": pack_name,
                "started_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            self.logger.info(f"🎯 Campanha de remarketing iniciada: {campaign_id}")
            
            # Agenda primeira mensagem (5 minutos)
            asyncio.create_task(self._enviar_primeira_mensagem(
                user_id, payment_id, valor_original, pack_name, campaign_id
            ))
            
            # Agenda segunda mensagem (15 minutos total - 10 minutos após a primeira)
            asyncio.create_task(self._enviar_segunda_mensagem(
                user_id, payment_id, valor_original, pack_name, campaign_id
            ))
            
        except Exception as e:
            self.logger.error(f"Erro ao iniciar campanha de remarketing: {e}")
    
    async def _enviar_primeira_mensagem(self, 
                                       user_id: str, 
                                       payment_id: str, 
                                       valor_original: float,
                                       pack_name: str,
                                       campaign_id: str):
        """
        Envia primeira mensagem de remarketing após 5 minutos
        """
        try:
            # Aguarda 5 minutos
            await asyncio.sleep(300)  # 300 segundos = 5 minutos
            
            # Verifica se a campanha ainda está ativa
            if campaign_id not in self.active_campaigns:
                return
            
            # Verifica se o pagamento foi realizado
            if await self._verificar_pagamento_realizado(payment_id):
                self.logger.info(f"Pagamento {payment_id} já foi realizado. Cancelando remarketing.")
                self._cancelar_campanha(campaign_id)
                return
            
            # Calcula valor com desconto (50% off)
            valor_desconto = valor_original * 0.5
            
            # Texto provocativo e persuasivo
            texto_remarketing_1 = f"""🔥 **ÚLTIMA CHANCE - OFERTA RELÂMPAGO!** ⚡

😱 Ei! Vi que você estava interessado no {pack_name}...

💸 **PERDEU A CHANCE?** Não se preocupe!

🎯 **OFERTA EXCLUSIVA PARA VOCÊ:**
• {pack_name} por apenas **R$ {valor_desconto:.2f}**
• 🔥 **50% DE DESCONTO** (era R$ {valor_original:.2f})
• ⏰ **VÁLIDO POR APENAS 10 MINUTOS!**

🚀 **POR QUE ESTA OFERTA É IMPERDÍVEL:**
✅ Mesmo conteúdo premium
✅ Acesso imediato após pagamento
✅ Suporte VIP incluso
✅ Garantia de 7 dias

⚠️ **ATENÇÃO:** Esta é uma oferta única e personalizada!

💰 **Economize R$ {valor_original - valor_desconto:.2f} AGORA!**

👇 **CLIQUE AQUI PARA GARANTIR:**
/gerarpix {valor_desconto:.2f} {pack_name} - Oferta 50% OFF

⏳ Restam apenas **10 minutos** para aproveitar!

🔥 Não deixe essa oportunidade passar! 🔥"""
            
            # Envia vídeo com texto
            video_path = "fotos/1.mp4"
            if os.path.exists(video_path):
                with open(video_path, 'rb') as video:
                    await self.bot.send_video(
                        chat_id=user_id,
                        video=video,
                        caption=texto_remarketing_1,
                        parse_mode='Markdown'
                    )
            else:
                # Se não encontrar o vídeo, envia apenas o texto
                await self.bot.send_message(
                    chat_id=user_id,
                    text=texto_remarketing_1,
                    parse_mode='Markdown'
                )
            
            # Registra envio da primeira mensagem
            self.active_campaigns[campaign_id]["primeira_mensagem_enviada"] = datetime.now().isoformat()
            
            self.logger.info(f"📱 Primeira mensagem de remarketing enviada para {user_id}")
            
        except TelegramError as e:
            self.logger.error(f"Erro do Telegram ao enviar primeira mensagem: {e}")
        except Exception as e:
            self.logger.error(f"Erro ao enviar primeira mensagem de remarketing: {e}")
    
    async def _enviar_segunda_mensagem(self, 
                                      user_id: str, 
                                      payment_id: str, 
                                      valor_original: float,
                                      pack_name: str,
                                      campaign_id: str):
        """
        Envia segunda mensagem de remarketing após 15 minutos total (10 minutos após a primeira)
        """
        try:
            # Aguarda 15 minutos total (900 segundos)
            await asyncio.sleep(900)  # 900 segundos = 15 minutos
            
            # Verifica se a campanha ainda está ativa
            if campaign_id not in self.active_campaigns:
                return
            
            # Verifica se o pagamento foi realizado
            if await self._verificar_pagamento_realizado(payment_id):
                self.logger.info(f"Pagamento {payment_id} já foi realizado. Cancelando remarketing.")
                self._cancelar_campanha(campaign_id)
                return
            
            # Calcula valor com desconto ainda maior (70% off)
            valor_desconto_final = valor_original * 0.3
            
            # Texto ainda mais persuasivo para última chance
            texto_remarketing_2 = f"""🚨 **ALERTA VERMELHO - ÚLTIMA OPORTUNIDADE!** 🚨

😰 **SÉRIO?** Você ainda não garantiu o {pack_name}?

💥 **OFERTA FINAL - NUNCA MAIS REPETIDA:**
• {pack_name} por apenas **R$ {valor_desconto_final:.2f}**
• 🔥 **70% DE DESCONTO** (era R$ {valor_original:.2f})
• ⏰ **EXPIRA EM 5 MINUTOS!**

🎯 **ESTA É SUA ÚLTIMA CHANCE PORQUE:**
❌ Depois disso, volta ao preço normal
❌ Esta oferta não será repetida
❌ Vagas limitadas restantes

💎 **O QUE VOCÊ ESTÁ PERDENDO:**
🚀 Conteúdo que vale R$ {valor_original:.2f}
🎁 Bônus exclusivos
🏆 Acesso VIP ao grupo
📞 Suporte prioritário

💰 **VOCÊ ECONOMIZA R$ {valor_original - valor_desconto_final:.2f}!**

⚠️ **ATENÇÃO:** Após 5 minutos, esta oferta será removida PERMANENTEMENTE!

🔥 **ÚLTIMA CHANCE - CLIQUE AGORA:**
/gerarpix {valor_desconto_final:.2f} {pack_name} - OFERTA FINAL 70% OFF

⏳ **5 MINUTOS RESTANTES!**

💔 Não se arrependa depois... Esta é sua ÚLTIMA oportunidade!"""
            
            # Envia imagem com texto
            image_path = "fotos/4.jpg"  # Usando 4.jpg como imagem 2
            if os.path.exists(image_path):
                with open(image_path, 'rb') as image:
                    await self.bot.send_photo(
                        chat_id=user_id,
                        photo=image,
                        caption=texto_remarketing_2,
                        parse_mode='Markdown'
                    )
            else:
                # Se não encontrar a imagem, envia apenas o texto
                await self.bot.send_message(
                    chat_id=user_id,
                    text=texto_remarketing_2,
                    parse_mode='Markdown'
                )
            
            # Registra envio da segunda mensagem
            self.active_campaigns[campaign_id]["segunda_mensagem_enviada"] = datetime.now().isoformat()
            self.active_campaigns[campaign_id]["status"] = "completed"
            
            self.logger.info(f"📱 Segunda mensagem de remarketing enviada para {user_id}")
            
            # Agenda limpeza da campanha após 1 hora
            asyncio.create_task(self._limpar_campanha(campaign_id))
            
        except TelegramError as e:
            self.logger.error(f"Erro do Telegram ao enviar segunda mensagem: {e}")
        except Exception as e:
            self.logger.error(f"Erro ao enviar segunda mensagem de remarketing: {e}")
    
    async def _verificar_pagamento_realizado(self, payment_id: str) -> bool:
        """
        Verifica se o pagamento foi realizado consultando os logs
        
        Returns:
            bool: True se o pagamento foi realizado, False caso contrário
        """
        try:
            if not os.path.exists(self.logger_path):
                return False
            
            with open(self.logger_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verifica nos webhooks se há pagamento aprovado
            for webhook in data.get('webhooks', []):
                if (webhook.get('payment_id') == payment_id and 
                    webhook.get('webhook_data', {}).get('status') == 'paid'):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar pagamento: {e}")
            return False
    
    def _cancelar_campanha(self, campaign_id: str):
        """
        Cancela uma campanha de remarketing
        """
        if campaign_id in self.active_campaigns:
            self.active_campaigns[campaign_id]["status"] = "cancelled"
            self.active_campaigns[campaign_id]["cancelled_at"] = datetime.now().isoformat()
            self.logger.info(f"🚫 Campanha de remarketing cancelada: {campaign_id}")
    
    async def _limpar_campanha(self, campaign_id: str):
        """
        Remove campanha da memória após 1 hora
        """
        await asyncio.sleep(3600)  # 1 hora
        if campaign_id in self.active_campaigns:
            del self.active_campaigns[campaign_id]
            self.logger.info(f"🧹 Campanha removida da memória: {campaign_id}")
    
    def obter_campanhas_ativas(self) -> Dict[str, Any]:
        """
        Retorna todas as campanhas ativas
        """
        return self.active_campaigns
    
    def obter_estatisticas_remarketing(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das campanhas de remarketing
        """
        total_campanhas = len(self.active_campaigns)
        campanhas_ativas = sum(1 for c in self.active_campaigns.values() if c['status'] == 'active')
        campanhas_completas = sum(1 for c in self.active_campaigns.values() if c['status'] == 'completed')
        campanhas_canceladas = sum(1 for c in self.active_campaigns.values() if c['status'] == 'cancelled')
        
        return {
            "total_campanhas": total_campanhas,
            "campanhas_ativas": campanhas_ativas,
            "campanhas_completas": campanhas_completas,
            "campanhas_canceladas": campanhas_canceladas,
            "taxa_conclusao": (campanhas_completas / max(total_campanhas, 1)) * 100
        }

# Exemplo de uso
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Configuração
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if BOT_TOKEN:
        remarketing = RemarketingPIX(BOT_TOKEN)
        
        # Exemplo de iniciar campanha
        # asyncio.run(remarketing.iniciar_campanha_remarketing(
        #     user_id="123456789",
        #     payment_id="pix_teste123",
        #     valor_original=97.00,
        #     pack_name="Pack Premium"
        # ))
        
        print("Sistema de remarketing PIX inicializado!")
    else:
        print("❌ Token do bot não encontrado. Configure TELEGRAM_BOT_TOKEN no .env")