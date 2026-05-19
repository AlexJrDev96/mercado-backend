from src.config.data_base import db

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    quantity = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Boolean, nullable = False, default=True)
    image = db.Column(db.String(500), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "image": self.image,
            "user_id": self.user_id
        }