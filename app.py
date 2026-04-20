import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. 頁面配置
st.set_page_config(page_title="智慧化 ESG 能源監控平台", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS 優化 (隱藏側邊欄、巨大金額、精緻卡片樣式)
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        .main .block-container { padding-top: 1rem; }
        
        .big-amount-container {
            text-align: center;
            margin: 10px 0 25px 0;
            padding: 20px;
            background-color: rgba(255, 75, 75, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 75, 75, 0.2);
        }
        .amount-label { color: #BBBBBB; font-size: 24px; }
        .amount-value { color: #FF4B4B; font-size: 80px; font-weight: bold; font-family: 'Courier New', monospace; }
        
        .metric-box {
            border: 2px solid #00FF00;
            padding: 15px;
            border-radius: 10px;
            background-color: rgba(0, 255, 0, 0.05);
            text-align: center;
            height: 110px;
        }
        .metric-title { font-size: 14px; color: #BBBBBB; }
        .metric-value { font-size: 24px; font-weight: bold; color: #FFFFFF; }
        
        .strategy-card {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #00FF00;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 超詳細數據模擬
def get_detailed_data():
    # 總體指標
    total_load = 1304.7
    emission_factor = 0.424
    carbon_emission = round(total_load * emission_factor, 2)
    actual_amount = round(carbon_emission * 10, 2)
    
    # 1F 極細項清單
    df_1f = pd.DataFrame({
        '區域': '1F',
        '具體設備': ['大廳空調', '西側辦公區空調', '走廊LED燈', '展示區照明', '電梯A電力', '公共插座', '飲水機', '自動門系統'],
        '功耗 (kW)': [250.2, 200.0, 60.5, 60.0, 45.3, 35.0, 15.6, 13.0]
    })
    
    # 4F 極細項清單
    df_4f = pd.DataFrame({
        '區域': '4F',
        '具體設備': ['數據中心主機', '伺服器機櫃', '會議室空調', '高階辦公區照明', 'UPS 備援系統', '影印室電力', '門禁感應器', '茶水間設備'],
        '功耗 (kW)': [320.0, 100.0, 100.0, 40.0, 30.2, 15.0, 10.0, 10.0]
    })
    
    # 樓層匯總數據 (用於圓餅圖)
    f1_total = df_1f['功耗 (kW)'].sum()
    f4_total = df_4f['功耗 (kW)'].sum()
    
    return total_load, carbon_emission, actual_amount, df_1f, df_4f, f1_total, f4_total, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

total_load, carbon_emission, actual_amount, df_1f, df_4f, f1_sum, f4_sum, current_time = get_detailed_data()

# 4. 頂部區域
t_col1, t_col2 = st.columns([0.8, 0.2])
with t_col1:
    st.markdown("## 🏛️ 智慧化 ESG 能源監控平台")
with t_col2:
    if st.button("🔄 立即刷新數據", use_container_width=True):
        st.rerun()
st.markdown(f"**數據更新時間：** `{current_time}` | **電力排放係數：** :green[0.424]")

# 5. 巨大金額
st.markdown(f"""
    <div class="big-amount-container">
        <div class="amount-label">💰 預估碳成本金額</div>
        <div class="amount-value">NT$ {actual_amount:,.1f}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 四格核心指標
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box"><div class="metric-title">全區總負載</div><div class="metric-value">{total_load} kW</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-box"><div class="metric-title">即時總碳排</div><div class="metric-value">{carbon_emission} kg/h</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-title">1F 區域總負載</div><div class="metric-value">{f1_sum:.1f} kW</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box"><div class="metric-title">4F 區域總負載</div><div class="metric-value">{f4_sum:.1f} kW</div></div>', unsafe_allow_html=True)

st.write("---")

# 7. 圖表區 (圓餅圖 + 設備長條圖)
st.markdown("### 📊 負載分佈可視化")
chart_l, chart_r = st.columns([1, 1.2])

with chart_l:
    st.markdown("#### 1F vs 4F 佔比圖")
    fig_pie = px.pie(values=[f1_sum, f4_sum], names=['1F 區域', '4F 區域'], hole=0.4,
                     color_discrete_sequence=['#108c71', '#4caf50'])
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_r:
    st.markdown("#### 跨區域設備功耗對比")
    # 提取兩層樓前 4 大設備做對比
    df_compare = pd.concat([df_1f.head(4), df_4f.head(4)])
    fig_bar = px.bar(df_compare, x='具體設備', y='功耗 (kW)', color='區域', barmode='group',
                     color_discrete_map={'1F': '#108c71', '4F': '#4caf50'})
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("---")

# 8. 詳細設備清單 (兩欄表格)
st.markdown("### 📋 設備細項功耗明細表 (全記錄)")
tab_l, tab_r = st.columns(2)

with tab_l:
    st.info("🏠 1F 區域設備細項")
    st.dataframe(df_1f, use_container_width=True, hide_index=True)

with tab_r:
    st.success("🏢 4F 區域設備細項")
    st.dataframe(df_4f, use_container_width=True, hide_index=True)

st.write("---")

# 9. 底部策略建議
st.markdown("### 💡 智能節能決策系統")
s1, s2 = st.columns(2)
with s1:
    st.markdown("""<div class="strategy-card"><b>🌱 即時節能建議</b><br>
    • 1F <b>大廳空調</b> 負載異常，建議檢查過濾網。<br>
    • 4F <b>數據中心</b> 目前負載極高，建議啟動自然冷卻模式。</div>""", unsafe_allow_html=True)
with s2:
    st.markdown("""<div class="strategy-card"><b>🎮 區域控制策略</b><br>
    • 晚上 10 點後強制關閉 1F 走廊燈及展示區電源。<br>
    • 針對 4F 閒置伺服器執行虛擬化休眠以節省 10% 電力。</div>""", unsafe_allow_html=True)