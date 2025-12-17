# libraries
from fastapi import FastAPI

# Modules
from backend.app.api.heartbeat import router as heartbeat_router 
from backend.app.core.config import settings 
from backend.app.api.views import router as views_router
from backend.app.api.websocket import router as chat_router


# App instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Routers


# Heartbeat router
app.include_router(heartbeat_router)
app.include_router(views_router)
app.include_router(chat_router)