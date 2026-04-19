import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

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
    st.set_page_config(page_title="Jamiecompany活動空間監控", layout="wide")
    
    manager = JamiecompanyESGManager()
    # 這裡抓取數據，df 就被定義了
    df = manager.fetch_live_signals()
    
    # 標題設定
    st.title("🏛️ 智慧化 ESG 能源監控平台：以 Jamiecompany 為例")
    st.write(f"數據更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 電力排放係數: `{manager.carbon_factor}`")

    # --- 數據統計計算 ---
    total_p = df["即時功耗(kW)"].sum()
    total_c = df["碳排當量(kg)"].sum()
    floor_summary = df.groupby('樓層')[["即時功耗(kW)", "碳排當量(kg)"]].sum()
    device_summary = df.groupby('設備類型')["即時功耗(kW)"].sum().sort_values(ascending=False)

    # --- KPI 顯示 ---
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

    # --- 節能建議區塊 (解決 df 未定義與建議顯示問題) ---
    with st.expander("🔍 節能建議與場館控制策略"):
        # 計算最高耗電百分比
        max_device = device_summary.idxmax()
        max_device_pct = (device_summary.max() / total_p) * 100
        # 計算燈光節能潛力
        light_tax_saving = df[df['設備類型']=='燈光照明']['預估碳費(TWD)'].sum() * 0.5

        st.markdown(f"""
        1. **負載警示**：目前「**{max_device}**」佔總功耗最高（約 **{max_device_pct:.1f}%**），建議檢查 AHU 變頻器頻率。
        2. **離峰策略**：非展覽期間可將照明減半，預計每小時可節省碳費約 **{light_tax_saving:.2f} TWD**。
        3. **即時調控**：南港展覽館場地大，建議根據現場人員密度即時手動微調冷氣溫度，避免過度製冷。
        """)

    st.write("---")
    
    # --- 頁尾手動更新按鈕 ---
    ft_col1, ft_col2 = st.columns([4, 1])
    with ft_col1:
        st.caption(f"💡 系統目前為模擬實時數據。最後同步時間：{datetime.now().strftime('%H:%M:%S')}")
    with ft_col2:
        if st.button("🔄 立即更新數據"):
            st.rerun()

if __name__ == "__main__":
    main()