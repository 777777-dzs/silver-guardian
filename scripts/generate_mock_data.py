import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATA_DIR

def generate_normal_transactions():
    """生成正常老人交易序列"""
    np.random.seed(42)
    records = []
    base_date = pd.Timestamp("2025-01-01")
    
    counterparties = [
        ("永辉超市", "超市", 50, 300),
        ("市第一医院", "医院", 100, 800),
        ("国家电网", "水电煤", 100, 300),
        ("自来水公司", "水电煤", 30, 100),
        ("儿子-张伟", "子女", 500, 2000),
        ("女儿-张丽", "子女", 500, 2000),
    ]
    
    for day in range(180):
        date = base_date + pd.Timedelta(days=day)
        if np.random.random() < 0.7:
            n_tx = np.random.randint(1, 3)
            for _ in range(n_tx):
                cp_name, cp_type, low, high = counterparties[np.random.randint(len(counterparties))]
                amount = round(np.random.uniform(low, high), 2)
                hour = np.random.randint(8, 19)
                records.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "hour": hour,
                    "counterparty": cp_name,
                    "counterparty_type": cp_type,
                    "amount": amount,
                    "frequency": 1
                })
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "normal_transactions.csv"), index=False)
    print(f"正常交易数据已生成：{len(df)}条")
    return df

def generate_fraudulent_transactions():
    """生成被诈骗老人的渐进式交易序列"""
    records = []
    
    records.append({"date": "2025-06-01", "hour": 14, "counterparty": "XX健康管理", 
                    "counterparty_type": "保健品", "amount": 300, "frequency": 1})
    records.append({"date": "2025-06-03", "hour": 20, "counterparty": "XX健康管理", 
                    "counterparty_type": "保健品", "amount": 2000, "frequency": 1})
    records.append({"date": "2025-06-05", "hour": 22, "counterparty": "XX健康管理", 
                    "counterparty_type": "保健品", "amount": 20000, "frequency": 1})
    records.append({"date": "2025-06-07", "hour": 23, "counterparty": "XX健康管理", 
                    "counterparty_type": "保健品", "amount": 50000, "frequency": 1})
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, "fraudulent_transactions.csv"), index=False)
    print(f"诈骗交易数据已生成：{len(df)}条")
    return df

if __name__ == "__main__":
    generate_normal_transactions()
    generate_fraudulent_transactions()