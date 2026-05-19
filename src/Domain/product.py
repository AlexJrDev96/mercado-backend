class ProductDomain:
    def __init__(self, id, name, price, quantity, status, image, user_id):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.image = image
        self.user_id = user_id
        
        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price) if self.price is not None else 0.0,
            "quantity": self.quantity,
            "status": self.status,
            "image": self.image,
            "user_id": self.user_id
        }