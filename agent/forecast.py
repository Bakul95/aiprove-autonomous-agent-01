"""Prediction strategies — small, documented, deterministic heuristics.

These are deliberately simple and honest about what they are: a momentum
continuation rule for direction calls and a mean-reversion rule for close
prices. No strategy claims an edge; every prediction ships with the modest
confidence the rule earns (0.55-0.65), never a fabricated 0.9.
"""
from . import market


def _confidence(change_pct):
    """0.55 base, +0.01 per point of move, capped at 0.65."""
    return round(min(0.55 + abs(change_pct) * 0.01, 0.65), 2)


def direction_call(change_pct):
    """Yes/no: will the asset close higher? Momentum continuation."""
    answer = "yes" if change_pct >= 0 else "no"
    return answer, _confidence(change_pct)


def side_call(change_pct):
    """Long/short for the next 24h. Momentum continuation."""
    return ("long" if change_pct >= 0 else "short"), _confidence(change_pct)


def close_call(closes):
    """Tomorrow's close: last price pulled 25% toward the recent mean."""
    mean = sum(closes) / len(closes)
    last = closes[-1]
    return round(last + 0.25 * (mean - last), 2), 0.58


def predict(slug):
    """Compute (answer, confidence) for a forecast bounty slug.

    Returns None when the market data needed is unavailable — the caller
    then skips the bounty instead of guessing.
    """
    if slug in ("btc-tomorrow", "forecast-eth-24h"):
        coin = "bitcoin" if slug == "btc-tomorrow" else "ethereum"
        data = market.coingecko_24h([coin])
        if data is None:
            return None
        _, change = data[coin]
        return direction_call(change)
    if slug == "forecast-btc-7d":
        res = market.coingecko_change_7d("bitcoin")
        if res is None:
            return None
        change, _ = res
        return direction_call(change)
    if slug == "signal-eth-pnl-24h":
        data = market.coingecko_24h(["ethereum"])
        if data is None:
            return None
        _, change = data["ethereum"]
        return side_call(change)
    if slug in ("forecast-gold-tomorrow", "spy-close-1dollar", "forecast-nvda-3d"):
        symbol = {"forecast-gold-tomorrow": "GLD",
                  "spy-close-1dollar": "SPY",
                  "forecast-nvda-3d": "NVDA"}[slug]
        res = market.yahoo_closes(symbol)
        if res is None:
            return None
        closes, _ = res
        return close_call(closes)
    return None
