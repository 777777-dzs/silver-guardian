import os

# 工行绑定配置（Demo阶段模拟）
ICBC_API_BASE = os.getenv("ICBC_API_BASE", "https://mock.icbc.com/api")
ICBC_APP_ID = os.getenv("ICBC_APP_ID", "silver_guardian_demo")
ICBC_APP_SECRET = os.getenv("ICBC_APP_SECRET", "demo_secret")

# 风险阈值
RISK_THRESHOLDS = {
    "low": {"behavior": (30, 60), "scam": (30, 60)},
    "medium": {"behavior": (60, 80), "scam": (60, 80)},
    "high": {"behavior": (80, 100), "scam": (80, 100)},
}

# 冷静期配置（修订版）
COOLDOWN_CONFIG = {
    "low": {"hours": 4, "notify_family": False, "can_extend": False},
    "medium": {"hours": 24, "notify_family": True, "can_extend": True, "extended_hours": 72},
    "high": {"hours": 72, "notify_family": True, "can_extend": False, "requires_manual": True},
}

# 数据路径
DATA_DIR = os.path.join(os.path.dirname(__file__), "../数据")
os.makedirs(DATA_DIR, exist_ok=True)
