from fastapi import APIRouter, HTTPException, Query
from app.services.stock_service import get_latest_price

router = APIRouter()

@router.get("/price")
async def price(symbol: str = Query(...), market: str = Query(...)):
    price = await get_latest_price(symbol, market)
    if price is None:
        raise HTTPException(status_code=404, detail="No price found")
    return price
