import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import json
import os

# 你的核心资产池
CORE_PAIRS = {
    'VUAA.DE': {'name': '标普500 (VUAA)'},
    'XNAS.DE': {'name': '纳指100 (XNAS)'},
    'VGWE.DE': {'name': '全球高息 (VGWE)'}
}


def fetch_data():
    print("🚀 开始抓取最新行情...")
    tickers_str = " ".join(CORE_PAIRS.keys())

    try:
        data = yf.download(tickers_str, period="5d", progress=False, threads=True)
        close_prices = data['Close']
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return

    results = []

    for ticker, info in CORE_PAIRS.items():
        try:
            series = close_prices[ticker].dropna()
            if len(series) >= 2:
                curr = float(series.iloc[-1])
                prev = float(series.iloc[-2])
                pct = ((curr - prev) / prev) * 100
                amt = curr - prev

                results.append({
                    "ticker": ticker,
                    "name": info['name'],
                    "price": round(curr, 2),
                    "change_pct": round(pct, 2),
                    "change_amt": round(amt, 2)
                })
        except Exception as e:
            print(f"⚠️ 处理 {ticker} 时出错: {e}")

    # 获取当前慕尼黑时间
    tz_berlin = pytz.timezone('Europe/Berlin')
    update_time = datetime.now(tz_berlin).strftime('%Y-%m-%d %H:%M:%S')

    # 打包成 JSON 字典
    output_data = {
        "timestamp": update_time,
        "data": results
    }

    # 将数据写入本地 data.json 文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"✅ 数据已成功写入 data.json！(更新时间: {update_time})")


if __name__ == "__main__":
    fetch_data()
