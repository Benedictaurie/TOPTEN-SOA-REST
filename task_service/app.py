#file ini untuk config blueprint booking entity
from flask import Flask
from controller.booking_controller import booking_bp

app = Flask(__name__)
app.register_blueprint(booking_bp, url_prefix='/api/bookings')

if __name__ == '__main__':
    print("Task Service running on port 8001")
    app.run(port=8001, debug=True)