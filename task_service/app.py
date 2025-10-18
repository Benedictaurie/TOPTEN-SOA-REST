import os
from flask import Flask
from flasgger import Swagger
from controller.booking_controller import booking_bp

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
app.register_blueprint(booking_bp, url_prefix='/api/bookings')

@app.route('/')
def home():
    return "<h1>Welcome to TOPTENBALITOUR Task Service</h1><p>Go to /docs/ for API documentation.</p>"

if __name__ == '__main__':
    app.run(port=8001, debug=True)