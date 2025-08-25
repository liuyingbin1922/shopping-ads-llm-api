from app.core.database import SessionLocal
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate
# Import all models to ensure they are registered
from app.models import user, product, order
import random

def add_mock_products():
    """Add realistic mock products to the database"""
    db = SessionLocal()
    product_service = ProductService(db)
    
    # Check existing products
    existing_products = product_service.get_products()
    print(f"Found {len(existing_products)} existing products")
    
    # Mock product data - realistic e-commerce products
    mock_products = [
        # Electronics
        {
            "name": "Samsung Galaxy S24 Ultra",
            "description": "Premium Android smartphone with S Pen, 200MP camera, and AI features",
            "price": 1299.99,
            "category": "Electronics",
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
            "stock_quantity": 45
        },
        {
            "name": "Sony WH-1000XM5 Wireless Headphones",
            "description": "Industry-leading noise cancellation with 30-hour battery life",
            "price": 349.99,
            "category": "Electronics",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
            "stock_quantity": 78
        },
        {
            "name": "iPad Pro 12.9-inch (M4)",
            "description": "Most powerful iPad with Liquid Retina XDR display and Apple Pencil Pro support",
            "price": 1099.99,
            "category": "Electronics",
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
            "stock_quantity": 32
        },
        {
            "name": "DJI Mini 4 Pro Drone",
            "description": "Ultralight camera drone with 4K video and obstacle avoidance",
            "price": 759.99,
            "category": "Electronics",
            "image_url": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400",
            "stock_quantity": 15
        },
        {
            "name": "Nintendo Switch OLED",
            "description": "Handheld gaming console with 7-inch OLED screen",
            "price": 349.99,
            "category": "Electronics",
            "image_url": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400",
            "stock_quantity": 89
        },
        
        # Fashion & Apparel
        {
            "name": "Levi's 501 Original Jeans",
            "description": "Classic straight-leg jeans in authentic denim",
            "price": 89.99,
            "category": "Fashion",
            "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
            "stock_quantity": 156
        },
        {
            "name": "Adidas Ultraboost 22 Running Shoes",
            "description": "Premium running shoes with responsive Boost midsole",
            "price": 189.99,
            "category": "Fashion",
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "stock_quantity": 67
        },
        {
            "name": "Ray-Ban Aviator Classic",
            "description": "Timeless aviator sunglasses with gold frame and green lenses",
            "price": 169.99,
            "category": "Fashion",
            "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",
            "stock_quantity": 42
        },
        {
            "name": "Casio G-Shock DW5600E",
            "description": "Rugged digital watch with shock resistance and water resistance",
            "price": 49.99,
            "category": "Fashion",
            "image_url": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400",
            "stock_quantity": 93
        },
        {
            "name": "Uniqlo Heattech Long Sleeve T-Shirt",
            "description": "Thermal underwear with moisture-wicking technology",
            "price": 19.99,
            "category": "Fashion",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            "stock_quantity": 234
        },
        
        # Home & Kitchen
        {
            "name": "Instant Pot Duo 7-in-1",
            "description": "Electric pressure cooker with 7 cooking functions",
            "price": 99.99,
            "category": "Home & Kitchen",
            "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",
            "stock_quantity": 28
        },
        {
            "name": "Dyson V15 Detect Cordless Vacuum",
            "description": "Powerful cordless vacuum with laser dust detection",
            "price": 699.99,
            "category": "Home & Kitchen",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
            "stock_quantity": 19
        },
        {
            "name": "KitchenAid Artisan Stand Mixer",
            "description": "Professional 5-quart stand mixer with 10-speed motor",
            "price": 379.99,
            "category": "Home & Kitchen",
            "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",
            "stock_quantity": 34
        },
        {
            "name": "Philips Hue White and Color Ambiance",
            "description": "Smart LED light bulbs with 16 million colors",
            "price": 49.99,
            "category": "Home & Kitchen",
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400",
            "stock_quantity": 87
        },
        {
            "name": "Ninja Foodi 9-in-1 Deluxe",
            "description": "Multi-cooker with pressure cooking and air frying",
            "price": 199.99,
            "category": "Home & Kitchen",
            "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400",
            "stock_quantity": 41
        },
        
        # Sports & Outdoors
        {
            "name": "Yeti Rambler 20oz Tumbler",
            "description": "Vacuum insulated stainless steel tumbler with 24-hour cold retention",
            "price": 34.99,
            "category": "Sports & Outdoors",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
            "stock_quantity": 123
        },
        {
            "name": "Patagonia Down Sweater Jacket",
            "description": "Lightweight down jacket with 800-fill-power goose down",
            "price": 229.99,
            "category": "Sports & Outdoors",
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
            "stock_quantity": 56
        },
        {
            "name": "GoPro HERO11 Black",
            "description": "Action camera with 5.3K video and HyperSmooth 5.0 stabilization",
            "price": 399.99,
            "category": "Sports & Outdoors",
            "image_url": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400",
            "stock_quantity": 23
        },
        {
            "name": "Osprey Atmos AG 65 Backpack",
            "description": "65-liter backpack with Anti-Gravity suspension system",
            "price": 249.99,
            "category": "Sports & Outdoors",
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
            "stock_quantity": 18
        },
        {
            "name": "Garmin Fenix 7 Sapphire Solar",
            "description": "Premium multisport GPS watch with solar charging",
            "price": 899.99,
            "category": "Sports & Outdoors",
            "image_url": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400",
            "stock_quantity": 12
        },
        
        # Books & Media
        {
            "name": "Kindle Paperwhite (8GB)",
            "description": "Waterproof e-reader with 6.8-inch display and adjustable warm light",
            "price": 139.99,
            "category": "Books & Media",
            "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",
            "stock_quantity": 67
        },
        {
            "name": "Bose QuietComfort 45 Headphones",
            "description": "Over-ear headphones with world-class noise cancellation",
            "price": 329.99,
            "category": "Books & Media",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
            "stock_quantity": 38
        },
        {
            "name": "JBL Flip 6 Portable Speaker",
            "description": "Waterproof portable Bluetooth speaker with 12 hours of playtime",
            "price": 129.99,
            "category": "Books & Media",
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
            "stock_quantity": 89
        },
        {
            "name": "Sony PlayStation 5 Digital Edition",
            "description": "Next-gen gaming console with ultra-high-speed SSD",
            "price": 399.99,
            "category": "Books & Media",
            "image_url": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400",
            "stock_quantity": 15
        },
        {
            "name": "Apple TV 4K (128GB)",
            "description": "Streaming device with 4K HDR and Dolby Atmos support",
            "price": 179.99,
            "category": "Books & Media",
            "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400",
            "stock_quantity": 42
        },
        
        # Beauty & Personal Care
        {
            "name": "Dyson Airwrap Multi-styler",
            "description": "Hair styling tool with intelligent heat control",
            "price": 599.99,
            "category": "Beauty & Personal Care",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400",
            "stock_quantity": 27
        },
        {
            "name": "Oral-B iO Series 9 Electric Toothbrush",
            "description": "Smart electric toothbrush with AI recognition and app connectivity",
            "price": 199.99,
            "category": "Beauty & Personal Care",
            "image_url": "https://images.unsplash.com/photo-1559591935-c6c92c6c2c6c?w=400",
            "stock_quantity": 73
        },
        {
            "name": "Foreo Luna 3 Facial Cleansing Brush",
            "description": "Silicone facial cleansing brush with T-Sonic technology",
            "price": 199.99,
            "category": "Beauty & Personal Care",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400",
            "stock_quantity": 45
        },
        {
            "name": "Philips Norelco Series 9000 Shaver",
            "description": "Electric shaver with V-Track Precision Blades",
            "price": 249.99,
            "category": "Beauty & Personal Care",
            "image_url": "https://images.unsplash.com/photo-1559591935-c6c92c6c2c6c?w=400",
            "stock_quantity": 31
        },
        {
            "name": "Clarisonic Mia Smart Facial Cleansing Device",
            "description": "Sonic facial cleansing brush with customizable cleansing modes",
            "price": 169.99,
            "category": "Beauty & Personal Care",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400",
            "stock_quantity": 52
        }
    ]
    
    added_count = 0
    for product_data in mock_products:
        try:
            # Check if product already exists by name
            existing = product_service.get_products(search=product_data["name"])
            if not existing:
                product_create = ProductCreate(**product_data)
                product_service.create_product(product_create)
                added_count += 1
                print(f"Added: {product_data['name']}")
            else:
                print(f"Skipped (already exists): {product_data['name']}")
        except Exception as e:
            print(f"Error adding {product_data['name']}: {e}")
    
    print(f"\nTotal products added: {added_count}")
    
    # Show final count
    final_products = product_service.get_products()
    print(f"Total products in database: {len(final_products)}")
    
    # Show products by category
    categories = {}
    for product in final_products:
        cat = product.category
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    print("\nProducts by category:")
    for category, count in categories.items():
        print(f"  {category}: {count} products")
    
    db.close()

if __name__ == "__main__":
    add_mock_products()
