from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_orders():
    """Get all orders"""
    return {"message": "Orders endpoint"}
