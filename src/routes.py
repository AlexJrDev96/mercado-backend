from src.Application.Controllers.sale_controller import SaleController
from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.product_controller import ProductController
from flask import jsonify, make_response, send_from_directory
from src.Infrastructure.storage.image_storage import get_upload_folder

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/users', methods=['GET'])
    def get_all_users():
        return UserController.get_all_users()
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/user/activate', methods=['POST'])
    def activate_user():
        return UserController.activate_user()

    @app.route('/login', methods=["POST"])
    def login():
        return UserController.login()
    
    @app.route('/user', methods=['GET'])
    def get_user():
        return UserController.get_user()
    
    @app.route('/user', methods=['PUT'])
    def update_user():
        return UserController.update_user()
    
    @app.route('/product', methods=['GET'])
    def get_all_products():
        return ProductController.get_all_products()
    
    @app.route('/product', methods=['POST'])
    def create_product():
        return ProductController.create_product()

    @app.route('/product/upload', methods=['POST'])
    def upload_product_image():
        return ProductController.upload_image()

    @app.route('/uploads/<path:filename>')
    def serve_product_image(filename):
        return send_from_directory(get_upload_folder(), filename)
    
    @app.route('/product', methods=['PUT'])
    def update_product():
        return ProductController.update_product()
    
    @app.route('/product/status', methods=['PUT'])
    def update_status_product():
        return ProductController.update_status_product()
    @app.route('/venda', methods=['POST'])
    def create_venda():
        return SaleController.create_venda()
    
    @app.route('/venda', methods=['GET'])
    def get_all_vendas():
        return SaleController.get_all_vendas()