from fastapi import APIRouter

router = APIRouter()

@router.get("/heartbeat", tags=["heartbeat"])
async def heartbeat():
    return {"status": "ok"}
