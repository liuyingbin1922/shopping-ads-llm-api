# API 端点列表

## 🔐 认证相关

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 | 公开 |
| POST | `/api/v1/auth/login` | 用户登录 | 公开 |

## 👤 用户管理

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| GET | `/api/v1/users/me` | 获取当前用户信息 | 需要认证 |

## 📦 商品管理

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| GET | `/api/v1/products/` | 获取商品列表 | 公开 |
| GET | `/api/v1/products/{product_id}` | 获取单个商品 | 公开 |
| POST | `/api/v1/products/` | 创建商品 | 管理员 |
| PUT | `/api/v1/products/{product_id}` | 更新商品 | 管理员 |
| DELETE | `/api/v1/products/{product_id}` | 删除商品 | 管理员 |

## 🛒 订单管理

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| GET | `/api/v1/orders/` | 获取用户订单列表 | 需要认证 |
| GET | `/api/v1/orders/{order_id}` | 获取单个订单 | 需要认证 |
| POST | `/api/v1/orders/` | 创建订单 | 需要认证 |
| PUT | `/api/v1/orders/{order_id}` | 更新订单状态 | 需要认证 |
| DELETE | `/api/v1/orders/{order_id}` | 取消订单 | 需要认证 |

## 📊 埋点分析

### 基础埋点

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| POST | `/api/v1/analytics/track` | 单条事件上报 | 公开 |
| POST | `/api/v1/analytics/track/batch` | 批量事件上报 | 公开 |

### 便捷埋点

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| POST | `/api/v1/analytics/page-view` | 页面浏览追踪 | 需要认证 |
| POST | `/api/v1/analytics/product-view` | 商品浏览追踪 | 需要认证 |
| POST | `/api/v1/analytics/purchase` | 购买事件追踪 | 需要认证 |

### 数据查询

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| GET | `/api/v1/analytics/events` | 获取事件列表 | 管理员 |
| GET | `/api/v1/analytics/summary` | 获取统计摘要 | 管理员 |
| GET | `/api/v1/analytics/user/{user_id}/events` | 获取用户事件 | 管理员 |
| GET | `/api/v1/analytics/popular-products` | 获取热门商品 | 管理员 |

## 🐰 Beacon API

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| POST | `/api/v1/beacon/beacon` | 完整功能端点 | 公开 |
| POST | `/api/v1/beacon/simple` | 简化端点 | 公开 |

## 🔧 系统

| 方法 | 端点 | 描述 | 权限 |
|------|------|------|------|
| GET | `/` | 根路径 | 公开 |
| GET | `/health` | 健康检查 | 公开 |
| GET | `/docs` | API 文档 (Swagger) | 公开 |
| GET | `/redoc` | API 文档 (ReDoc) | 公开 |

## 📝 查询参数

### 商品列表
- `skip`: 跳过数量 (默认: 0)
- `limit`: 返回数量 (默认: 100)
- `category`: 分类过滤
- `search`: 搜索关键词

### 事件列表
- `event_type`: 事件类型过滤
- `user_id`: 用户 ID 过滤
- `limit`: 返回数量 (默认: 100)
- `offset`: 偏移量 (默认: 0)

### 统计摘要
- `days`: 统计天数 (默认: 7)

### 热门商品
- `days`: 统计天数 (默认: 7)
- `limit`: 返回数量 (默认: 10)

### 简化 Beacon
- `type`: 事件类型
- `name`: 事件名称
- `url`: 页面 URL
- `uid`: 用户 ID

## 🔐 权限说明

### 公开接口
无需认证，可直接访问

### 需要认证
需要有效的 JWT Token

### 管理员接口
需要管理员权限的 JWT Token

## 📊 响应状态码

| 状态码 | 描述 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 成功无内容 (Beacon API) |
| 400 | 请求错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 🚨 错误响应格式

```json
{
  "detail": "错误描述"
}
```

## 📈 数据格式

### 埋点事件
```json
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

### 商品信息
```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics",
  "stock_quantity": 100
}
```

### 订单信息
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```
