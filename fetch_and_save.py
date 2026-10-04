import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import json

# 你的核心资产池
CORE_PAIRS = {
    'VUAA.DE': {'name': '标普500 (VUAA)'},
    'XNAS.DE': {'name': '纳指100 (XNAS)'},
    'SEC0.DE': {'name': '全球半导体 (SEC0)'},
    'VGWE.DE': {'name': '全球高息 (VGWE)'}
}

INCEPTION_DATE = "2026-01-01"

def fetch_data():
    print(f"🚀 开始抓取最新行情，并增量更新自 {INCEPTION_DATE} 以来的历史走势...")
    tickers_str = " ".join(CORE_PAIRS.keys())

    try:
        # 1. 抓取最新快照（用于顶部实时看板）
        data = yf.download(tickers_str, period="1mo", progress=False, threads=True)
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

    # ================= 2. 更新 history.json =================
    try:
        with open('history.json', 'r', encoding='utf-8') as f:
            existing_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_history = []

    # 新增资产时，旧 history.json 没有对应字段。此时从基准日完整回填一次；
    # 正常情况下仍只做增量更新，避免每次重复下载全部历史。
    missing_tickers = [
        ticker for ticker in CORE_PAIRS
        if existing_history and not any(item.get(ticker) is not None for item in existing_history)
    ]
    needs_full_backfill = bool(missing_tickers)

    if needs_full_backfill:
        print(f"🔄 检测到新增资产 {missing_tickers}，从 {INCEPTION_DATE} 重新回填完整历史...")
        start_date = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()
    elif existing_history:
        last_date_str = existing_history[-1].get("date", INCEPTION_DATE)
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        except ValueError:
            last_date = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()
        start_date = last_date + timedelta(days=1)
    else:
        start_date = datetime.strptime(INCEPTION_DATE, "%Y-%m-%d").date()

    today_utc = datetime.utcnow().date()

    if start_date > today_utc and not needs_full_backfill:
        history_list = existing_history
    else:
        mode = "完整回填" if needs_full_backfill or not existing_history else "增量拉取"
        print(f"📈 从 {start_date} 开始{mode}历史数据...")
        try:
            hist_data = yf.download(
                tickers_str,
                start=start_date.strftime("%Y-%m-%d"),
                progress=False,
                threads=True
            )
            if hist_data.empty:
                print("ℹ️ 没有新的历史数据需要写入。")
                history_list = existing_history
            else:
                hist_close = hist_data["Close"]
                unavailable_tickers = [
                    ticker for ticker in CORE_PAIRS
                    if ticker not in hist_close.columns or hist_close[ticker].dropna().empty
                ]
                if unavailable_tickers:
                    raise RuntimeError(f"缺少有效历史价格: {unavailable_tickers}")

                downloaded_history = []
                for date, row in hist_close.iterrows():
                    day_data = {"date": date.strftime('%Y-%m-%d')}
                    for ticker in CORE_PAIRS.keys():
                        val = row[ticker]
                        day_data[ticker] = round(float(val), 2) if pd.notna(val) else None
                    downloaded_history.append(day_data)

                history_list = downloaded_history if needs_full_backfill or not existing_history else existing_history + downloaded_history
        except Exception as e:
            print(f"⚠️ 历史数据更新失败: {e}")
            history_list = existing_history

    # 去重并统一按日期排序
    unique_history = {}
    for item in history_list:
        unique_history[item["date"]] = item
    history_list = sorted(unique_history.values(), key=lambda x: x["date"])

    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history_list, f, ensure_ascii=False, indent=4)

    print(f"✅ 数据已成功写入！(基准日: {INCEPTION_DATE} -> 更新时间: {update_time})")

if __name__ == "__main__":
    fetch_data()