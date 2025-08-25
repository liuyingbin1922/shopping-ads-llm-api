from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up FastAPI application...")
    print("Initializing analytics system...")
    
    # Initialize RabbitMQ connection
    try:
        from app.core.rabbitmq import rabbitmq_manager
        if rabbitmq_manager.is_connected():
            print("✅ RabbitMQ connection established")
        else:
            print("⚠️  RabbitMQ connection failed - analytics events will be stored locally only")
    except Exception as e:
        print(f"⚠️  RabbitMQ initialization error: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down FastAPI application...")
    
    # Close RabbitMQ connection
    try:
        from app.core.rabbitmq import rabbitmq_manager
        rabbitmq_manager.close()
        print("✅ RabbitMQ connection closed")
    except Exception as e:
        print(f"⚠️  Error closing RabbitMQ connection: {e}")


app = FastAPI(
    title="Shopping API",
    description="A modern shopping API built with FastAPI and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Shopping API with Analytics"}


@app.get("/health")
async def health_check():
    # Check RabbitMQ connection
    rabbitmq_status = "unknown"
    try:
        from app.core.rabbitmq import rabbitmq_manager
        rabbitmq_status = "connected" if rabbitmq_manager.is_connected() else "disconnected"
    except:
        rabbitmq_status = "error"
    
    return {
        "status": "healthy", 
        "message": "Service is running",
        "analytics": {
            "enabled": settings.ANALYTICS_ENABLED,
            "rabbitmq": rabbitmq_status
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
