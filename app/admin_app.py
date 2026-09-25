import streamlit as st
import pandas as pd
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATA_DIR
from src.risk_engine import RiskEngine
from src.utils import load_transactions, load_scam_cases

st.set_page_config(page_title="银发守护·后台", page_icon="⚙️", layout="wide")

st.title("⚙️ 银发守护 · 后台管理端")
st.caption("养老资金安全智能守护平台 · 运营管理")

# 加载引擎
@st.cache_resource
def init_engine():
    normal_tx = load_transactions(os.path.join(DATA_DIR, "normal_transactions.csv"))
    scam_cases = load_scam_cases(os.path.join(DATA_DIR, "scam_cases.json"))
    engine = RiskEngine()
    engine.train(normal_tx, scam_cases)
    return engine

engine = init_engine()

# 标签页
tab1, tab2, tab3, tab4 = st.tabs(["📊 风险总览", "⏳ 冷静期管理", "📚 骗局知识库", "⚙️ 系统配置"])

with tab1:
    st.subheader("风险总览")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("今日交易", "1,234")
    col2.metric("低风险", "45", delta="+5")
    col3.metric("中风险", "12", delta="+2")
    col4.metric("高风险", "3", delta="-1")
    
    st.subheader("风险分布")
    risk_data = pd.DataFrame({
        "风险等级": ["正常", "低风险", "中风险", "高风险"],
        "数量": [1174, 45, 12, 3]
    })
    st.bar_chart(risk_data.set_index("风险等级"))

with tab2:
    st.subheader("冷静期管理")
    
    # 模拟冷静期记录
    cooldowns = pd.DataFrame([
        {"交易ID": "TX20250605001", "老人": "张大爷", "对手方": "XX健康管理", 
         "金额": 20000, "风险等级": "高风险", "冷静期": "72小时", 
         "状态": "已延长", "子女确认": "是"},
        {"交易ID": "TX20250605002", "老人": "李奶奶", "对手方": "XX养老公寓", 
         "金额": 50000, "风险等级": "中风险", "冷静期": "24小时", 
         "状态": "进行中", "子女确认": "待确认"},
    ])
    st.dataframe(cooldowns, use_container_width=True)
    
    st.subheader("子女反馈统计")
    st.metric("今日推送", "23")
    st.metric("已确认风险", "5")
    st.metric("已确认正常", "12")
    st.metric("未响应", "6")

with tab3:
    st.subheader("养老诈骗知识库")
    scam_cases = load_scam_cases(os.path.join(DATA_DIR, "scam_cases.json"))
    for case in scam_cases:
        with st.expander(f"🔴 {case['type']}"):
            st.write(f"**描述**：{case['description']}")
            st.write(f"**典型步骤**：{' → '.join(case['steps'])}")
            st.write(f"**关键词**：{', '.join(case['keywords'])}")

with tab4:
    st.subheader("系统配置")
    st.write("**风险阈值**")
    st.json({
        "低风险": {"行为偏离度": "30-60", "骗局匹配度": "30-60"},
        "中风险": {"行为偏离度": "60-80", "骗局匹配度": "60-80"},
        "高风险": {"行为偏离度": "≥80", "骗局匹配度": "≥80"}
    })
    
    st.write("**冷静期配置**")
    st.json({
        "低风险": {"冷静期": "4小时", "通知子女": False},
        "中风险": {"冷静期": "24小时", "通知子女": True, "可延长": True},
        "高风险": {"冷静期": "72小时", "通知子女": True, "转人工": True}
    })