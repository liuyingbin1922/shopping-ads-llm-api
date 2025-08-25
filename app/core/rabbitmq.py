import pika
import json
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQManager:
    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._connect()

    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USERNAME,
                settings.RABBITMQ_PASSWORD
            )
            
            parameters = pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare the analytics queue
            self.channel.queue_declare(
                queue=settings.ANALYTICS_QUEUE_NAME,
                durable=True,
                arguments={
                    'x-message-ttl': 86400000,  # 24 hours in milliseconds
                    'x-max-length': 10000  # Max 10k messages
                }
            )
            
            logger.info("Successfully connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def is_connected(self) -> bool:
        """Check if connected to RabbitMQ"""
        return self.connection is not None and not self.connection.is_closed

    def publish_event(self, event_data: Dict[str, Any], routing_key: str = None) -> bool:
        """Publish event to RabbitMQ queue"""
        if not self.is_connected():
            logger.warning("RabbitMQ not connected, attempting to reconnect...")
            self._connect()
            
        if not self.is_connected():
            logger.error("Failed to reconnect to RabbitMQ")
            return False
            
        try:
            # Use default queue if no routing key specified
            if routing_key is None:
                routing_key = settings.ANALYTICS_QUEUE_NAME
                
            message = json.dumps(event_data, default=str)
            
            self.channel.basic_publish(
                exchange='',
                routing_key=routing_key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            
            logger.debug(f"Published event to RabbitMQ: {event_data.get('event_name', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish event to RabbitMQ: {e}")
            return False

    def publish_batch(self, events: list[Dict[str, Any]], routing_key: str = None) -> int:
        """Publish multiple events to RabbitMQ queue"""
        if not self.is_connected():
            logger.warning("RabbitMQ not connected, attempting to reconnect...")
            self._connect()
            
        if not self.is_connected():
            logger.error("Failed to reconnect to RabbitMQ")
            return 0
            
        published_count = 0
        
        try:
            for event_data in events:
                if self.publish_event(event_data, routing_key):
                    published_count += 1
                    
            logger.info(f"Published {published_count}/{len(events)} events to RabbitMQ")
            return published_count
            
        except Exception as e:
            logger.error(f"Failed to publish batch to RabbitMQ: {e}")
            return published_count

    def close(self):
        """Close RabbitMQ connection"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")


# Global RabbitMQ manager instance
rabbitmq_manager = RabbitMQManager()
