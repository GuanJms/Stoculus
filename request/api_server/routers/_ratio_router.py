from typing import Annotated, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from request.handlers import FundamentalDataRequestHandler

ratio_router = APIRouter(
    prefix="/ratio",
    tags=["server"],
    responses={404: {"description": "Not found"}},
)


@ratio_router.get("/company/{ticker}")
async def get_server_status(ticker: str):
    data = FundamentalDataRequestHandler.get_financial_ratio(ticker)
    # convert data in to
    return {
        'ticker': ticker,
        'result': data
    }