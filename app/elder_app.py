import streamlit as st
import pandas as pd
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATA_DIR
from src.risk_engine import RiskEngine
from src.utils import load_transactions, load_scam_cases

st.set_page_config(page_title="工银e伴安·老人端", page_icon="🛡️", layout="wide")

st.title("🛡️ 工银e伴安 · 老人端")
st.caption("银发金融安全协同平台｜守护养老资金安全")

# 加载数据
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
    st.header("📋 使用说明")
    st.markdown("""
    1. 查看您的养老金健康度
    2. 收到风险提示时请确认
    3. 高风险交易有冷静期保护
    4. 可一键联系子女或客服
    """)
    st.header("🏦 工行服务")
    st.info("本平台嵌入工商银行手机银行幸福生活版")

# 主界面
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💚 养老金健康度")
    
    # 模拟健康度评分
    health_score = 92
    st.metric("当前健康度", f"{health_score}/100", delta="正常")
    
    # 健康度仪表盘
    fig = {
        "data": [{
            "type": "indicator",
            "mode": "gauge+number",
            "value": health_score,
            "title": {"text": "养老金健康度"},
            "gauge": {
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2ecc71"},
                "steps": [
                    {"range": [0, 40], "color": "#ffcccc"},
                    {"range": [40, 70], "color": "#fff3cc"},
                    {"range": [70, 100], "color": "#ccffcc"}
                ]
            }
        }],
        "layout": {"height": 300}
    }
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📢 风险提示")
    st.success("暂无风险提示，您的账户安全")
    st.button("📞 一键联系子女")
    st.button("💬 联系客服")

# 交易记录
st.subheader("📊 近期交易")
normal_tx = pd.read_csv(os.path.join(DATA_DIR, "normal_transactions.csv"))
recent = normal_tx.tail(10)
st.dataframe(recent, use_container_width=True)

# 冷静期提示
st.subheader("⏳ 冷静期状态")
st.info("当前无进行中的冷静期")