import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import COOLDOWN_CONFIG

class CooldownManager:
    def __init__(self):
        self.config = COOLDOWN_CONFIG
        self.active_cooldowns = {}  # {transaction_id: {...}}
    
    def create_cooldown(self, transaction_id, risk_level, behavior_score, scam_score):
        """创建冷静期记录"""
        cfg = self.config[risk_level]
        cooldown = {
            'transaction_id': transaction_id,
            'risk_level': risk_level,
            'behavior_score': behavior_score,
            'scam_score': scam_score,
            'cooldown_hours': cfg['hours'],
            'notify_family': cfg['notify_family'],
            'can_extend': cfg.get('can_extend', False),
            'extended': False,
            'family_confirmed': False,
            'status': 'active'
        }
        self.active_cooldowns[transaction_id] = cooldown
        return cooldown
    
    def family_confirm_risk(self, transaction_id):
        """子女确认有风险，触发冷静期延长"""
        if transaction_id not in self.active_cooldowns:
            return {'error': '冷静期记录不存在'}
        
        cooldown = self.active_cooldowns[transaction_id]
        
        if not cooldown['can_extend']:
            return {
                'action': 'no_extend',
                'message': '当前风险等级无需延长冷静期'
            }
        
        cooldown['extended'] = True
        cooldown['family_confirmed'] = True
        cooldown['cooldown_hours'] = self.config['medium']['extended_hours']  # 72小时
        cooldown['status'] = 'extended'
        
        return {
            'action': 'extend_cooldown',
            'new_cooldown_hours': cooldown['cooldown_hours'],
            'transfer_to_manual': True,
            'message_to_elder': '您的家人对此交易有疑问，客服将与您联系确认',
            'message_to_family': '已确认风险，冷静期已延长至72小时，客服将介入'
        }
    
    def get_cooldown(self, transaction_id):
        return self.active_cooldowns.get(transaction_id)
    
    def get_all_active(self):
        return [c for c in self.active_cooldowns.values() if c['status'] in ('active', 'extended')]