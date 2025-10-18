from flask import Flask
from controller.tour_package_controller import tour_bp
from controller.activity_package_controller import activity_bp
from controller.rental_package_controller import rental_bp
from controller.destination_controller import destination_bp

app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
Swagger(app, config=swagger_config)

app.register_blueprint(destination_bp, url_prefix='/api/destinations')
# Daftarkan blueprint lainnya
# app.register_blueprint(tour_bp, url_prefix='/api/tour-packages')

if __name__ == '__main__':
    print("Entity Service running on port 8003")
    app.run(port=8003, debug=True)