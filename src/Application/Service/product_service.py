from src.Domain.product import ProductDomain
from src.Domain.sale import SaleDomain
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.sale import Sale
from src.config.data_base import db
from datetime import datetime

class ProductService:
    def get_all_products(user_id):
        products = db.session.query(Product).filter(Product.user_id == user_id).all()
        return [ProductDomain(product.id, product.name, product.price, product.quantity, product.status, product.image, product.user_id)for product in products]
    
    @staticmethod
    def create_product(name, price, quantity, image, user_id):
        if db.session.query(Product).filter(Product.name == name, Product.user_id == user_id).first():
            return {"success": False, "message": "Já há um produto cadastrado com esse nome!"}
        
        product = Product(name=name, price=price, quantity=quantity, image=image, user_id=user_id)
        db.session.add(product)
        db.session.commit()
 
        product = ProductDomain(
            product.id, product.name, product.price, 
            product.quantity, product.status, product.image, product.user_id
        )

        return {
            "success": True,
            "produto": product
        }
    

    @staticmethod
    def update_product(product_id, data):
        product = db.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"success": False, "message": "Produto não encontrado!"}
        
        if 'name' in data:
            product.name = data['name']
        if 'image' in data:
            product.image = data['image']
        if 'price' in data:
            product.price = data['price']
            
        if 'quantity' in data:
            nova_quantidade = int(data['quantity'])
            product.quantity = nova_quantidade
            
            if nova_quantidade <= 0:
                product.status = False

        if 'status' in data:
            if product.quantity > 0:
                product.status = data['status']
            else:
                product.status = False

        try:
            db.session.commit()
            return {"success": True, "message": "Informações do produto atualizadas com sucesso."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao atualizar o banco de dados: {str(e)}"}
    