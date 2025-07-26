import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BotMetrics:
    def __init__(self, metrics_file: str = 'bot_metrics.json'):
        self.metrics_file = metrics_file
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Carregar métricas do arquivo JSON"""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f'Erro ao carregar métricas: {e}')
                return self._create_empty_metrics()
        else:
            return self._create_empty_metrics()
    
    def _create_empty_metrics(self) -> Dict:
        """Criar estrutura vazia de métricas"""
        return {
            'total_users': 0,
            'daily_stats': {},
            'user_interactions': {},
            'conversion_stats': {
                'total_conversations': 0,
                'payments_12': 0,
                'payments_5': 0,
                'total_revenue': 0.0
            },
            'hourly_stats': {str(i): 0 for i in range(24)},
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_metrics(self):
        """Salvar métricas no arquivo JSON"""
        try:
            self.metrics['last_updated'] = datetime.now().isoformat()
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f'Erro ao salvar métricas: {e}')
    
    def log_user_start(self, user_id: int, username: str = None, first_name: str = None):
        """Registrar início de conversa de um usuário"""
        today = datetime.now().strftime('%Y-%m-%d')
        hour = datetime.now().hour
        
        # Verificar se é um novo usuário
        is_new_user = str(user_id) not in self.metrics['user_interactions']
        
        if is_new_user:
            self.metrics['total_users'] += 1
            self.metrics['user_interactions'][str(user_id)] = {
                'first_interaction': datetime.now().isoformat(),
                'username': username,
                'first_name': first_name,
                'total_conversations': 0,
                'payments': [],
                'last_interaction': datetime.now().isoformat()
            }
        
        # Atualizar estatísticas diárias
        if today not in self.metrics['daily_stats']:
            self.metrics['daily_stats'][today] = {
                'new_users': 0,
                'total_conversations': 0,
                'payments': 0,
                'revenue': 0.0
            }
        
        if is_new_user:
            self.metrics['daily_stats'][today]['new_users'] += 1
        
        self.metrics['daily_stats'][today]['total_conversations'] += 1
        self.metrics['conversion_stats']['total_conversations'] += 1
        
        # Atualizar estatísticas por hora
        self.metrics['hourly_stats'][str(hour)] += 1
        
        # Atualizar dados do usuário
        self.metrics['user_interactions'][str(user_id)]['total_conversations'] += 1
        self.metrics['user_interactions'][str(user_id)]['last_interaction'] = datetime.now().isoformat()
        
        self._save_metrics()
        
        logger.info(f'Usuário {user_id} ({username or "sem username"}) iniciou conversa. Novo usuário: {is_new_user}')
    
    def log_payment(self, user_id: int, amount: float, payment_type: str):
        """Registrar pagamento realizado"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        payment_data = {
            'amount': amount,
            'type': payment_type,
            'date': datetime.now().isoformat()
        }
        
        # Atualizar dados do usuário
        if str(user_id) in self.metrics['user_interactions']:
            self.metrics['user_interactions'][str(user_id)]['payments'].append(payment_data)
        
        # Atualizar estatísticas de conversão
        if payment_type == 'pack_12':
            self.metrics['conversion_stats']['payments_12'] += 1
        elif payment_type == 'pack_5':
            self.metrics['conversion_stats']['payments_5'] += 1
        
        self.metrics['conversion_stats']['total_revenue'] += amount
        
        # Atualizar estatísticas diárias
        if today in self.metrics['daily_stats']:
            self.metrics['daily_stats'][today]['payments'] += 1
            self.metrics['daily_stats'][today]['revenue'] += amount
        
        self._save_metrics()
        
        logger.info(f'Pagamento registrado: Usuário {user_id}, Valor: R$ {amount:.2f}, Tipo: {payment_type}')
    
    def get_daily_stats(self, days: int = 7) -> Dict:
        """Obter estatísticas dos últimos N dias"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'period': f'{start_date.strftime("%Y-%m-%d")} a {end_date.strftime("%Y-%m-%d")}',
            'days': [],
            'totals': {
                'new_users': 0,
                'conversations': 0,
                'payments': 0,
                'revenue': 0.0
            }
        }
        
        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            day_stats = self.metrics['daily_stats'].get(date, {
                'new_users': 0,
                'total_conversations': 0,
                'payments': 0,
                'revenue': 0.0
            })
            
            stats['days'].append({
                'date': date,
                **day_stats
            })
            
            stats['totals']['new_users'] += day_stats['new_users']
            stats['totals']['conversations'] += day_stats['total_conversations']
            stats['totals']['payments'] += day_stats['payments']
            stats['totals']['revenue'] += day_stats['revenue']
        
        return stats
    
    def get_conversion_rate(self) -> Dict:
        """Calcular taxa de conversão"""
        total_conversations = self.metrics['conversion_stats']['total_conversations']
        total_payments = self.metrics['conversion_stats']['payments_12'] + self.metrics['conversion_stats']['payments_5']
        
        conversion_rate = (total_payments / total_conversations * 100) if total_conversations > 0 else 0
        
        return {
            'total_conversations': total_conversations,
            'total_payments': total_payments,
            'conversion_rate': round(conversion_rate, 2),
            'payments_12': self.metrics['conversion_stats']['payments_12'],
            'payments_5': self.metrics['conversion_stats']['payments_5'],
            'total_revenue': round(self.metrics['conversion_stats']['total_revenue'], 2),
            'average_ticket': round(self.metrics['conversion_stats']['total_revenue'] / total_payments, 2) if total_payments > 0 else 0
        }
    
    def get_hourly_distribution(self) -> Dict:
        """Obter distribuição de conversas por hora"""
        total_interactions = sum(self.metrics['hourly_stats'].values())
        
        hourly_data = []
        for hour in range(24):
            count = self.metrics['hourly_stats'][str(hour)]
            percentage = (count / total_interactions * 100) if total_interactions > 0 else 0
            
            hourly_data.append({
                'hour': f'{hour:02d}:00',
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        return {
            'total_interactions': total_interactions,
            'hourly_data': hourly_data
        }
    
    def get_summary(self) -> Dict:
        """Obter resumo geral das métricas"""
        today_stats = self.get_daily_stats(1)['days'][0] if self.get_daily_stats(1)['days'] else {
            'new_users': 0, 'total_conversations': 0, 'payments': 0, 'revenue': 0.0
        }
        
        return {
            'total_users': self.metrics['total_users'],
            'today': today_stats,
            'conversion': self.get_conversion_rate(),
            'last_updated': self.metrics['last_updated']
        }
    
    def export_user_list(self) -> List[Dict]:
        """Exportar lista de usuários com suas informações"""
        users = []
        for user_id, data in self.metrics['user_interactions'].items():
            user_info = {
                'user_id': user_id,
                'username': data.get('username', 'N/A'),
                'first_name': data.get('first_name', 'N/A'),
                'first_interaction': data['first_interaction'],
                'last_interaction': data['last_interaction'],
                'total_conversations': data['total_conversations'],
                'total_payments': len(data['payments']),
                'total_spent': sum(p['amount'] for p in data['payments'])
            }
            users.append(user_info)
        
        # Ordenar por última interação
        users.sort(key=lambda x: x['last_interaction'], reverse=True)
        return users

# Instância global das métricas
bot_metrics = BotMetrics()