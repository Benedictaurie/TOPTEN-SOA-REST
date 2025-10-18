from flask import Flask
from flasgger import Swagger
from controller.destination_controller import destination_bp
from controller.tour_package_controller import tour_bp
from controller.activity_package_controller import activity_bp
from controller.rental_package_controller import rental_bp

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

# Daftarkan Blueprint dari setiap controller
app.register_blueprint(destination_bp, url_prefix='/api/destinations')
app.register_blueprint(tour_bp, url_prefix='/api/tour-packages')
app.register_blueprint(activity_bp, url_prefix='/api/activity-packages')
app.register_blueprint(rental_bp, url_prefix='/api/rental-packages')

@app.route('/')
def home():
    return "<h1>Welcome to TOPTENBALITOUR Entity Service</h1><p>Go to /docs/ for API documentation.</p>"

if __name__ == '__main__':
    app.run(port=8003, debug=True)