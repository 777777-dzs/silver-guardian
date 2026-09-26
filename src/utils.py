import pandas as pd
import json

def load_transactions(filepath):
    df = pd.read_csv(filepath)
    return df.to_dict('records')

def load_scam_cases(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)