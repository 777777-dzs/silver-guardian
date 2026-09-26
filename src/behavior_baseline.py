import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

class BehaviorBaseline:
    def __init__(self):
        self.lof = LocalOutlierFactor(novelty=True)
        self.ocsvm = OneClassSVM(kernel='rbf', nu=0.1)
        self.iforest = IsolationForest(contamination=0.1)
        self.is_fitted = False
        self.counterparty_map = {}
        self.counterparty_counter = 0
    
    def _encode_counterparty(self, name):
        if name not in self.counterparty_map:
            self.counterparty_map[name] = self.counterparty_counter
            self.counterparty_counter += 1
        return self.counterparty_map[name]
    
    def extract_features(self, transactions):
        features = []
        for tx in transactions:
            features.append([
                self._encode_counterparty(tx['counterparty']),
                tx['amount'],
                tx['hour'],
                tx.get('frequency', 1)
            ])
        return np.array(features)
    
    def fit(self, transactions):
        features = self.extract_features(transactions)
        if len(features) < 5:
            raise ValueError("训练数据太少，至少需要5条交易")
        self.lof.fit(features)
        self.ocsvm.fit(features)
        self.iforest.fit(features)
        self.is_fitted = True
    
    def detect_anomaly(self, transaction):
        if not self.is_fitted:
            raise ValueError("模型尚未训练")
        features = self.extract_features([transaction])
        
        try:
            score_lof = -self.lof.score_samples(features)[0]
        except:
            score_lof = 0
        try:
            score_svm = -self.ocsvm.score_samples(features)[0]
        except:
            score_svm = 0
        try:
            score_if = -self.iforest.score_samples(features)[0]
        except:
            score_if = 0
        
        # 加权融合
        final_score = 0.3 * score_lof + 0.3 * score_svm + 0.4 * score_if
        # 归一化到0-100
        normalized = min(100, max(0, abs(final_score) * 80))
        return round(normalized, 2)