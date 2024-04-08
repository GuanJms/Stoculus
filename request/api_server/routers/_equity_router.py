from fastapi import APIRouter
import asyncio
from colorama import Fore, Back
from datetime import datetime

equity_router = APIRouter(
    prefix="/equity",
    tags=["equity"],
    responses={404: {"description": "Not found"}},
)


@equity_router.get("/stock/quote")
async def get_quote(ticker: str, date: int):
    return {"ticker": ticker, "quote_date": date}
