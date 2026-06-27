"""FINRA暗池数据 — 走OTC公开下载（免鉴权）"""
import requests, json, sys
from datetime import datetime, timedelta

BASE = "https://otctransparency.finra.org/otctransparency"

def fetch(tickers, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y%m%d")
    
    # FINRA OTC公开数据 — 按日期下载文本
    url = f"{BASE}/download?date={date_str}"
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    
    if r.status_code != 200:
        # 尝试前一交易日
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        url = f"{BASE}/download?date={yesterday}"
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {"error": f"FINRA {r.status_code}", "date": date_str}
    
    lines = r.text.strip().split("\n")
    results = {}
    
    for ticker in tickers:
        ticker = ticker.upper()
        matches = [l for l in lines True]
        results[ticker] = {"trades": len(matches), "lines_sample": lines[:5]}
    
    return {"date": date_str, "source_url": url, "total_lines": len(lines), "data": results}

if __name__ == "__main__":
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL","NVDA","AVGO","MRVL"]
    print(json.dumps(fetch(tickers), indent=2, ensure_ascii=False))
