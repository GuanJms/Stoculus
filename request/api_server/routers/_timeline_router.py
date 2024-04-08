from typing import Annotated, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from colorama import Fore, Back
from request.handlers.tokens import TokenManager
from request.handlers import RequestHandler

timeline_router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
    responses={404: {"description": "Not found"}},
)


class TickerDomainInfo(BaseModel):
    DOMAINS: str
    DATE: Optional[str] = None


class TokenHeader(BaseModel):
    public_token: str
    key: str


@timeline_router.get("/time/next/")
async def get_read_upto_time(public_token: str | None = None,
                             key: str | None = None,
                             time: int | None = None):
    if not isinstance(time, int):
        raise HTTPException(status_code=400, detail="Invalid time")
    if not TokenManager.is_valid_token(public_token, key):
        raise HTTPException(status_code=400, detail="Invalid token")
    token = TokenManager.decrypt_token(public_token, key)
    data = RequestHandler.handle_read_upto_time_request(token, time)
    return data


@timeline_router.post("/start/")
async def start_cache(tickers: Dict[str, TickerDomainInfo]):
    public_token, key, token = RequestHandler.create_timeline_cache()
    failed_tickers = []
    errors = []
    for ticker, domain_info in tickers.items():
        domain_chain_str = domain_info.DOMAINS
        date = domain_info.DATE
        try:
            RequestHandler.create_reader(domain_chain_str=domain_chain_str, token=token, root=ticker, date=date)
        except ValueError as e:
            failed_tickers.append(ticker)
            errors.append(str(e))
    return {
        'public_token': public_token,
        'private_key': key,
        'failed_tickers': failed_tickers,
        'errors': errors
    }


@timeline_router.get("/status/")
async def get_timeline_status(public_token: str | None = None, key: str | None = None):
    if not TokenManager.is_valid_token(public_token, key):
        raise HTTPException(status_code=400, detail="Invalid token")
    token = TokenManager.decrypt_token(public_token, key)
    return {
        'status': RequestHandler.get_cache_status(token)
    }
