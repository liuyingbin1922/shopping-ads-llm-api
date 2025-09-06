#!/usr/bin/env python3
"""
RabbitMQ 消息查看器
用于查看 analytics_events 队列中的消息
"""

import pika
import json
import sys
from datetime import datetime

def view_messages():
    """查看 RabbitMQ 队列中的消息"""
    try:
        # 连接到 RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                virtual_host='/',
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        channel = connection.channel()
        
        # 获取队列信息
        queue_name = 'analytics_events'
        method = channel.queue_declare(queue=queue_name, durable=True, passive=True)
        message_count = method.method.message_count
        
        print(f"📊 RabbitMQ 队列状态 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   队列名称: {queue_name}")
        print(f"   消息数量: {message_count}")
        print("=" * 60)
        
        if message_count == 0:
            print("📭 队列中没有消息")
            return
        
        # 显示所有消息
        for i in range(message_count):
            method, properties, body = channel.basic_get(queue=queue_name, auto_ack=False)
            if method:
                try:
                    message_data = json.loads(body.decode('utf-8'))
                    print(f"\n📨 消息 {i+1}:")
                    print(f"   🎯 事件类型: {message_data.get('event_type')}")
                    print(f"   📝 事件名称: {message_data.get('event_name')}")
                    print(f"   👤 用户ID: {message_data.get('user_id')}")
                    print(f"   🔗 会话ID: {message_data.get('session_id')}")
                    print(f"   🌐 页面URL: {message_data.get('page_url')}")
                    print(f"   ⏰ 时间戳: {message_data.get('timestamp')}")
                    
                    properties = message_data.get('properties', {})
                    if properties:
                        print(f"   📋 属性:")
                        for key, value in properties.items():
                            print(f"      {key}: {value}")
                    
                    print("-" * 40)
                    
                except Exception as e:
                    print(f"   ❌ 解析消息失败: {e}")
                    print(f"   📄 原始数据: {body.decode('utf-8')}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ 连接 RabbitMQ 失败: {e}")
        print("请确保 RabbitMQ 服务正在运行")

def consume_messages():
    """实时消费消息（会删除消息）"""
    def callback(ch, method, properties, body):
        try:
            message_data = json.loads(body.decode('utf-8'))
            print(f"\n🔄 收到新消息 - {datetime.now().strftime('%H:%M:%S')}")
            print(f"   🎯 事件: {message_data.get('event_type')} - {message_data.get('event_name')}")
            print(f"   👤 用户: {message_data.get('user_id')}")
            print(f"   🌐 页面: {message_data.get('page_url')}")
            
            # 确认消息
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"❌ 处理消息失败: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                virtual_host='/',
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        channel = connection.channel()
        
        queue_name = 'analytics_events'
        channel.queue_declare(queue=queue_name, durable=True)
        
        print(f"🔄 开始实时消费消息... (按 Ctrl+C 停止)")
        print(f"   队列: {queue_name}")
        print("=" * 60)
        
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback
        )
        
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print("\n⏹️  停止消费消息")
        channel.stop_consuming()
        connection.close()
    except Exception as e:
        print(f"❌ 消费消息失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "consume":
        consume_messages()
    else:
        view_messages()
