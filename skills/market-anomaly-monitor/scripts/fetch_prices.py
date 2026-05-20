"""
市场价格采集脚本 v2 — 零依赖，纯 Python 内置库
数据源:
  - 美股/ETF/加密: Nasdaq 官方 API (api.nasdaq.com)
  - 港股/恒指:    新浪财经 API (hq.sinajs.cn)
  - 韩股/KOSPI:   Naver Finance API (m.stock.naver.com)

异动判断升级为三层机制：
  L1 绝对阈值   — 单日涨跌幅超过固定阈值（粗筛，快速）
  L2 相对偏离值 — 个股/板块涨跌幅 vs 基准指数的偏离（精筛，去噪）
  L3 综合评级   — 综合 L1/L2 给出 STRONG / MODERATE / WATCH 三级

用法: python3 fetch_prices.py [--json-only]
  --json-only  只输出 JSON，不输出人类可读摘要（供 Automation 调用）
"""

import sys, json, urllib.request, urllib.error
from datetime import datetime

# ── 监控标的配置 ──────────────────────────────────────────────
# Nasdaq: (symbol, 显示名, category, assetclass, L1绝对阈值%)
NASDAQ_WATCHLIST = [
    ("SPY",  "标普500 ETF",     "us_index", "etf",    2.0),
    ("QQQ",  "纳斯达克100 ETF", "us_index", "etf",    2.0),
    ("UVXY", "VIX恐慌(2x ETF)", "vix",      "etf",   15.0),
    ("GLD",  "黄金 ETF",        "macro",    "etf",    3.0),
    ("USO",  "原油 ETF",        "macro",    "etf",    3.0),
    ("UUP",  "美元指数 ETF",    "macro",    "etf",    1.5),
    ("BTC",  "比特币",          "crypto",   "crypto", 5.0),
]

# 新浪港股: (sina_symbol, 显示名, category, L1阈值%)
SINA_HK_WATCHLIST = [
    ("hkHSI",  "恒生指数",   "hk_index", 2.0),
    ("hk09988","阿里巴巴-W", "hk_stock", 5.0),
    ("hk00700","腾讯控股",   "hk_stock", 5.0),
]

# Naver 韩股: (code, 显示名, category, L1阈值%, is_index)
NAVER_KR_WATCHLIST = [
    ("KOSPI",  "韩国综合指数", "kr_index", 2.0,  True),
    ("000660", "SK海力士",     "kr_stock", 5.0,  False),
    ("005930", "三星电子",     "kr_stock", 5.0,  False),
]

# ── 基准指数映射（用于计算相对偏离值）────────────────────────
# 个股/板块 → 对应基准指数 symbol
BENCHMARK_MAP = {
    "us_index": None,    # 指数本身不做相对偏离
    "vix":      None,
    "macro":    None,
    "crypto":   None,
    "hk_index": None,
    "kr_index": None,
    "hk_stock": "hkHSI",   # 港股个股 vs 恒生指数
    "kr_stock": "KOSPI",   # 韩股个股 vs KOSPI
}

# ── 相对偏离值阈值（个股涨跌幅 - 基准指数涨跌幅）────────────
RELATIVE_THRESHOLD = {
    "hk_stock": 4.0,   # 港股个股偏离恒指 ≥ ±4%
    "kr_stock": 4.0,   # 韩股个股偏离KOSPI ≥ ±4%
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}

def http_get(url, extra_headers=None, timeout=10, encoding="utf-8"):
    headers = {**HEADERS, **(extra_headers or {})}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode(encoding, errors="replace")
    except Exception as e:
        return None

# ── 各数据源 fetch ────────────────────────────────────────────
def fetch_nasdaq(symbol, assetclass):
    url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass={assetclass}"
    raw = http_get(url)
    if not raw:
        return {"error": "request failed"}
    try:
        d = json.loads(raw.strip())
        pd = (d.get("data") or {}).get("primaryData") or {}
        if not pd.get("lastSalePrice"):
            return {"error": "no price data"}
        price = float(pd["lastSalePrice"].replace("$","").replace(",","").strip())
        pct   = float(pd["percentageChange"].replace("%","").replace("+","").strip())
        return {"price": price, "change_pct": pct}
    except Exception as e:
        return {"error": str(e)}

