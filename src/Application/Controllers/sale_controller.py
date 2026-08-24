from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Application.Service.sale_service import SaleService

class SaleController:

    @staticmethod
    def get_all_vendas():
        token = request.headers.get('Authorization')
        
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)
        
        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)
        
        user_id = token_validation["user_id"]
        result = SaleService.get_all_vendas(user_id)
        
        if isinstance(result, dict) and result.get("success") is False:
            return make_response(jsonify({
                "erro": result["message"]
            }), 500)

        return make_response(jsonify({
            "mensagem": "Vendas encontradas com sucesso",
            "vendas": [venda.to_dict() for venda in result]
        }), 200)
    
    @staticmethod
    def create_venda():
        token = request.headers.get('Authorization')
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)
        
        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)
        
        user_id = token_validation["user_id"]
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity:
            return make_response(jsonify({"erro": "Dados incompletos (ID produto/Quantidade)"}), 400)

        result = SaleService.create_venda(user_id, product_id, quantity)

        if not result["success"]:
            return make_response(jsonify({"erro": result["message"]}), 400)

        sale_domain = result["venda"]

        return make_response(
            jsonify({
                "message": "Venda realizada com sucesso!",
                "venda": sale_domain.to_dict()
            }), 201
        )

    @staticmethod
    def update_status_sale():
        token = request.headers.get('Authorization')
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        user_id = token_validation["user_id"]
        data = request.get_json()

        if not data:
            return make_response(jsonify({"erro": "Dados para atualização não fornecidos"}), 400)

        sale_id = data.get('id')
        if not sale_id:
            return make_response(jsonify({"erro": "ID da venda não fornecido"}), 400)

        if 'status' not in data:
            return make_response(jsonify({"erro": "Status não fornecido"}), 400)

        result = SaleService.update_status(sale_id, user_id, data.get('status'))

        if result["success"]:
            return make_response(jsonify({"mensagem": result["message"]}), 200)
        return make_response(jsonify({"erro": result["message"]}), 400)
