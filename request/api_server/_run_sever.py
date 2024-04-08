from fastapi import FastAPI, APIRouter
from request.api_server.routers._equity_router import equity_router
from request.api_server.routers._timeline_router import timeline_router
import uvicorn


app = FastAPI()
internal_router = APIRouter()


@app.get("/")
async def home():
    return {"message": "Welcome to Stoculus!"}


internal_router.include_router(equity_router)
internal_router.include_router(timeline_router)
app.include_router(internal_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
