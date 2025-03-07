from fastapi import APIRouter

router = APIRouter()

@router.get("/climate")
async def get_climate():
    return {"message": "Climate Data"}
