import yfinance as yf

symbol = "005930.KS"  # 삼성전자 KOSPI

ticker = yf.Ticker(symbol)
hist = ticker.history(period='5d')
print(hist)
print("empty:", hist.empty)
