"""FINRA暗池数据"""
import requests, json, sys
from datetime import datetime

BASE = "https://otctransparency.finra.org/otctransparency"

def fetch(tickers, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y%m%d")
    url = BASE + "/download?date=" + date_str
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        return {"error": "FINRA " + str(r.status_code), "date": date_str}
    lines = r.text.splitlines()
    results = {}
    for ticker in tickers:
        t = ticker.upper()
        matches = [l for l in lines if t in l]
        results[t] = {"matches": len(matches), "sample": matches[:3]}
    return {
        "date": date_str,
        "total_lines": len(lines),
        "first_3_lines": lines[:3],
        "data": results
    }

if __name__ == "__main__":
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL","NVDA","AVGO","MRVL"]
    print(json.dumps(fetch(tickers), indent=2, ensure_ascii=False))