def fetch_sina_hk_batch(sina_symbols):
    symbols_str = ",".join(sina_symbols)
    url = f"https://hq.sinajs.cn/list={symbols_str}"
    raw = http_get(url, extra_headers={"Referer": "https://finance.sina.com.cn/"}, encoding="gb18030")
    if not raw:
        return {s: {"error": "request failed"} for s in sina_symbols}
    results = {}
    for line in raw.split(";"):
        line = line.strip()
        if not line or '"' not in line:
            continue
        try:
            sym_part = line.split("=")[0].split("_")[-1]
            val = line.split('"')[1]
            if not val:
                results[sym_part] = {"error": "empty (market closed?)"}
                continue
            fields = val.split(",")
            # 字段: name, cn_name, prev_close, open, high, low, price, change_abs, change_pct
            results[sym_part] = {
                "price":      float(fields[6]),
                "prev_close": float(fields[2]),
                "change_pct": float(fields[8]),
            }
        except Exception as e:
            sym_part = line.split("=")[0].split("_")[-1] if "=" in line else "unknown"
            results[sym_part] = {"error": str(e)}
    for s in sina_symbols:
        if s not in results:
            results[s] = {"error": "not in response"}
    return results

def fetch_naver_kr(code, is_index):
    url = (f"https://m.stock.naver.com/api/index/{code}/basic" if is_index
           else f"https://m.stock.naver.com/api/stock/{code}/basic")
    raw = http_get(url)
    if not raw:
        return {"error": "request failed"}
    try:
        d = json.loads(raw.strip())
        price   = float(d.get("closePrice","0").replace(",",""))
        pct_abs = float(d.get("fluctuationsRatio","0"))
        compare = float(d.get("compareToPreviousClosePrice","0").replace(",",""))
        sign    = -1 if compare < 0 else 1
        return {"price": price, "change_pct": round(sign * pct_abs, 2)}
    except Exception as e:
        return {"error": str(e)}

# ── 异动评级（三层）──────────────────────────────────────────
def grade_anomaly(symbol, category, change_pct, l1_threshold, benchmark_pct):
    """
    返回 (level, reason)
    level: "STRONG" | "MODERATE" | "WATCH" | None
    """
    abs_chg = abs(change_pct)
    l1_hit  = abs_chg >= l1_threshold

    # 相对偏离值（仅对有基准的个股计算）
    rel_threshold = RELATIVE_THRESHOLD.get(category)
    rel_deviation = None
    l2_hit = False
    if benchmark_pct is not None and rel_threshold is not None:
        rel_deviation = round(change_pct - benchmark_pct, 2)
        l2_hit = abs(rel_deviation) >= rel_threshold

    # 评级逻辑
    if l1_hit and l2_hit:
        reason = f"绝对涨跌 {change_pct:+.2f}%（阈值±{l1_threshold}%），相对基准偏离 {rel_deviation:+.2f}%（阈值±{rel_threshold}%）"
        return "STRONG", reason
    elif l1_hit:
        reason = f"绝对涨跌 {change_pct:+.2f}%（阈值±{l1_threshold}%）"
        if rel_deviation is not None:
            reason += f"，相对基准偏离 {rel_deviation:+.2f}%（未超阈值，可能是板块联动）"
        return "MODERATE", reason
    elif l2_hit:
        reason = f"相对基准偏离 {rel_deviation:+.2f}%（阈值±{rel_threshold}%），绝对涨跌 {change_pct:+.2f}% 未超阈值"
        return "WATCH", reason
    else:
        return None, None

def make_result(symbol, name, category, threshold, data, benchmark_pct=None):
    if "error" in data:
        return {"symbol": symbol, "name": name, "category": category,
                "price": None, "change_pct": None, "threshold": threshold,
                "anomaly_level": None, "anomaly_reason": None, "error": data["error"]}
    pct = data["change_pct"]
    level, reason = grade_anomaly(symbol, category, pct, threshold, benchmark_pct)
    return {
        "symbol":        symbol,
        "name":          name,
        "category":      category,
        "price":         data["price"],
        "change_pct":    round(pct, 2),
        "threshold":     threshold,
        "anomaly_level": level,    # STRONG / MODERATE / WATCH / None
        "anomaly_reason": reason,
        "error":         None,
    }

