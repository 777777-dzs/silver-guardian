import streamlit as st
import pandas as pd
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATA_DIR
from src.risk_engine import RiskEngine
from src.utils import load_transactions, load_scam_cases

st.set_page_config(page_title="银发守护·子女端", page_icon="👨‍👩‍👧", layout="wide")

st.title("👨‍👩‍👧 银发守护 · 子女端")
st.caption("银发金融安全协同平台｜亲情风险预警提醒")

# 加载引擎
@st.cache_resource
def init_engine():
    normal_tx = load_transactions(os.path.join(DATA_DIR, "normal_transactions.csv"))
    scam_cases = load_scam_cases(os.path.join(DATA_DIR, "scam_cases.json"))
    engine = RiskEngine()
    engine.train(normal_tx, scam_cases)
    return engine

engine = init_engine()

# 侧边栏
with st.sidebar:
    st.header("👤 家人信息")
    st.write("**张大爷**（父亲）")
    st.write("年龄：72岁")
    st.write("账户：尾号8823")
    
    st.header("🔔 通知设置")
    st.checkbox("接收脱敏风险提示", value=True)
    st.checkbox("高风险时电话通知", value=True)

# 主界面
st.subheader("📊 家人养老金健康度趋势")

# 模拟趋势数据
trend_data = pd.DataFrame({
    "日期": pd.date_range("2025-06-01", periods=14, freq="D"),
    "健康度": [92, 91, 93, 92, 90, 88, 85, 80, 75, 68, 60, 55, 50, 45]
})

st.line_chart(trend_data.set_index("日期"))

# 风险提示
st.subheader("⚠️ 风险提示")

# 模拟一条中风险提示
st.warning("""
**中风险提示**（2025-06-05 22:30）

您的家人今日有一笔异常转账行为：
- 交易对手：XX健康管理
- 交易特征：夜间22:30转账，金额20000元
- 偏离度：82/100
- 骗局匹配：保健品投资返利骗局（匹配度91%）

**请确认是否知情：**
""")

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 我知情，交易正常"):
        st.success("已反馈：交易正常。系统将记录该交易为正常样本，优化后续检测。")
with col2:
    if st.button("🚨 我怀疑这笔交易有问题"):
        st.error("""
        已确认风险！系统已执行以下操作：
        1. 冷静期延长至72小时
        2. 转人工客服介入
        3. 已通知老人：您的家人对此交易有疑问，客服将与您联系
        """)

# 冷静期状态
st.subheader("⏳ 冷静期状态")
st.info("当前有1笔交易处于冷静期：XX健康管理 20000元（高风险·72小时）")