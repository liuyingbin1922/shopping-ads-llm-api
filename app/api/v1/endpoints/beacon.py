from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsEventCreate
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_request_info(request: Request) -> dict:
    """Extract request information for analytics"""
    return {
        'ip_address': request.client.host if request.client else None,
        'user_agent': request.headers.get('user-agent'),
        'referrer': request.headers.get('referer'),
        'page_url': str(request.url),
    }


@router.post("/beacon")
async def beacon_track(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle navigator.sendBeacon requests
    
    This endpoint is optimized for sendBeacon:
    - Accepts both JSON and form data
    - Returns minimal response (204 No Content)
    - Handles page unload events
    - Non-blocking operation
    """
    try:
        # Get content type
        content_type = request.headers.get('content-type', '')
        
        # Parse request data based on content type
        if 'application/json' in content_type:
            data = await request.json()
        elif 'text/plain' in content_type:
            body = await request.body()
            data = json.loads(body.decode('utf-8'))
        else:
            form_data = await request.form()
            data = dict(form_data)
        
        # Extract event data
        event_type = data.get('event_type', 'beacon')
        event_name = data.get('event_name', 'page_unload')
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        page_url = data.get('page_url')
        properties = data.get('properties', {})
        
        # Add beacon-specific properties
        beacon_properties = {
            'beacon': True,
            'page_unload': True,
            **properties
        }
        
        # Create analytics event
        event_data = AnalyticsEventCreate(
            event_type=event_type,
            event_name=event_name,
            user_id=user_id,
            session_id=session_id,
            page_url=page_url,
            properties=beacon_properties
        )
        
        # Track event
        request_info = get_request_info(request)
        analytics_service = AnalyticsService(db)
        success = analytics_service.track_event(event_data, request_info)
        
        if success:
            logger.info(f"Beacon event tracked: {event_name}")
        
        # Return 204 No Content for sendBeacon
        return Response(status_code=204)
        
    except Exception as e:
        logger.error(f"Error processing beacon request: {e}")
        return Response(status_code=204)


@router.post("/simple")
async def beacon_simple_track(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Simple beacon endpoint for basic tracking
    """
    try:
        # Get data from query parameters or body
        if request.method == 'GET':
            event_type = request.query_params.get('type', 'page_view')
            event_name = request.query_params.get('name', 'page_unload')
            page_url = request.query_params.get('url', '')
            user_id = request.query_params.get('uid')
        else:
            try:
                data = await request.json()
            except:
                form_data = await request.form()
                data = dict(form_data)
            
            event_type = data.get('type', 'page_view')
            event_name = data.get('name', 'page_unload')
            page_url = data.get('url', '')
            user_id = data.get('uid')
        
        # Create event
        event_data = AnalyticsEventCreate(
            event_type=event_type,
            event_name=event_name,
            user_id=user_id,
            page_url=page_url,
            properties={'beacon': True, 'simple': True}
        )
        
        # Track event
        request_info = get_request_info(request)
        analytics_service = AnalyticsService(db)
        success = analytics_service.track_event(event_data, request_info)
        
        if success:
            logger.info(f"Simple beacon event tracked: {event_name}")
        
        return Response(status_code=204)
        
    except Exception as e:
        logger.error(f"Error processing simple beacon request: {e}")
        return Response(status_code=204)
