import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.behavior_baseline import BehaviorBaseline
from src.scam_matcher import ScamPatternMatcher
from src.family_guardian import FamilyGuardian
from src.cooldown_manager import CooldownManager
import json

class RiskEngine:
    def __init__(self):
        self.baseline = BehaviorBaseline()
        self.matcher = ScamPatternMatcher()
        self.guardian = FamilyGuardian()
        self.cooldown_manager = CooldownManager()
        self.is_trained = False
    
    def train(self, historical_transactions, scam_cases):
        self.baseline.fit(historical_transactions)
        self.matcher.load_cases(scam_cases)
        self.is_trained = True
    
    def evaluate(self, transaction, transaction_id=None):
        if not self.is_trained:
            raise ValueError("引擎尚未训练")
        
        # 1. 行为偏离度
        behavior_score = self.baseline.detect_anomaly(transaction)
        
        # 2. 骗局匹配度
        tx_desc = f"向{transaction['counterparty']}转账{transaction['amount']}元"
        match_result = self.matcher.match(tx_desc)
        scam_score = match_result['max_score']
        pattern_confirmed = scam_score >= 80
        
        # 3. 风险分类
        risk_level = self.guardian.classify_risk(behavior_score, scam_score, pattern_confirmed)
        
        # 4. 干预策略
        intervention = self.guardian.get_intervention(risk_level, behavior_score, scam_score)
        
        # 5. 冷静期
        cooldown = None
        if transaction_id and risk_level in ('low', 'medium', 'high'):
            cooldown = self.cooldown_manager.create_cooldown(
                transaction_id, risk_level, behavior_score, scam_score
            )
        
        return {
            'behavior_score': behavior_score,
            'scam_score': scam_score,
            'pattern_confirmed': pattern_confirmed,
            'risk_level': risk_level,
            'intervention': intervention,
            'cooldown': cooldown,
            'matched_patterns': match_result['matches']
        }