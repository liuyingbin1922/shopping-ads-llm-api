# Shopping API

A modern RESTful API for an e-commerce platform built with FastAPI, SQLAlchemy, and SQLite.

## Features

- **User Management**: Registration, authentication, and user profile management
- **Product Management**: CRUD operations for products with categories and stock management
- **Order Management**: Order creation, tracking, and status management
- **Authentication**: JWT-based authentication with password hashing
- **Database**: SQLite database with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Analytics**: Comprehensive analytics and tracking system
- **Beacon API**: Navigator.sendBeacon support for reliable data collection

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite**: Lightweight database for development
- **Uvicorn**: ASGI server for running FastAPI applications
- **RabbitMQ**: Message queue for analytics processing
- **Redis**: Caching and session management

## Project Structure

```
python-shopping-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── products.py
│   │       │   ├── orders.py
│   │       │   ├── analytics.py
│   │       │   └── beacon.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── rabbitmq.py
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── analytics.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── auth.py
│   │   └── analytics.py
│   └── services/
│       ├── auth_service.py
│       ├── user_service.py
│       ├── product_service.py
│       ├── order_service.py
│       ├── analytics_service.py
│       └── analytics_consumer.py
├── static/
│   ├── analytics.js
│   └── demo.html
├── main.py
├── init_db.py
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
├── API_ENDPOINTS.md
├── ANALYTICS_README.md
├── BEACON_README.md
└── BEACON_SUMMARY.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-shopping-api
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Complete API Documentation**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **API Endpoints List**: [API_ENDPOINTS.md](./API_ENDPOINTS.md)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user account

### Products
- `GET /api/v1/products/` - Get all products
- `GET /api/v1/products/{product_id}` - Get product by ID
- `POST /api/v1/products/` - Create new product (admin only)
- `PUT /api/v1/products/{product_id}` - Update product (admin only)
- `DELETE /api/v1/products/{product_id}` - Delete product (admin only)

### Orders
- `GET /api/v1/orders/` - Get user's orders
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `POST /api/v1/orders/` - Create new order
- `PUT /api/v1/orders/{order_id}` - Update order status
- `DELETE /api/v1/orders/{order_id}` - Cancel order

### Analytics
- `POST /api/v1/analytics/track` - Track single event
- `POST /api/v1/analytics/track/batch` - Track multiple events
- `POST /api/v1/analytics/page-view` - Track page view
- `POST /api/v1/analytics/product-view` - Track product view
- `POST /api/v1/analytics/purchase` - Track purchase
- `GET /api/v1/analytics/events` - Get events (admin)
- `GET /api/v1/analytics/summary` - Get analytics summary (admin)

### Beacon API
- `POST /api/v1/beacon/beacon` - Full beacon endpoint
- `POST /api/v1/beacon/simple` - Simple beacon endpoint

## Sample Data

The database initialization script creates:

- **Admin user**: 
  - Email: admin@example.com
  - Password: admin123
  - Username: admin

- **Sample products**:
  - iPhone 15 Pro ($999.99)
  - MacBook Air M2 ($1199.99)
  - Nike Air Max ($129.99)
  - Coffee Maker ($89.99)

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=11520
DATABASE_URL=sqlite:///./shopping_api.db
ENVIRONMENT=development
DEBUG=true
ALLOWED_HOSTS=["*"]

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest

# Analytics Configuration
ANALYTICS_ENABLED=true
ANALYTICS_QUEUE_NAME=analytics_events
```

## Development

### Running in Development Mode
```bash
python main.py
```

The server will run with auto-reload enabled.

### Running Tests
```bash
# Test analytics functionality
python test_analytics_standalone.py

# Test beacon functionality
python test_beacon.py

# Test products functionality
python test_products.py
```

### Analytics Consumer
```bash
# Start the analytics consumer (in a separate terminal)
python analytics_consumer.py
```

### Database Migrations
For production, consider using Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Analytics & Tracking

### Frontend Integration
Include the analytics library in your frontend:

```html
<script src="static/analytics.js"></script>
<script>
    const analytics = new AnalyticsBeacon({
        baseUrl: 'http://localhost:8000/api/v1/beacon',
        debug: true
    });
    
    analytics.track('page_view', { page_title: 'Homepage' });
</script>
```

### Beacon API Usage
```javascript
// Page unload tracking
window.addEventListener('beforeunload', () => {
    const data = {
        event_type: 'page_unload',
        event_name: 'page_closed',
        page_url: window.location.href
    };
    
    navigator.sendBeacon('/api/v1/beacon/beacon', 
        new Blob([JSON.stringify(data)], { type: 'application/json' })
    );
});
```

For detailed analytics documentation, see:
- [Analytics Documentation](./ANALYTICS_README.md)
- [Beacon API Documentation](./BEACON_README.md)
- [Analytics Summary](./ANALYTICS_SUMMARY.md)
- [Beacon Summary](./BEACON_SUMMARY.md)

## Production Deployment

For production deployment:

1. Change the database URL to PostgreSQL or MySQL
2. Set a strong SECRET_KEY
3. Configure proper CORS settings
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Set up proper logging and monitoring
6. Configure RabbitMQ and Redis for production use
7. Set up proper SSL/TLS certificates

## License

This project is licensed under the MIT License.
