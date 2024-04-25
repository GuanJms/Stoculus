from fastapi import APIRouter, Response
import asyncio
from colorama import Fore, Back
from datetime import datetime

from request.handlers.option_data_request_handler import OptionDataRequestHandler
from fastapi import HTTPException

option_router = APIRouter(
    prefix="/option",
    tags=["option"],
    responses={404: {"description": "Not found"}},
)

@option_router.get("/quote/eod/")
async def get_option_chain_historical_quote(ticker: str, exp: int, year: int, month:int):
    data = OptionDataRequestHandler.get_option_chain_historical_quote(ticker=ticker, exp=exp,
                                                                      year=year, month=month)
    if data is None:
        raise HTTPException(status_code=472, detail="No data available for the given ticker and expiration.")
    return {
        'ticker': ticker,
        'exp': exp,
        'result': data
    }


@option_router.get("/exp/")
async def get_option_expiration_dates(ticker: str):
    data = OptionDataRequestHandler.get_option_expiration_dates(ticker=ticker)
    if data is None:
        raise HTTPException(status_code=472, detail="No data available for the given ticker and expiration.")
    return {
        'ticker': ticker,
        'exps': data
    }