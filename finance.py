import pandas as pd
from datetime import datetime

class SMB_CarbonAccounting:
    # SMB, Small and Medium-sized Businesses

    def __init__(self):

        self.carbon_tax_rate = 300  # TWD/公噸
        self.avg_electricity_price = 5.0  # TWD/度
        
    def generate_daily_report(self, electricity_kwh, fuel_liters, logistics_km):
        """
        會計日結功能：輸入當日各項數據，產生財務影響分析
        """
        # 1. 碳排計算 (依據常見係數)
        elec_carbon = electricity_kwh * 0.424  # 電力 (kg)
        fuel_carbon = fuel_liters * 2.66      # 柴油/燃油 (kg)
        logistics_carbon = logistics_km * 0.2  # 物流運送 (kg)
        
        total_carbon_kg = elec_carbon + fuel_carbon + logistics_carbon
        total_carbon_tons = total_carbon_kg / 1000
        
        carbon_fee = total_carbon_tons * self.carbon_tax_rate
        energy_cost = electricity_kwh * self.avg_electricity_price
        
        # 節稅與獲利評估 (中小企業最在意的)
        # 假設轉用綠電或節能設備能減少 15% 碳費
        potential_savings = carbon_fee * 0.15
        
        return {
            "日期": datetime.now().strftime("%Y-%m-%d"),
            "當日總碳排(t)": round(total_carbon_tons, 4),
            "預估累計碳費(TWD)": round(carbon_fee, 2),
            "能源現金支出(TWD)": round(energy_cost, 2),
            "潛在節稅空間(TWD)": round(potential_savings, 2),
            "碳強度(kg/TWD)": round(total_carbon_kg / (energy_cost + 1), 3) # 每花1元產生的碳
        }

    def get_tax_reduction_advice(self, carbon_tons):
        """
        針對中小企業提供的「節稅錦囊」
        """
        if carbon_tons > 1.0:
            return "⚠️ 碳排超標：建議檢查老舊空調，更換為一級能效設備可申請政府 30% 補助。"
        elif carbon_tons > 0.5:
            return "💡 節稅提醒：目前碳費壓力中等，建議導入再生能源憑證 (REC) 抵銷支出。"
        else:
            return "✅ 表現優異：當前碳強度低於產業平均，可考慮申請 ESG 低利貸款。"