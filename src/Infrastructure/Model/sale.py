from src.config.data_base import db
from datetime import datetime

class Sale(db.Model):
    __tablename__='sales'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(10), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": float(self.price) if self.price is not None else 0.0,
            "total_price": float(self.total_price) if self.total_price is not None else 0.0,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
