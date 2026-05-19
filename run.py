import time
import os
from flask import Flask
from src.config.data_base import init_db
from src.routes import init_routes
from flask_cors import CORS
from src.Infrastructure.storage.image_storage import get_upload_folder

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    CORS(app)
    os.makedirs(get_upload_folder(), exist_ok=True)
    init_db(app)
    init_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)