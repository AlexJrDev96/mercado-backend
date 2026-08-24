from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.product import Product
from src.Domain.sale import SaleDomain
from src.config.data_base import db
import random

class SaleService:

    @staticmethod
    def generate_order_code():
        numero = random.randint(1000, 9999)
        return f"P-{numero}"

    @staticmethod
    def create_venda(user_id, product_id, quantity):
        try:
            product = db.session.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
            
            if not product:
                return {"success": False, "message": "Produto não encontrado!"}
            
            if product.quantity < quantity:
                return {"success": False, "message": f"Quantidade insuficiente! Disponível: {product.quantity}"}
            
            if product.status == False:
                return {"success": False, "message": "Produto indisponível!"}
            
            total_price = float(product.price) * quantity
            
            codigo_pedido = SaleService.generate_order_code()

            sale = Sale(
                order_number=codigo_pedido,
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                price=product.price,
                total_price=total_price,
                user_id=user_id
            )
            
            product.quantity -= quantity
            if product.quantity <= 0:
                product.status = False
            
            db.session.add(sale)
            db.session.commit()
            
            sale_domain = SaleDomain(
                sale.id,
                sale.order_number,
                sale.product_id,
                sale.product_name,
                sale.quantity,
                sale.price,
                sale.total_price,
                sale.user_id,
                sale.status,
                sale.created_at
            )

            return {
                "success": True,
                "message": f"Venda {codigo_pedido} realizada com sucesso! Produto: {product.name}, Quantidade: {quantity}",
                "venda": sale_domain
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao registrar venda: {str(e)}"}

    @staticmethod
    def get_all_vendas(user_id):
        try:
            sales = db.session.query(Sale).filter(Sale.user_id == user_id).all()
            return [SaleDomain(
                sale.id,
                sale.order_number,
                sale.product_id,
                sale.product_name,
                sale.quantity,
                sale.price,
                sale.total_price,
                sale.user_id,
                sale.status,
                sale.created_at
            ) for sale in sales]
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar vendas: {str(e)}"}

    @staticmethod
    def update_status(sale_id, user_id, status):
        sale = db.session.query(Sale).filter(Sale.id == sale_id, Sale.user_id == user_id).first()
        if not sale:
            return {"success": False, "message": "Venda não encontrada!"}

        sale.status = status

        try:
            db.session.commit()
            return {"success": True, "message": "Status da venda atualizado com sucesso."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao atualizar o banco de dados: {str(e)}"}
