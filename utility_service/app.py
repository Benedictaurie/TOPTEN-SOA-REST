#file ini digunakan untuk konfigurasi Flask dan mendaftarkan Blueprint untuk user entity
from flask import Flask
from controller.user_controller import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == '__main__':
    print("Utility Service running on port 8002")
    app.run(port=8002, debug=True)