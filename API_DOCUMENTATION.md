# Shopping API 接口文档

## 📋 概述

Shopping API 是一个基于 FastAPI 构建的电商平台后端服务，提供用户管理、商品管理、订单管理和埋点分析等功能。

**基础信息**:
- **Base URL**: `http://localhost:8000`
- **API 版本**: v1
- **文档地址**: `http://localhost:8000/docs` (Swagger UI)

## 🔐 认证

### JWT Token 认证

大部分 API 需要 JWT Token 认证，在请求头中添加：

```http
Authorization: Bearer <your_jwt_token>
```

### 获取 Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

## 📊 埋点分析 API

### 1. 基础埋点上报

#### 单条事件上报
```http
POST /api/v1/analytics/track
Content-Type: application/json

{
  "event_type": "page_view",
  "event_name": "homepage_visited",
  "user_id": 123,
  "page_url": "https://example.com/",
  "properties": {
    "page_title": "Homepage"
  }
}
```

#### 批量事件上报
```http
POST /api/v1/analytics/track/batch
Content-Type: application/json

{
  "events": [
    {
      "event_type": "page_view",
      "event_name": "page_visited"
    },
    {
      "event_type": "click",
      "event_name": "button_clicked"
    }
  ]
}
```

### 2. 便捷埋点端点

#### 页面浏览追踪
```http
POST /api/v1/analytics/page-view?page_url=https://example.com/products
Authorization: Bearer <token>
```

#### 商品浏览追踪
```http
POST /api/v1/analytics/product-view?product_id=1&product_name=iPhone 15 Pro
Authorization: Bearer <token>
```

#### 购买事件追踪
```http
POST /api/v1/analytics/purchase?order_id=12345&total_amount=999.99&product_ids=[1,2]
Authorization: Bearer <token>
```

### 3. 数据查询 API

#### 获取事件列表
```http
GET /api/v1/analytics/events?event_type=page_view&limit=10
Authorization: Bearer <token>
```

#### 获取统计摘要
```http
GET /api/v1/analytics/summary?days=7
Authorization: Bearer <token>
```

#### 获取用户事件
```http
GET /api/v1/analytics/user/{user_id}/events?limit=50
Authorization: Bearer <token>
```

#### 获取热门商品
```http
GET /api/v1/analytics/popular-products?days=7&limit=10
Authorization: Bearer <token>
```

## 🐰 Beacon API (Navigator.sendBeacon)

### 完整功能端点
```http
POST /api/v1/beacon/beacon
Content-Type: application/json

{
  "event_type": "page_view",
  "event_name": "homepage_visited",
  "user_id": 123,
  "page_url": "https://example.com/",
  "properties": {
    "page_title": "Homepage"
  }
}
```

### 简化端点
```http
POST /api/v1/beacon/simple?type=page_view&name=page_unload&url=https://example.com&uid=123
```

## 👤 用户管理 API

### 用户注册
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "newuser",
  "password": "password123",
  "full_name": "New User"
}
```

### 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin123"
}
```

### 获取当前用户信息
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

## 📦 商品管理 API

### 获取商品列表
```http
GET /api/v1/products/?skip=0&limit=10&category=Electronics&search=iPhone
```

### 获取单个商品
```http
GET /api/v1/products/{product_id}
```

### 创建商品 (管理员)
```http
POST /api/v1/products/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "New Product",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics",
  "stock_quantity": 100
}
```

### 更新商品 (管理员)
```http
PUT /api/v1/products/{product_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Updated Product",
  "price": 89.99
}
```

### 删除商品 (管理员)
```http
DELETE /api/v1/products/{product_id}
Authorization: Bearer <token>
```

## 🛒 订单管理 API

### 获取用户订单列表
```http
GET /api/v1/orders/
Authorization: Bearer <token>
```

### 获取单个订单
```http
GET /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

### 创建订单
```http
POST /api/v1/orders/
Content-Type: application/json
Authorization: Bearer <token>

{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

### 更新订单状态
```http
PUT /api/v1/orders/{order_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "status": "completed"
}
```

### 取消订单
```http
DELETE /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

## 🔧 系统 API

### 健康检查
```http
GET /health
```

### 根路径
```http
GET /
```

## 📊 数据模型

### 用户 (User)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_admin": false,
  "created_at": "2025-08-24T07:14:38"
}
```

### 商品 (Product)
```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics",
  "stock_quantity": 100,
  "is_active": true,
  "created_at": "2025-08-24T07:14:38"
}
```

### 埋点事件 (AnalyticsEvent)
```json
{
  "id": 1,
  "event_type": "page_view",
  "event_name": "homepage_visited",
  "user_id": 1,
  "page_url": "https://example.com/",
  "properties": {
    "page_title": "Homepage"
  },
  "timestamp": "2025-08-24T07:14:38"
}
```

## 🚨 错误响应

### 400 Bad Request
```json
{
  "detail": "Validation error"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "Product not found"
}
```

## 🔐 权限说明

### 公开接口
- 用户注册/登录
- 商品查询
- 埋点上报
- Beacon 上报

### 需要认证的接口
- 用户信息
- 订单管理

### 管理员接口
- 商品管理
- 数据分析查询

## 📝 使用示例

### JavaScript 示例
```javascript
// 初始化埋点
const analytics = new AnalyticsBeacon({
    baseUrl: 'http://localhost:8000/api/v1/beacon',
    debug: true
});

// 追踪事件
analytics.track('page_view', {
    page_title: 'Homepage'
});

// Beacon 上报
navigator.sendBeacon('/api/v1/beacon/beacon', 
    new Blob([JSON.stringify(data)], { type: 'application/json' })
);
```

### cURL 示例
```bash
# 用户登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# 获取商品列表
curl -X GET "http://localhost:8000/api/v1/products/?category=Electronics"

# 埋点上报
curl -X POST http://localhost:8000/api/v1/analytics/track \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","event_name":"api_test"}'
```
