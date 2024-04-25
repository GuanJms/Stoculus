from fastapi import APIRouter, Response
import asyncio
from colorama import Fore, Back
from datetime import datetime

from request.handlers.option_data_request_handler import OptionDataRequestHandler
from fastapi import HTTPException

ticker_router = APIRouter(
    prefix="/ticker",
    tags=["ticker"],
    responses={404: {"description": "Not found"}},
)


@ticker_router.get("/check")
async def check_ticker_existence(ticker: str, exp: int, year: int, month: int):
    data = OptionDataRequestHandler.get_option_chain_historical_quote(ticker=ticker, exp=exp,
                                                                      year=year, month=month)
    if data is None:
        raise HTTPException(status_code=472, detail="No data available for the given ticker and expiration.")
    return {
        'ticker': ticker,
        'exp': exp,
        'result': data
    }
