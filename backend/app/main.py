from fastapi import FastAPI
from backend.app.api.heartbeat import router as heartbeat_router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(heartbeat_router)
