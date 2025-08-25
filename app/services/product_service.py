from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_products(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        query = self.db.query(Product).filter(Product.is_active == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            search_filter = or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()

    def create_product(self, product: ProductCreate) -> Product:
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_product(self, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        db_product = self.get_product(product_id)
        if not db_product:
            return None

        update_data = product_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int) -> bool:
        db_product = self.get_product(product_id)
        if not db_product:
            return False

        self.db.delete(db_product)
        self.db.commit()
        return True

    def update_stock(self, product_id: int, quantity: int) -> bool:
        db_product = self.get_product(product_id)
        if not db_product:
            return False

        db_product.stock_quantity += quantity
        self.db.commit()
        return True
