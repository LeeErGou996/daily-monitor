import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import json

# 你的核心资产池
CORE_PAIRS = {
    'VUAA.DE': {'name': '标普500 (VUAA)'},
    'XNAS.DE': {'name': '纳指100 (XNAS)'},
    'VGWE.DE': {'name': '全球高息 (VGWE)'}
}

INCEPTION_DATE = "2026-01-01"

def fetch_data():
    print(f"🚀 开始抓取最新行情，并全量更新自 {INCEPTION_DATE} 以来的历史走势...")
    tickers_str = " ".join(CORE_PAIRS.keys())

    try:
        # 1. 抓取最新快照
        # 【关键改动】：加入 repair=True，让 yfinance 在底层自动修复异常/丢失的 K 线数据
        data = yf.download(tickers_str, period="1mo", progress=False, threads=True, auto_adjust=False, repair=True)
        adj_close_prices = data['Adj Close']

    except Exception as e:
        print(f"❌ 抓取快照失败: {e}")
        return

    # ================= 1. 生成 data.json (实时看板) =================
    results = []
    for ticker, info in CORE_PAIRS.items():
        try:
            series = adj_close_prices[ticker].dropna()
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
            print(f"⚠️ 处理快照 {ticker} 时出错: {e}")

    tz_berlin = pytz.timezone('Europe/Berlin')
    update_time = datetime.now(tz_berlin).strftime('%Y-%m-%d %H:%M:%S')

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"timestamp": update_time, "data": results}, f, ensure_ascii=False, indent=4)

    # ================= 2. 全量更新 history.json (无限延伸的折线图) =================
    print(f"📈 全量拉取自 {INCEPTION_DATE} 以来的历史复权数据 (已开启自动修复)...")
    try:
        # 【关键改动】：历史数据同步开启 repair=True
        hist_data = yf.download(tickers_str, start=INCEPTION_DATE, progress=False, threads=True, auto_adjust=False, repair=True)
        
        if hist_data.empty:
            print("ℹ️ 没有获取到历史数据。")
        else:
            # 拿到已修复好的复权数据
            hist_adj_close = hist_data["Adj Close"]
            history_list = []
            
            for date, row in hist_adj_close.iterrows():
                day_data = {"date": date.strftime('%Y-%m-%d')}
                for ticker in CORE_PAIRS.keys():
                    val = row[ticker]
                    # 依然保留 pd.notna 兜底，防止某些极端情况依然返回 NaN
                    day_data[ticker] = round(float(val), 2) if pd.notna(val) else None
                history_list.append(day_data)

            # 覆盖写入
            with open('history.json', 'w', encoding='utf-8') as f:
                json.dump(history_list, f, ensure_ascii=False, indent=4)
                
    except Exception as e:
        print(f"⚠️ 拉取历史数据时出错: {e}")

    print(f"✅ 数据已成功写入！(基准日: {INCEPTION_DATE} -> 更新时间: {update_time})")

if __name__ == "__main__":
    fetch_data()