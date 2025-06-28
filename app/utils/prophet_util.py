import yfinance as yf
from prophet import Prophet
import pandas as pd

def convert_symbol(symbol: str, market: str) -> str:
    if market == 'KOSPI':
        return f"{symbol}.KS"
    elif market == 'KOSDAQ':
        return f"{symbol}.KQ"
    else:
        return symbol

def prophet_forecast(symbol, market):
    yf_symbol = convert_symbol(symbol, market)
    # KOSPI는 10년치, 그 외는 5년치
    period = '10y' if market == 'KOSPI' else '5y'
    ticker = yf.Ticker(yf_symbol)
    df = ticker.history(period=period).reset_index()
    if df.empty:
        return [], "데이터 없음"
    df = df.rename(columns={'Date': 'ds', 'Close': 'y'})
    if market == 'KOSPI' and 'Volume' in df.columns:
        model = Prophet()
        model.add_regressor('Volume')
        model.fit(df[['ds', 'y', 'Volume']])
        future = model.make_future_dataframe(periods=30)
        # 미래 거래량은 최근 30일 평균으로 채움
        avg_volume = df['Volume'].tail(30).mean()
        future = future.merge(df[['ds', 'Volume']], on='ds', how='left')
        future['Volume'] = future['Volume'].fillna(avg_volume)
        forecast = model.predict(future)
    else:
        model = Prophet()
        model.fit(df[['ds', 'y']])
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
    result = [
        {"date": str(row['ds'].date()), "price": float(row['yhat'])}
        for _, row in forecast.tail(30).iterrows()
    ]
    summary = f"향후 30일간 예측: 최저 {min(r['price'] for r in result):,.2f}, 최고 {max(r['price'] for r in result):,.2f}"
    return result, summary
