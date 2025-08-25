#!/usr/bin/env python3
"""
Analytics Consumer Script

This script starts the RabbitMQ consumer for processing analytics events.
Run this script to start consuming analytics events from the RabbitMQ queue.
"""

import sys
import os
import signal
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.analytics_consumer import analytics_consumer
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('analytics_consumer.log')
    ]
)

logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    analytics_consumer.stop_consuming()
    sys.exit(0)


def main():
    """Main function to start the analytics consumer"""
    logger.info("Starting Analytics Consumer...")
    logger.info(f"RabbitMQ Host: {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}")
    logger.info(f"Queue Name: {settings.ANALYTICS_QUEUE_NAME}")
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Check if RabbitMQ is available
        if not analytics_consumer.connection or analytics_consumer.connection.is_closed:
            logger.error("Failed to connect to RabbitMQ. Please ensure RabbitMQ is running.")
            sys.exit(1)
        
        # Start consuming messages
        analytics_consumer.start_consuming()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        analytics_consumer.stop_consuming()
        logger.info("Analytics Consumer stopped.")


if __name__ == "__main__":
    main()
