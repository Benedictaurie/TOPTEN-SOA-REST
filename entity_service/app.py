#file ini untuk configurasi Flask app dan mendaftarkan Blueprint untuk setiap entitas
from flask import Flask
from controller.tour_package_controller import tour_bp
from controller.activity_package_controller import activity_bp
from controller.rental_package_controller import rental_bp
from controller.destination_controller import destination_bp

app = Flask(__name__)

# Mendaftarkan Blueprint untuk setiap entitas
app.register_blueprint(tour_bp, url_prefix='/api/tours')
app.register_blueprint(activity_bp, url_prefix='/api/activities')
app.register_blueprint(rental_bp, url_prefix='/api/rentals')
app.register_blueprint(destination_bp, url_prefix='/api/destinations')


if __name__ == '__main__':
    print("Entity Service running on port 8003")
    app.run(port=8003, debug=True)