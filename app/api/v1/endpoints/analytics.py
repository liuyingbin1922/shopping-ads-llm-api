from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.analytics import (
    AnalyticsEventCreate, 
    AnalyticsEventResponse, 
    AnalyticsEventBatch,
    AnalyticsQuery,
    AnalyticsSummary
)
from app.services.analytics_service import AnalyticsService
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter()


def get_request_info(request: Request) -> dict:
    """Extract request information for analytics"""
    return {
        'ip_address': request.client.host if request.client else None,
        'user_agent': request.headers.get('user-agent'),
        'referrer': request.headers.get('referer'),
        'page_url': str(request.url),
    }


@router.post("/track", response_model=dict)
async def track_event(
    event: AnalyticsEventCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Track a single analytics event"""
    analytics_service = AnalyticsService(db)
    request_info = get_request_info(request)
    
    success = analytics_service.track_event(event, request_info)
    
    if success:
        return {"status": "success", "message": "Event tracked successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track event"
        )


@router.post("/track/batch", response_model=dict)
async def track_batch_events(
    batch: AnalyticsEventBatch,
    request: Request,
    db: Session = Depends(get_db)
):
    """Track multiple analytics events"""
    analytics_service = AnalyticsService(db)
    request_info = get_request_info(request)
    
    tracked_count = analytics_service.track_batch(batch.events, request_info)
    
    return {
        "status": "success",
        "message": f"Tracked {tracked_count}/{len(batch.events)} events",
        "tracked_count": tracked_count,
        "total_count": len(batch.events)
    }


@router.get("/events", response_model=List[AnalyticsEventResponse])
async def get_events(
    event_type: str = None,
    user_id: int = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics events (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    analytics_service = AnalyticsService(db)
    query = AnalyticsQuery(
        event_type=event_type,
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    
    events = analytics_service.get_events(query)
    return events


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics summary (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    analytics_service = AnalyticsService(db)
    summary = analytics_service.get_analytics_summary(days)
    return summary


@router.get("/user/{user_id}/events", response_model=List[AnalyticsEventResponse])
async def get_user_events(
    user_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get events for a specific user (admin or self)"""
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    analytics_service = AnalyticsService(db)
    events = analytics_service.get_user_events(user_id, limit)
    return events


@router.get("/popular-products")
async def get_popular_products(
    days: int = 7,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most viewed products (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    analytics_service = AnalyticsService(db)
    products = analytics_service.get_popular_products(days, limit)
    return {"products": products}


# Convenience endpoints for common events
@router.post("/page-view")
async def track_page_view(
    page_url: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track page view event"""
    event = AnalyticsEventCreate(
        event_type="page_view",
        event_name="page_viewed",
        user_id=current_user.id if current_user else None,
        page_url=page_url
    )
    
    analytics_service = AnalyticsService(db)
    request_info = get_request_info(request)
    
    success = analytics_service.track_event(event, request_info)
    
    if success:
        return {"status": "success", "message": "Page view tracked"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track page view"
        )


@router.post("/product-view")
async def track_product_view(
    product_id: int,
    product_name: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track product view event"""
    event = AnalyticsEventCreate(
        event_type="product_view",
        event_name="product_viewed",
        user_id=current_user.id if current_user else None,
        properties={
            "product_id": product_id,
            "product_name": product_name
        }
    )
    
    analytics_service = AnalyticsService(db)
    request_info = get_request_info(request)
    
    success = analytics_service.track_event(event, request_info)
    
    if success:
        return {"status": "success", "message": "Product view tracked"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track product view"
        )


@router.post("/purchase")
async def track_purchase(
    order_id: int,
    total_amount: float,
    product_ids: List[int],
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track purchase event"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    event = AnalyticsEventCreate(
        event_type="purchase",
        event_name="order_completed",
        user_id=current_user.id,
        properties={
            "order_id": order_id,
            "total_amount": total_amount,
            "product_ids": product_ids
        }
    )
    
    analytics_service = AnalyticsService(db)
    request_info = get_request_info(request)
    
    success = analytics_service.track_event(event, request_info)
    
    if success:
        return {"status": "success", "message": "Purchase tracked"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track purchase"
        )
