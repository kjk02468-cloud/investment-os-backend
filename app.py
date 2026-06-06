import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Investment OS - 지정학·공급망", layout="wide")
st.title("🧠 Investment OS : AI Infra + Geopolitics")

col1, col2 = st.columns([7, 3])
with col1:
    st.subheader(f"현재 시점: {datetime.now().strftime('%Y-%m-%d %H:%M')} KST")

# 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 이벤트", "🔗 Value Chain", "📊 Macro Dashboard", "⚠️ Risk Matrix", "🤖 AI Agent"])

with tab1:
    st.subheader("Scheduled & Unscheduled Events")
    # 여기에 이전에 준 내용 + 실시간 업데이트 로직

with tab2:
    st.subheader("Value Chain 현황")
    # HBM, Power, Rare Earth, Hormuz 등 차트/이미지

with tab3:
    st.subheader("Macro Dashboard")

with tab4:
    st.subheader("Risk Scenario Matrix")

with tab5:
    st.subheader("AI Reasoning Agent")
    query = st.text_input("오늘 어떤 이벤트/종목 분석해줄까?")
    if st.button("분석 시작"):
        # Ollama 호출 로직
        st.info("Agent thinking...")