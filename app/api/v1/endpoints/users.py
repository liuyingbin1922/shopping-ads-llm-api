from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_users():
    """Get all users"""
    return {"message": "Users endpoint"}
