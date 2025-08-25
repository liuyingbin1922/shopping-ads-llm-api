# Analytics & RabbitMQ Integration

## 📊 概述

本系统实现了完整的埋点上报服务，集成了 RabbitMQ 消息队列，用于收集、处理和存储用户行为数据。

## 🏗️ 系统架构

```
Frontend → FastAPI Analytics → RabbitMQ Queue → Consumer Service
                ↓
            Database (SQLite)
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动 RabbitMQ (可选)
```bash
docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3
```

### 3. 初始化数据库
```bash
python init_db.py
```

### 4. 启动服务
```bash
# API 服务
python main.py

# 消费者服务 (新终端)
python analytics_consumer.py
```

## 📡 API 端点

### 基础埋点
```http
POST /api/v1/analytics/track
{
  "event_type": "page_view",
  "event_name": "homepage_visited",
  "page_url": "https://example.com/"
}
```

### 便捷端点
```http
POST /api/v1/analytics/page-view?page_url=https://example.com/
POST /api/v1/analytics/product-view?product_id=1&product_name=iPhone
POST /api/v1/analytics/purchase?order_id=123&total_amount=999.99
```

## 🧪 测试

```bash
python test_analytics.py
```

## ⚙️ 配置

环境变量:
```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
ANALYTICS_ENABLED=true
ANALYTICS_QUEUE_NAME=analytics_events
```
