from fastapi import APIRouter
from app.api.v1.endpoints import users, products, orders, auth, analytics, beacon

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(beacon.router, prefix="/beacon", tags=["beacon"])
