import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
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
    print(f"🚀 开始抓取最新行情，并增量更新自 {INCEPTION_DATE} 以来的历史走势...")
    tickers_str = " ".join(CORE_PAIRS.keys())

    try:
        # 1. 抓取最新快照（用于顶部实时看板）
        data = yf.download(tickers_str, period="5d", progress=False, threads=True)
        close_prices = data['Close']

    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return

    # ================= 1. 生成 data.json (实时看板) =================
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
            print(f"⚠️ 处理快照 {ticker} 时出错: {e}")

    tz_berlin = pytz.timezone('Europe/Berlin')
    update_time = datetime.now(tz_berlin).strftime('%Y-%m-%d %H:%M:%S')

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"timestamp": update_time, "data": results}, f, ensure_ascii=False, indent=4)

    # ================= 2. 增量更新 history.json (无限延伸的折线图) =================
    try:
        with open('history.json', 'r', encoding='utf-8') as f:
            existing_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_history = []

    # 计算本地已有的最后日期
    if existing_history:
        last_date_str = existing_history[-1].get("date", INCEPTION_DATE)
    else:
        last_date_str = INCEPTION_DATE

    try:
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
    except ValueError:
        last_date = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()

    start_date = last_date + timedelta(days=1)
    today_utc = datetime.utcnow().date()

    # 如果已经追平到今天，则无需再拉增量
    if start_date > today_utc:
        history_list = existing_history
    else:
        print(f"📈 从 {start_date} 开始增量拉取历史数据...")
        try:
            # yfinance 的 start 为包含式区间，指定 start 不指定 end 默认到今天
            hist_data = yf.download(tickers_str, start=start_date.strftime("%Y-%m-%d"), progress=False, threads=True)
            if hist_data.empty:
                print("ℹ️ 没有新的历史数据需要追加。")
                history_list = existing_history
            else:
                hist_close = hist_data["Close"]
                new_history = []
                for date, row in hist_close.iterrows():
                    day_data = {"date": date.strftime('%Y-%m-%d')}
                    for ticker in CORE_PAIRS.keys():
                        val = row[ticker]
                        day_data[ticker] = round(float(val), 2) if pd.notna(val) else None
                    new_history.append(day_data)

                history_list = existing_history + new_history
        except Exception as e:
            print(f"⚠️ 增量拉取历史数据时出错: {e}")
            history_list = existing_history

    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history_list, f, ensure_ascii=False, indent=4)

    print(f"✅ 数据已成功写入！(基准日: {INCEPTION_DATE} -> 更新时间: {update_time})")


if __name__ == "__main__":
    fetch_data()

