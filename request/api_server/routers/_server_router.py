from typing import Annotated, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from colorama import Fore, Back
from request.handlers.tokens import TokenManager
from request.handlers import RequestHandler

server_router = APIRouter(
    prefix="/server",
    tags=["server"],
    responses={404: {"description": "Not found"}},
)


@server_router.get("/status/")
async def get_server_status(public_token: str | None = None,
                             private_key: str | None = None):
    if public_token != 'server' or private_key != 'server':
        raise HTTPException(status_code=400, detail="Invalid token")
    status = RequestHandler.get_server_status()
    return {
        'cache manager status': status
    }