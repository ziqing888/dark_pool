"""FINRA 暗池数据 — GitHub Actions 日更（美国IP免墙）"""
import requests, json, os, sys
from datetime import datetime

# FINRA OTC 公开数据下载
FINRA_BASE = "https://cdn.finra.org/equity/otcmarket/traded"

def fetch(tickers, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y%m%d")
    
    url = f"{FINRA_BASE}/CNMSdarkpool{date_str}.txt"
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        # 尝试前一天（周末没人交易）
        return {"error": f"FINRA {r.status_code}", "date": date_str}
    
    lines = r.text.strip().split("\n")
    results = {}
    
    for ticker in tickers:
        ticker = ticker.upper()
        matches = [l for l in lines if l.startswith(f"{ticker}|")]
        if not matches:
            results[ticker] = {"trades": 0, "volume": 0}
            continue
        
        total_vol = 0
        for l in matches:
            parts = l.split("|")
            if len(parts) >= 4:
                total_vol += int(parts[3])  # share quantity
        
        results[ticker] = {"trades": len(matches), "volume": total_vol}
    
    return {"date": date_str, "data": results}

if __name__ == "__main__":
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL","NVDA","AVGO","MRVL"]
    result = fetch(tickers)
    print(json.dumps(result, indent=2, ensure_ascii=False))
