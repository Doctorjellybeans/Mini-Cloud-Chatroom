from fastapi import FastAPI
from backend.app.api.heartbeat import router as heartbeat_router

app = FastAPI()

app.include_router(heartbeat_router)
