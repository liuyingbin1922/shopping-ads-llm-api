import json
import logging
import pika
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnalyticsConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
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
                durable=True
            )
            
            # Set QoS for fair dispatch
            self.channel.basic_qos(prefetch_count=1)
            
            logger.info("Analytics consumer connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"Failed to connect analytics consumer to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def process_analytics_event(self, ch, method, properties, body):
        """Process analytics event from RabbitMQ"""
        try:
            # Parse the message
            event_data = json.loads(body.decode('utf-8'))
            
            # Log the event
            logger.info(f"Processing analytics event: {event_data.get('event_name', 'unknown')}")
            
            # Here you can add additional processing logic:
            # - Send to external analytics services (Google Analytics, Mixpanel, etc.)
            # - Store in data warehouse
            # - Generate real-time reports
            # - Trigger alerts for specific events
            
            # Example: Process different event types
            event_type = event_data.get('event_type')
            if event_type == 'purchase':
                self._process_purchase_event(event_data)
            elif event_type == 'product_view':
                self._process_product_view_event(event_data)
            elif event_type == 'page_view':
                self._process_page_view_event(event_data)
            else:
                self._process_generic_event(event_data)
            
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error processing analytics event: {e}")
            # Reject the message and requeue it
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def _process_purchase_event(self, event_data: Dict[str, Any]):
        """Process purchase events"""
        logger.info(f"Purchase event: Order {event_data.get('properties', {}).get('order_id')} "
                   f"for ${event_data.get('properties', {}).get('total_amount')}")
        
        # Add your purchase processing logic here
        # - Update revenue metrics
        # - Send purchase confirmation emails
        # - Update inventory
        # - Generate sales reports

    def _process_product_view_event(self, event_data: Dict[str, Any]):
        """Process product view events"""
        properties = event_data.get('properties', {})
        logger.info(f"Product view: {properties.get('product_name')} (ID: {properties.get('product_id')})")
        
        # Add your product view processing logic here
        # - Update product popularity metrics
        # - Generate product recommendations
        # - Track user behavior patterns

    def _process_page_view_event(self, event_data: Dict[str, Any]):
        """Process page view events"""
        logger.info(f"Page view: {event_data.get('page_url')}")
        
        # Add your page view processing logic here
        # - Update page popularity metrics
        # - Track user navigation patterns
        # - Generate heatmaps

    def _process_generic_event(self, event_data: Dict[str, Any]):
        """Process generic events"""
        logger.info(f"Generic event: {event_data.get('event_name')} of type {event_data.get('event_type')}")

    def start_consuming(self):
        """Start consuming messages from RabbitMQ"""
        if not self.connection or self.connection.is_closed:
            logger.error("RabbitMQ connection not available")
            return
        
        try:
            # Set up the consumer
            self.channel.basic_consume(
                queue=settings.ANALYTICS_QUEUE_NAME,
                on_message_callback=self.process_analytics_event
            )
            
            logger.info("Starting analytics consumer...")
            logger.info(f"Waiting for messages on queue: {settings.ANALYTICS_QUEUE_NAME}")
            
            # Start consuming
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Stopping analytics consumer...")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error in analytics consumer: {e}")
            self.stop_consuming()

    def stop_consuming(self):
        """Stop consuming messages"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("Analytics consumer stopped")
        except Exception as e:
            logger.error(f"Error stopping analytics consumer: {e}")


# Global consumer instance
analytics_consumer = AnalyticsConsumer()
