from app.utils.prophet_util import prophet_forecast

async def get_ai_forecast(symbol: str, market: str):
    forecast, summary = prophet_forecast(symbol, market)
    return {
        "forecast": forecast,  # [{date, price}, ...]
        "summary": summary
    }