def main():
    json_only = "--json-only" in sys.argv
    results = []

    # 1. Nasdaq
    for symbol, name, category, assetclass, threshold in NASDAQ_WATCHLIST:
        data = fetch_nasdaq(symbol, assetclass)
        results.append(make_result(symbol, name, category, threshold, data))

    # 2. 新浪港股（批量）
    sina_symbols = [s for s, *_ in SINA_HK_WATCHLIST]
    sina_data = fetch_sina_hk_batch(sina_symbols)
    # 先拿恒指作为港股个股的基准
    hsi_pct = sina_data.get("hkHSI", {}).get("change_pct")
    for sina_sym, name, category, threshold in SINA_HK_WATCHLIST:
        benchmark = hsi_pct if category == "hk_stock" else None
        results.append(make_result(sina_sym, name, category, threshold,
                                   sina_data.get(sina_sym, {"error": "missing"}), benchmark))

    # 3. Naver 韩股
    # 先拿 KOSPI 作为韩股个股的基准
    kospi_data = fetch_naver_kr("KOSPI", True)
    kospi_pct  = kospi_data.get("change_pct") if "error" not in kospi_data else None
    results.append(make_result("KOSPI", "韩国综合指数", "kr_index", 2.0, kospi_data))
    for code, name, category, threshold, is_index in NAVER_KR_WATCHLIST:
        if is_index:
            continue  # KOSPI 已加入
        data = fetch_naver_kr(code, False)
        benchmark = kospi_pct if category == "kr_stock" else None
        results.append(make_result(code, name, category, threshold, data, benchmark))

    # ── 汇总 ──────────────────────────────────────────────────
    strong   = [r for r in results if r.get("anomaly_level") == "STRONG"]
    moderate = [r for r in results if r.get("anomaly_level") == "MODERATE"]
    watch    = [r for r in results if r.get("anomaly_level") == "WATCH"]
    errors   = [r for r in results if r.get("error")]

    output = {
        "timestamp":       datetime.now().isoformat(),
        "results":         results,
        "anomalies": {
            "STRONG":   strong,    # 绝对+相对双触发，需立即归因
            "MODERATE": moderate,  # 仅绝对阈值触发，可能是板块联动
            "WATCH":    watch,     # 仅相对偏离触发，值得关注
        },
        "has_anomaly":     len(strong) > 0 or len(moderate) > 0,
        "needs_attention": len(watch) > 0,
        "errors":          errors,
    }

    if json_only:
        print(json.dumps(output, ensure_ascii=False))
        return

    # ── 人类可读摘要 ──────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f"📊 市场异动监控  {output['timestamp'][:16]}")
    print(f"{'='*50}")

    if not strong and not moderate and not watch:
        print("✅ 全市场平稳，无异动信号")
    else:
        if strong:
            print(f"\n🚨 STRONG 异动（{len(strong)}个）— 需立即归因分析：")
            for r in strong:
                print(f"  {r['name']} ({r['symbol']})  {r['change_pct']:+.2f}%  ${r['price']}")
                print(f"    → {r['anomaly_reason']}")
        if moderate:
            print(f"\n⚠️  MODERATE 异动（{len(moderate)}个）— 绝对阈值触发：")
            for r in moderate:
                print(f"  {r['name']} ({r['symbol']})  {r['change_pct']:+.2f}%  ${r['price']}")
                print(f"    → {r['anomaly_reason']}")
        if watch:
            print(f"\n👀 WATCH 信号（{len(watch)}个）— 相对偏离值触发：")
            for r in watch:
                print(f"  {r['name']} ({r['symbol']})  {r['change_pct']:+.2f}%")
                print(f"    → {r['anomaly_reason']}")

    print(f"\n{'─'*50}")
    print("📈 全市场概览：")
    for r in results:
        if r.get("error"):
            print(f"  {r['name']:12s}  ERR")
        else:
            flag = {"STRONG":"🚨","MODERATE":"⚠️ ","WATCH":"👀","":""}.get(r.get("anomaly_level") or "", "  ")
            print(f"  {flag} {r['name']:12s}  {r['change_pct']:+.2f}%")

    if errors:
        print(f"\n❌ 获取失败（{len(errors)}个）：{', '.join(r['symbol'] for r in errors)}")
    print()

if __name__ == "__main__":
    main()
