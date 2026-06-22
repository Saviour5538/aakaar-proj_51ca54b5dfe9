from fastapi import APIRouter

router = APIRouter(prefix="/ui", tags=["UI"])

@router.get("/")
async def get_ui():
    return {"message": "UI endpoint"}