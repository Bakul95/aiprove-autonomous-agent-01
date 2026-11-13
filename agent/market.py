"""Public market data, no API keys.

Crypto: CoinGecko public API (free, no key).
Stocks/ETFs: Yahoo Finance chart API (free, no key).

Binance and Stooq are NOT used: Binance is geo-blocked from this sandbox
and Stooq sits behind a JS challenge wall. If a source fails, the caller
gets None and the bounty is skipped — the agent never guesses blind.
"""
import json

from .client import curl_text

CG = "https://api.coingecko.com/api/v3"
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart"


def coingecko_24h(coin_ids):
    """{coin_id: (price_usd, change_24h_pct)} or None on failure."""
    ids = ",".join(coin_ids)
    url = (f"{CG}/simple/price?ids={ids}&vs_currencies=usd"
           f"&include_24hr_change=true")
    status, text = curl_text(url)
    if status != 200:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    out = {}
    for cid in coin_ids:
        row = data.get(cid)
        if not row or "usd" not in row or "usd_24h_change" not in row:
            return None
        out[cid] = (row["usd"], row["usd_24h_change"])
    return out


def coingecko_change_7d(coin_id):
    """7-day percent change from the market_chart endpoint, or None."""
    url = f"{CG}/coins/{coin_id}/market_chart?vs_currency=usd&days=7"
    status, text = curl_text(url)
    if status != 200:
        return None
    try:
        prices = json.loads(text)["prices"]
    except (ValueError, KeyError):
        return None
    if len(prices) < 2:
        return None
    first, last = prices[0][1], prices[-1][1]
    if not first:
        return None
    return (last - first) / first * 100.0, last


def yahoo_closes(symbol, days="5d"):
    """(closes, last_price) for a stock/ETF symbol, or None on failure."""
    status, text = curl_text(f"{YAHOO}/{symbol}?range={days}&interval=1d")
    if status != 200:
        return None
    try:
        result = json.loads(text)["chart"]["result"][0]
        closes = [c for c in result["indicators"]["quote"][0]["close"]
                  if c is not None]
        last = result["meta"]["regularMarketPrice"]
    except (ValueError, KeyError, IndexError, TypeError):
        return None
    if len(closes) < 2 or not last:
        return None
    return closes, last
