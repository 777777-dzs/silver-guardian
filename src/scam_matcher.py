import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATA_DIR

class ScamPatternMatcher:
    def __init__(self):
        self.cases = []
        self.keyword_index = {}
    
    def load_cases(self, cases):
        self.cases = cases
        for case in cases:
            for kw in case['keywords']:
                if kw not in self.keyword_index:
                    self.keyword_index[kw] = []
                self.keyword_index[kw].append(case['id'])
    
    def match(self, transaction_description):
        """基于关键词匹配计算骗局匹配度"""
        matched = []
        max_score = 0
        
        for case in self.cases:
            score = 0
            matched_keywords = []
            for kw in case['keywords']:
                if kw in transaction_description:
                    score += 25
                    matched_keywords.append(kw)
            
            # 检查对手方类型
            if case['type'][:2] in transaction_description:
                score += 20
            
            if score > 0:
                matched.append({
                    'case_id': case['id'],
                    'type': case['type'],
                    'score': min(100, score),
                    'matched_keywords': matched_keywords,
                    'steps': case['steps']
                })
                max_score = max(max_score, min(100, score))
        
        matched.sort(key=lambda x: x['score'], reverse=True)
        return {
            'max_score': max_score,
            'matches': matched[:3]
        }