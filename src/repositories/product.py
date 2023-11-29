from src.models.product import Product
from sqlalchemy import func, cast, Float

class ProductRepository:

    def get_products_by_categories(self, categories):
        average_rating = Product.query.with_entities(cast(func.avg(Product.ratings), Float)).scalar()
        return Product.query.filter(Product.main_category.in_(categories), Product.ratings > average_rating).all()
