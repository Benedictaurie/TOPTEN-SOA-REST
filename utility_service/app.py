import sys
import os
# menambahkan path root proyek ke sys.path agar bisa import modil config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY, UTILITY_SERVICE_URL #import dr config global
from flask import Flask
from flasgger import Swagger
from controller.user_controller import user_bp
from dotenv import load_dotenv

load_dotenv() # memuat variabel lingkungan dari file .env

app = Flask(__name__)

# Konfigurasi Flasgger (Swagger)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
Swagger(app, config=swagger_config)

# Daftarkan Blueprint dari controller
app.register_blueprint(user_bp, url_prefix='/api/users')

@app.route('/')
def home():
    return "<h1>Welcome to TOPTENBALITOUR Utility Service</h1><p>Go to /docs/ for API documentation.</p>"

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 8002))
    app.run(port=port, debug=True)