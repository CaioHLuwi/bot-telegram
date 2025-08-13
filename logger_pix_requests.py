import json
import os
from datetime import datetime
import uuid
from typing import Dict, Any, Optional

class PixRequestLogger:
    """
    Classe para registrar todas as solicitações de PIX com parâmetros UTMify e Pushinpay
    """
    
    def __init__(self, log_file_path: str = "Logs/pix_requests_log.json"):
        self.log_file_path = log_file_path
        self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        """Garante que o arquivo de log existe"""
        if not os.path.exists(self.log_file_path):
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            initial_data = {
                "pix_requests": [],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "description": "Log de todas as solicitações de PIX com parâmetros UTMify e Pushinpay",
                    "version": "1.0"
                }
            }
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def log_pix_request(self, 
                       user_info: Dict[str, Any],
                       pix_data: Dict[str, Any],
                       utm_params: Dict[str, Any],
                       pushinpay_response: Dict[str, Any],
                       utmify_data: Optional[Dict[str, Any]] = None,
                       status: str = "success",
                       errors: list = None,
                       processing_time_ms: Optional[int] = None) -> str:
        """
        Registra uma solicitação de PIX no arquivo de log
        
        Args:
            user_info: Informações do usuário (telegram_id, username, email, phone)
            pix_data: Dados do PIX (valor, descrição, etc.)
            utm_params: Parâmetros UTM para rastreamento
            pushinpay_response: Resposta da API Pushinpay
            utmify_data: Dados preparados para UTMify
            status: Status da operação (success, error, pending)
            errors: Lista de erros, se houver
            processing_time_ms: Tempo de processamento em milissegundos
        
        Returns:
            str: ID único da solicitação
        """
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "request_id": request_id,
            "user_info": user_info,
            "pix_data": pix_data,
            "utm_params": utm_params,
            "pushinpay_response": pushinpay_response,
            "utmify_data": utmify_data,
            "status": status,
            "errors": errors or [],
            "processing_time_ms": processing_time_ms
        }
        
        # Carrega dados existentes
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"pix_requests": [], "metadata": {}}
        
        # Adiciona nova entrada
        data["pix_requests"].append(log_entry)
        
        # Salva dados atualizados
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ PIX request logged: {request_id} - Status: {status}")
        return request_id
    
    def log_webhook_received(self, 
                           webhook_data: Dict[str, Any],
                           payment_id: str,
                           utm_params: Dict[str, Any],
                           utmify_sent: bool = False,
                           utmify_response: Optional[Dict[str, Any]] = None) -> str:
        """
        Registra o recebimento de webhook da Pushinpay
        
        Args:
            webhook_data: Dados completos do webhook
            payment_id: ID do pagamento
            utm_params: Parâmetros UTM extraídos
            utmify_sent: Se os dados foram enviados para UTMify
            utmify_response: Resposta da UTMify
        
        Returns:
            str: ID único do webhook
        """
        webhook_id = f"webhook_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now().isoformat()
        
        webhook_entry = {
            "timestamp": timestamp,
            "webhook_id": webhook_id,
            "type": "webhook_received",
            "payment_id": payment_id,
            "webhook_data": webhook_data,
            "utm_params": utm_params,
            "utmify_sent": utmify_sent,
            "utmify_response": utmify_response,
            "status": "processed" if utmify_sent else "pending"
        }
        
        # Carrega dados existentes
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"pix_requests": [], "metadata": {}}
        
        # Adiciona entrada de webhook
        if "webhooks" not in data:
            data["webhooks"] = []
        data["webhooks"].append(webhook_entry)
        
        # Salva dados atualizados
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📨 Webhook logged: {webhook_id} - Payment: {payment_id}")
        return webhook_id
    
    def get_logs_by_date(self, date_str: str) -> list:
        """
        Recupera logs por data específica (formato: YYYY-MM-DD)
        """
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filtered_logs = []
            for log in data.get("pix_requests", []):
                if log["timestamp"].startswith(date_str):
                    filtered_logs.append(log)
            
            return filtered_logs
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_logs_by_status(self, status: str) -> list:
        """
        Recupera logs por status (success, error, pending)
        """
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filtered_logs = []
            for log in data.get("pix_requests", []):
                if log["status"] == status:
                    filtered_logs.append(log)
            
            return filtered_logs
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas dos logs
        """
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logs = data.get("pix_requests", [])
            webhooks = data.get("webhooks", [])
            
            stats = {
                "total_requests": len(logs),
                "total_webhooks": len(webhooks),
                "status_count": {},
                "utm_sources": {},
                "total_value": 0
            }
            
            for log in logs:
                # Contagem por status
                status = log.get("status", "unknown")
                stats["status_count"][status] = stats["status_count"].get(status, 0) + 1
                
                # Contagem por UTM source
                utm_source = log.get("utm_params", {}).get("utm_source", "unknown")
                stats["utm_sources"][utm_source] = stats["utm_sources"].get(utm_source, 0) + 1
                
                # Valor total
                valor = log.get("pix_data", {}).get("valor_reais", 0)
                if isinstance(valor, (int, float)):
                    stats["total_value"] += valor
            
            return stats
        except (FileNotFoundError, json.JSONDecodeError):
            return {"error": "Arquivo de log não encontrado ou corrompido"}

# Exemplo de uso
if __name__ == "__main__":
    logger = PixRequestLogger()
    
    # Exemplo de log de solicitação PIX
    user_info = {
        "telegram_id": "123456789",
        "username": "@usuario_teste",
        "email": "teste@email.com",
        "phone": "+5511999999999"
    }
    
    pix_data = {
        "valor_reais": 97.00,
        "descricao": "Pack Premium - Teste",
        "payment_id": "pix_teste123"
    }
    
    utm_params = {
        "utm_source": "telegram",
        "utm_medium": "bot",
        "utm_campaign": "teste_2024",
        "utm_content": "pack_premium",
        "utm_term": "teste"
    }
    
    pushinpay_response = {
        "success": True,
        "payment_id": "pix_teste123",
        "qr_code": "00020126580014BR.GOV.BCB.PIX...",
        "amount": 97.00,
        "status": "pending"
    }
    
    # Registra a solicitação
    request_id = logger.log_pix_request(
        user_info=user_info,
        pix_data=pix_data,
        utm_params=utm_params,
        pushinpay_response=pushinpay_response,
        status="success",
        processing_time_ms=1250
    )
    
    print(f"Request ID gerado: {request_id}")
    
    # Mostra estatísticas
    stats = logger.get_statistics()
    print(f"Estatísticas: {json.dumps(stats, indent=2, ensure_ascii=False)}")