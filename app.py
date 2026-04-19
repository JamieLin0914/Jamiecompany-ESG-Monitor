import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from finance import SMB_CarbonAccounting # 抓finance.py的東西來用

class JamiecompanyESGManager:
    def __init__(self):
        # 電力排放係數
        self.carbon_factor = 0.424
        self.carbon_tax_rate = 300 
        
    def fetch_live_signals(self):
        areas = {
            '1F': ['A_Zone', 'B_Zone', 'C_Zone'],
            '4F': ['D_Zone', 'E_Zone', 'F_Zone']
        }
        devices = ['燈光照明', '插座用電', '冷氣用電']
        
        data = []
        for floor, zones in areas.items():
            for zone in zones:
                for device in devices:
                    tag = f"Jamiecompany_{floor}_{zone}_{device}"
                    if "冷氣" in device:
                        val = np.random.uniform(120.0, 180.0) 
                    elif "插座" in device:
                        val = np.random.uniform(40.0, 60.0)
                    elif "燈光" in device:
                        val = np.random.uniform(15.0, 35.0)
                    else:
                        val = np.random.uniform(5.0, 20.0)

                    data.append({
                        "樓層": floor,
                        "區域": zone,
                        "設備類型": device,
                        "點位標籤": tag,
                        "即時功耗(kW)": round(val, 2)
                    })
        
        df = pd.DataFrame(data)
        df["碳排當量(kg)"] = round(df["即時功耗(kW)"] * self.carbon_factor, 2)
        df["預估碳費(TWD)"] = round((df["碳排當量(kg)"] / 1000) * self.carbon_tax_rate, 4)
        return df

