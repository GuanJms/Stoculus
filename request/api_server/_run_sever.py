from fastapi import FastAPI, APIRouter
from request.api_server.routers import equity_router, option_router, timeline_router, server_router, ratio_router
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
