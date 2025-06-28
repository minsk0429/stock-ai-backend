import yfinance as yf

def convert_symbol(symbol: str, market: str) -> str:
    if market == 'KOSPI':
        return f"{symbol}.KS"
    elif market == 'KOSDAQ':
        return f"{symbol}.KQ"
    else:
        return symbol

async def get_latest_price(symbol: str, market: str):
    yf_symbol = convert_symbol(symbol, market)
    ticker = yf.Ticker(yf_symbol)
    hist = ticker.history(period='5d')
    if hist.empty:
        return None
    last = hist.iloc[-1]
    return {
        "symbol": symbol,
        "market": market,
        "close": float(last["Close"]),
        "date": str(last.name.date())
    }
