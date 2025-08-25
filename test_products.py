from app.core.database import SessionLocal
from app.services.product_service import ProductService
from app.models import user, product, order

def test_products():
    """Test product service"""
    try:
        db = SessionLocal()
        product_service = ProductService(db)
        
        # Get products
        products = product_service.get_products(limit=5)
        print(f"Found {len(products)} products")
        
        for p in products:
            print(f"- {p.name}: ${p.price} ({p.category})")
            
        db.close()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_products()
