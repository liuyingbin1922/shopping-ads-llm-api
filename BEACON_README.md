# Navigator.sendBeacon 埋点上报服务

## 📊 概述

本项目支持 `navigator.sendBeacon` API，专门为页面卸载时数据上报设计。

## 🚀 快速开始

### 1. 后端 API 端点

```http
POST /api/v1/beacon/beacon     # 完整功能端点
POST /api/v1/beacon/simple     # 简化端点
```

### 2. 前端 JavaScript 库

```html
<script src="static/analytics.js"></script>
<script>
    const analytics = new AnalyticsBeacon({
        baseUrl: 'http://localhost:8000/api/v1/beacon',
        debug: true
    });
    
    analytics.track('button_click', { button_id: 'submit' });
</script>
```

## 📡 API 端点详解

### 完整功能端点

**URL**: `POST /api/v1/beacon/beacon`

```javascript
const data = {
    event_type: "page_view",
    event_name: "homepage_visited",
    user_id: 123,
    session_id: "session_abc123",
    page_url: "https://example.com/",
    properties: {
        page_title: "Homepage",
        referrer: "https://google.com"
    }
};

navigator.sendBeacon('/api/v1/beacon/beacon', 
    new Blob([JSON.stringify(data)], { type: 'application/json' })
);
```

### 简化端点

**URL**: `POST /api/v1/beacon/simple`

```javascript
const url = new URL('/api/v1/beacon/simple');
url.searchParams.set('type', 'page_view');
url.searchParams.set('name', 'page_unload');
url.searchParams.set('url', window.location.href);
url.searchParams.set('uid', '123');

navigator.sendBeacon(url.toString());
```

## 🎯 使用场景

### 页面卸载追踪

```javascript
window.addEventListener('beforeunload', () => {
    const data = {
        event_type: 'page_unload',
        event_name: 'page_closed',
        page_url: window.location.href,
        time_on_page: Date.now() - pageLoadTime
    };
    
    navigator.sendBeacon('/api/v1/beacon/beacon', 
        new Blob([JSON.stringify(data)], { type: 'application/json' })
    );
});
```

### 表单提交追踪

```javascript
document.getElementById('form').addEventListener('submit', (e) => {
    const formData = new FormData();
    formData.append('event_type', 'form_submit');
    formData.append('event_name', 'form_submitted');
    formData.append('user_id', userId);
    
    navigator.sendBeacon('/api/v1/beacon/beacon', formData);
});
```

## 🧪 测试

### 运行测试脚本

```bash
python test_beacon.py
```

### 浏览器测试

打开 `static/demo.html` 在浏览器中测试。

## 📊 数据存储

所有 beacon 事件存储到 `analytics_events` 表：

```sql
SELECT * FROM analytics_events 
WHERE properties LIKE '%beacon%' 
ORDER BY created_at DESC;
```

## 🔍 调试

### 浏览器调试

```javascript
const analytics = new AnalyticsBeacon({ debug: true });
// 查看控制台日志
```

### 服务器日志

```bash
tail -f uvicorn.log
```

## 🚨 注意事项

### 浏览器兼容性

- Chrome 39+
- Firefox 31+
- Safari 11.1+
- Edge 14+

### 数据大小限制

- 大多数浏览器限制为 64KB
- 建议保持数据简洁

### 错误处理

```javascript
if (navigator.sendBeacon) {
    navigator.sendBeacon(url, data);
} else {
    fetch(url, { method: 'POST', body: data });
}
```

## 📈 最佳实践

### 数据设计

```javascript
// 好的数据格式
const goodData = {
    event_type: 'user_action',
    event_name: 'button_click',
    user_id: 'user_123',
    properties: {
        button_id: 'submit',
        timestamp: new Date().toISOString()
    }
};
```

### 性能优化

```javascript
// 批量发送事件
const events = [];
let batchTimeout;

function addToBatch(event) {
    events.push(event);
    clearTimeout(batchTimeout);
    batchTimeout = setTimeout(() => {
        sendBatch(events);
        events.length = 0;
    }, 1000);
}
```

## 🎯 总结

`navigator.sendBeacon` 是页面卸载时数据上报的最佳选择：

- ✅ **非阻塞**: 不会影响页面关闭
- ✅ **可靠**: 浏览器保证数据发送
- ✅ **简单**: API 简单易用
- ✅ **异步**: 后台异步处理
- ✅ **兼容**: 良好的浏览器支持
