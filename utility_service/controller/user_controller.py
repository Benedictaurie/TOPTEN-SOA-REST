from flask import Blueprint, request, jsonify
from service.user_service import UserService

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    # ... logika register ...
    return jsonify({"message": "User created"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    # ... logika login, verifikasi password, generate token (JWT) ...
    # Misalkan login berhasil dan dapat user_id
    user_data = user_service.authenticate(request.get_json())
    if user_data:
        # Setelah login, user bisa melihat daftar paket.
        # Di aplikasi nyata, frontend akan memanggil entity service secara langsung.
        # Tapi sebagai contoh, kita bisa buat endpoint yang memanggilnya.
        return jsonify({
            "user": user_data,
            "message": "Login successful. You can now access packages at Entity Service."
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401