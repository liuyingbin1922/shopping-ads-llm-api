from app.core.database import engine, Base
from app.models import user, product, order, analytics
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.schemas.user import UserCreate
from app.schemas.product import ProductCreate
from app.core.database import SessionLocal


def init_database():
    """Initialize database with tables and sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Adding sample data...")
    db = SessionLocal()
    
    try:
        # Create admin user
        user_service = UserService(db)
        admin_user = user_service.get_user_by_email("admin@example.com")
        if not admin_user:
            admin_data = UserCreate(
                email="admin@example.com",
                username="admin",
                password="admin123",
                full_name="Administrator"
            )
            admin_user = user_service.create_user(admin_data)
            admin_user.is_admin = True
            db.commit()
            print("Created admin user")
        
        # Create sample products
        product_service = ProductService(db)
        sample_products = [
            {
                "name": "iPhone 15 Pro",
                "description": "Latest iPhone with advanced features",
                "price": 999.99,
                "category": "Electronics",
                "stock_quantity": 50
            },
            {
                "name": "MacBook Air M2",
                "description": "Powerful laptop with M2 chip",
                "price": 1199.99,
                "category": "Electronics",
                "stock_quantity": 30
            },
            {
                "name": "Nike Air Max",
                "description": "Comfortable running shoes",
                "price": 129.99,
                "category": "Sports",
                "stock_quantity": 100
            },
            {
                "name": "Coffee Maker",
                "description": "Automatic coffee machine",
                "price": 89.99,
                "category": "Home & Kitchen",
                "stock_quantity": 25
            }
        ]
        
        for product_data in sample_products:
            existing_product = product_service.get_products(search=product_data["name"])
            if not existing_product:
                product_create = ProductCreate(**product_data)
                product_service.create_product(product_create)
                print(f"Created product: {product_data['name']}")
        
        print("Database initialization completed!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
