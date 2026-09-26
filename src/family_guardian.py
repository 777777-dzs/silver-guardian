import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.settings import RISK_THRESHOLDS

class FamilyGuardian:
    def __init__(self):
        self.thresholds = RISK_THRESHOLDS
    
    def classify_risk(self, behavior_score, scam_score, pattern_confirmed=False):
        """根据双维度评分和模式确认，判定风险等级"""
        
        # 高风险：双维度≥80 且 模式确认
        if behavior_score >= 80 and scam_score >= 80:
            return 'high'
        if pattern_confirmed and (behavior_score >= 80 or scam_score >= 80):
            return 'high'
        
        # 中风险：单维度60-80，或双维度30-60
        if 60 <= behavior_score < 80 or 60 <= scam_score < 80:
            return 'medium'
        if 30 <= behavior_score < 60 and 30 <= scam_score < 60:
            return 'medium'
        
        # 低风险：单维度30-60
        if 30 <= behavior_score < 60 or 30 <= scam_score < 60:
            return 'low'
        
        return 'normal'
    
    def get_intervention(self, risk_level, behavior_score, scam_score):
        """返回干预策略"""
        if risk_level == 'normal':
            return {
                'level': 'normal',
                'action': 'none',
                'notify_elder': False,
                'notify_family': False
            }
        elif risk_level == 'low':
            return {
                'level': 'low',
                'action': 'notify_elder',
                'notify_elder': True,
                'notify_family': False,
                'message': '今日有一笔交易与您平时习惯略有不同，请确认是否本人操作'
            }
        elif risk_level == 'medium':
            return {
                'level': 'medium',
                'action': 'notify_elder_and_family',
                'notify_elder': True,
                'notify_family': True,
                'message_to_elder': '检测到一笔交易与您平时习惯明显不同，请确认是否本人操作',
                'message_to_family': '您的家人今日有一笔异常转账行为，请确认是否知情',
                'can_extend': True
            }
        else:  # high
            return {
                'level': 'high',
                'action': 'cooldown_and_notify',
                'notify_elder': True,
                'notify_family': True,
                'message_to_elder': '检测到高风险交易，已启动冷静期，请谨慎操作',
                'message_to_family': '检测到高风险交易，已启动冷静期，请尽快与家人确认',
                'requires_manual': True
            }