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
    DATE: Optional[str | int] = None

@timeline_router.get("/time/next/")
async def get_read_upto_time(public_token: str | None = None,
                             private_key: str | None = None,
                             time: int | float | None = None):
    if not isinstance(time, (int, float)):
        raise HTTPException(status_code=400, detail="Invalid time")
    if not TokenManager.is_valid_token(public_token, private_key):
        raise HTTPException(status_code=400, detail="Invalid token")
    token = TokenManager.decrypt_token(public_token, private_key)
    data = RequestHandler.handle_read_upto_time_request(token, time)
    return data


@timeline_router.post("/start/")
async def start_cache(tickers: Dict[str, TickerDomainInfo], hub_id: Optional[str] = None):
    public_token, key, token = RequestHandler.create_timeline_cache()

    prev_token = RequestHandler.find_token(hub_id) # type: None | str
    if prev_token:
        RequestHandler.delete_token(prev_token)

    failed_tickers = []
    errors = []
    for ticker, domain_info in tickers.items():
        domain_chain_str = domain_info.DOMAINS
        date = domain_info.DATE
        try:
            if hub_id is not None:
                RequestHandler.register_token(hub_id, token)
            RequestHandler.create_reader(domain_chain_str=domain_chain_str, token=token,
                                         root=ticker, date=date)
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
async def get_timeline_status(public_token: str | None = None, private_key: str | None = None):
    if not TokenManager.is_valid_token(public_token, private_key):
        raise HTTPException(status_code=400, detail="Invalid token")
    token = TokenManager.decrypt_token(public_token, private_key)
    return {
        'status': RequestHandler.get_cache_status(token)
    }

@timeline_router.get("/status/tickers/")
async def get_timeline_status(public_token: str | None = None, private_key: str | None = None):
    if not TokenManager.is_valid_token(public_token, private_key):
        raise HTTPException(status_code=400, detail="Invalid token")
    token = TokenManager.decrypt_token(public_token, private_key)
    return {
        'tickers': RequestHandler.get_tickers(token)
    }





