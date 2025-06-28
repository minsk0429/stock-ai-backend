from fastapi import APIRouter, HTTPException, Query
from app.services.ai_service import get_ai_forecast

router = APIRouter()

@router.get("/ai")
async def ai(symbol: str = Query(...), market: str = Query(...)):
    result = await get_ai_forecast(symbol, market)
    if result is None:
        raise HTTPException(status_code=404, detail="No forecast")
    return result
