from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.product import Product
from src.Domain.sale import SaleDomain
from src.Application.Service.product_service import ProductService
from src.config.data_base import db
import random

class SaleService:

    @staticmethod
    def generate_order_code():
        numero = random.randint(1000, 9999)
        return f"P-{numero}"

    @staticmethod
    def create_venda(user_id, itens):
        try:
            # 1. Prepara os dados para o motor de estoque
            itens_venda = {}
            for item in itens:
                product_id = item.get('product_id')
                qtd = item.get('quantity')
                if not product_id or not qtd:
                    return {"success": False, "message": "Dados incompletos nos itens da venda (necessário product_id e quantity)."}
                itens_venda[product_id] = qtd
            
            # 2. CHAMA O MOTOR DE ESTOQUE EM LOTE
            resultado_estoque = ProductService.subtract_stock_batch(user_id, itens_venda)
            if not resultado_estoque["success"]:
                return resultado_estoque 

            # A função de estoque já nos devolve os produtos atualizados, vamos usá-los!
            produtos_atualizados = resultado_estoque["products"]
            mapa_produtos = {p.id: p for p in produtos_atualizados}

            # 3. Gera um único código de pedido para o lote inteiro
            codigo_pedido = SaleService.generate_order_code()
            sales_criadas = []
            sales_domains = []

            # 4. Salva o registro de venda (Sale) para cada item do pedido
            for item in itens:
                product_id = item.get('product_id')
                qtd = item.get('quantity')
                produto = mapa_produtos[product_id]

                total_price = float(produto.price) * qtd

                sale = Sale(
                    order_number=codigo_pedido,
                    product_id=produto.id,
                    product_name=produto.name,
                    quantity=qtd,
                    price=produto.price,
                    total_price=total_price,
                    user_id=user_id
                )
                db.session.add(sale)
                sales_criadas.append(sale)
            
            # Salva tudo no banco de uma vez só!
            db.session.commit()

            # 5. Formata os dados para retornar à API
            for sale in sales_criadas:
                sales_domains.append(SaleDomain(
                    sale.id, sale.order_number, sale.product_id, sale.product_name,
                    sale.quantity, sale.price, sale.total_price, sale.user_id, sale.status, sale.created_at
                ))

            return {
                "success": True,
                "message": f"Pedido {codigo_pedido} realizado com sucesso com {len(itens)} item(ns)!",
                "vendas": sales_domains
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao registrar pedido: {str(e)}"}

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

        # Verifica se estamos inativando uma venda que estava ativa
        status_inativo = (status == "inativa" or status == False)
        venda_era_ativa = (sale.status != "inativa" and sale.status != False)

        if status_inativo and venda_era_ativa:
            # Cria um dicionário simulando um lote de 1 item
            itens_para_devolver = {sale.product_id: sale.quantity}
            
            # Devolve ao estoque com segurança
            resultado_estoque = ProductService.add_stock_batch(user_id, itens_para_devolver)
            if not resultado_estoque["success"]:
                return {"success": False, "message": "Erro ao devolver itens ao estoque."}

        sale.status = status

        try:
            db.session.commit()
            return {"success": True, "message": "Status da venda atualizado com sucesso."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao atualizar o banco de dados: {str(e)}"}
