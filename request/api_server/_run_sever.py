from fastapi import FastAPI, APIRouter
from request.api_server.routers._equity_router import equity_router
from request.api_server.routers._timeline_router import timeline_router
from request.api_server.routers._server_router import server_router
from request.api_server.routers._ratio_router import ratio_router
from request.api_server.routers._option_router import option_router
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
internal_router = APIRouter()


@app.get("/")
async def home():
    return {"message": "Welcome to Stoculus!"}


@app.exception_handler(ValueError)
async def general_exception_handler(request, exc: ValueError):
    """
    Catch unhandled exceptions and return a custom response.
    This handler will catch any exception in the application.
    """
    return JSONResponse(
        status_code=500,
        content={"message": "Stoculus Server Error", "detail": str(exc)},
    )


internal_router.include_router(equity_router)
internal_router.include_router(option_router)
internal_router.include_router(timeline_router)
internal_router.include_router(server_router)
internal_router.include_router(ratio_router)
app.include_router(internal_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1999)