def main():
    st.set_page_config(page_title="EcoPay 企業 ESG 管理系統", layout="wide")
    
    # 1. 先抓取數據
    st.sidebar.title("🌿 EcoPay 管理後台")
    st.sidebar.markdown("服務中小企業，達成智慧化 ESG 轉型。")
    page = st.sidebar.radio("請選擇操作視窗：", ["📊 即時能源監控", "💰 會計碳稅日結"])
    
    manager = JamiecompanyESGManager()
    df = manager.fetch_live_signals()

    st.markdown("""
        <style>
        header {visibility: hidden;}
        .main .block-container {
            padding-top: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin-top: -50px;
        }
        .block-container { padding-top: 1rem !important; }
        .stApp { background-color: #0E1117; }
        h1, h2, h3, p, span, label { color: #FFFFFF !important; }
        [data-testid="stSidebar"] { background-color: #161B22 !important; }
        [data-testid="stMetricValue"] { color: #00FF41 !important; }
        [data-testid="stMetricLabel"] { color: #CCCCCC !important; }
        [data-testid="stMetric"] { background-color: #161B22; border: 1px solid #00FF41; padding: 10px; border-radius: 10px; }
                
        div.stButton > button {
            background-color: #161B22 !important; /* 按鈕背景深色 */
            color: #FFFFFF !important;            /* 文字白色 */
            border: 2px solid #00FF41 !important; /* 螢光綠邊框 */
            border-radius: 10px !important;       /* 圓角 */
            padding: 10px 24px !important;        /* 間距 */
            transition: all 0.3s ease !important; /* 動畫效果 */
        }

        div.stButton > button:hover {
            background-color: #00FF41 !important; /* 背景變綠色 */
            color: #0E1117 !important;            /* 文字變黑色 */
            box-shadow: 0 0 15px #00FF41 !important; /* 發光效果 */
        }
                
        div.stButton > button:active {
            transform: scale(0.95) !important;    /* 縮放一下的感覺 */
        }
                
                [data-testid="stElementToolbar"] {
            background-color: transparent !important; /* 讓背景透明 */
            right: 1rem !important;
        }
                
        div[data-testid="stElementToolbar"] > div {
            background-color: #161B22 !important; /* 改為深灰色 */
            border: 1px solid #00FF41 !important; /* 加上綠色邊框更有質感 */
            border-radius: 5px;
        }

        [data-testid="stElementToolbar"] svg {
            fill: #00FF41 !important;
        }

        .stDataFrame, [data-testid="stTable"] {
            background-color: #0E1117 !important;
        }

        input[aria-label="Search records"] {
            color: #FFFFFF !important;
        }
                
        .streamlit-expanderHeader p {
            color: #FFFFFF !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }

        .streamlit-expanderContent {
            color: #FFFFFF !important;
            background-color: #161B22 !important; /* 讓內容背景深一點點，增加層次感 */
        }
                
        .streamlit-expanderHeader svg {
            fill: #00FF41 !important;
        }

        .streamlit-expanderContent li {
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.subheader("🕹️ 節能策略模擬")
    strategy_light = st.sidebar.toggle("燈光亮度減半 (50%)", key="s_light_unique")
    strategy_ac = st.sidebar.toggle("冷氣進入環保模式 (+2°C)", key="s_ac_unique")

    # 3. 【核心計算】這段要放在所有 if 顯示之前！
    if strategy_light:
        df.loc[df['設備類型'] == '燈光照明', '即時功耗(kW)'] *= 0.5
    if strategy_ac:
        df.loc[df['設備類型'] == '冷氣用電', '即時功耗(kW)'] *= 0.8
    
    # 重新計算碳排與碳費 (確保數據是最新的)
    df["碳排當量(kg)"] = round(df["即時功耗(kW)"] * manager.carbon_factor, 2)
    df["預估碳費(TWD)"] = round((df["碳排當量(kg)"] / 1000) * manager.carbon_tax_rate, 4)

    # 4. 【唯一的一個 if 區塊】
    if page == "📊 即時能源監控":
        st.title("🏛️ 智慧化 ESG 能源監控平台")
        st.write(f"數據更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 電力排放係數: `{manager.carbon_factor}`")

        # 在這裡做數據統計
        total_p = df["即時功耗(kW)"].sum()
        total_c = df["碳排當量(kg)"].sum()
        floor_summary = df.groupby('樓層')[["即時功耗(kW)", "碳排當量(kg)"]].sum()
        device_summary = df.groupby('設備類型')["即時功耗(kW)"].sum().sort_values(ascending=False)

        # 在這裡顯示 KPI
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("全館總負載", f"{total_p:,.1f} kW")
        m2.metric("即時總碳排", f"{total_c:,.2f} kg/h")
        m3.metric("1F 區域負載", f"{floor_summary.loc['1F', '即時功耗(kW)']:,.1f} kW")
        m4.metric("4F 區域負載", f"{floor_summary.loc['4F', '即時功耗(kW)']:,.1f} kW")
        
        st.write("---")

        # --- 圖表區 ---
        left, right = st.columns([1, 1])
        with left:
            st.subheader("📊 1F vs 4F 負載佔比")
            fig_pie = go.Figure(data=[go.Pie(
                labels=floor_summary.index, 
                values=floor_summary["即時功耗(kW)"], 
                hole=.3,
                marker_colors=['#1E3A8A', "#9333EA"]
            )])
            st.plotly_chart(fig_pie, use_container_width=True)

        with right:
            st.subheader("⚡ 設備類型功耗統計 (kW)")
            fig_device = go.Figure(go.Bar(
                x=device_summary.index,
                y=device_summary.values,
                marker_color="#059669", 
                text=device_summary.values.round(1),
                textposition='auto',
            ))
            fig_device.update_layout(xaxis_title="設備種類", yaxis_title="總功耗 (kW)")
            st.plotly_chart(fig_device, use_container_width=True)

        st.write("---")
        st.subheader("📋 實時監測明細")
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("🔍 節能建議與場館控制策略"):
            max_device = device_summary.idxmax()
            max_device_pct = (device_summary.max() / total_p) * 100
            light_tax_saving = df[df['設備類型']=='燈光照明']['預估碳費(TWD)'].sum() * 0.5

            st.markdown(f"""
            1. **負載警示**：目前「**{max_device}**」佔總功耗最高（約 **{max_device_pct:.1f}%**），建議檢查 AHU 變頻器頻率。
            2. **離峰策略**：非展覽期間可將照明減半，預計每小時可節省碳費約 **{light_tax_saving:.2f} TWD**。
            3. **即時調控**：建議根據現場人員密度即時微調冷氣溫度，避免過度製冷，協助企業有效節省碳稅支出。
            """)
        
        if st.button("🔄 立即更新數據"):
            st.rerun()

    elif page == "💰 會計碳稅日結":
        # 切換到會計專用視窗
        st.title("💼 中小企業碳會計日結系統")
        st.info("會計人員請確認今日營運數據，系統將自動計算應計負載與碳成本。")
        
        accounting = SMB_CarbonAccounting()
        
        # 使用表單讓會計輸入
        with st.form("daily_form"):
            st.subheader("📝 今日營運實績錄入")
            col1, col2, col3 = st.columns(3)
            with col1:
                # 預設帶入監控系統的總電力，方便會計參考
                current_p_sum = df["即時功耗(kW)"].sum()
                elec = st.number_input("今日累計用電 (kWh)", value=float(current_p_sum))
            with col2:
                fuel = st.number_input("今日物流/燃油消耗 (L)", value=15.0)
            with col3:
                logistics = st.number_input("委外物流里程 (km)", value=50.0)
            
            submit = st.form_submit_button("執行日結核算")

        if submit:
            # 呼叫 finance.py 的計算邏輯
            report = accounting.generate_daily_report(elec, fuel, logistics)
            
            st.divider()
            st.subheader(f"📅 {report['日期']} 財務結算摘要")
            
            k1, k2, k3 = st.columns(3)
            k1.metric("應計碳費 (預留成本)", f"TWD {report['預估累計碳費(TWD)']}")
            k2.metric("潛在節稅空間", f"TWD {report['潛在節稅空間(TWD)']}", delta="優化空間")
            k3.metric("碳強度指標", report['碳強度(kg/TWD)'])

            # 顯示節稅錦囊
            st.warning(accounting.get_tax_reduction_advice(report['當日總碳排(t)']))
            
            # --- 這是給會計的核心功能：自動傳票建議 ---
            st.subheader("📒 建議會計分錄備註")
            st.code(f"""
                    
[一般日記簿傳票]
借：製造費用－環境成本 (碳費)  TWD {report['預估累計碳費(TWD)']}
    貸：應付帳款－應付碳費基金      TWD {report['預估累計碳費(TWD)']}
(摘要：依據當日營運碳排量 {report['當日總碳排(t)']}t 自動計提成本)
            """)

if __name__ == "__main__":
    main()