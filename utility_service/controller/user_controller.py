# utility_service/controller/user_controller.py
from flask import Blueprint, request, jsonify
from service.user_service import UserService

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            password:
              type: string
            phone_number:
              type: string
    responses:
      201:
        description: User successfully created
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'email', 'password', 'phone_number']):
        return jsonify({"message": "Invalid input"}), 400

    new_user, message = user_service.register_user(data)
    if new_user:
        return jsonify(new_user.to_dict()), 201
    return jsonify({"message": message}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return an auth token.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful, returns auth token
    """
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({"message": "Email and password are required"}), 400

    user = user_service.authenticate_user(data['email'], data['password'])
    if user:
        auth_token = user_service.generate_auth_token(user.id, user.role)
        return jsonify({
            "user": user.to_dict(),
            "token": auth_token
        }), 200
    
    return jsonify({"message": "Invalid email or password"}), 401

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user details by ID (for internal service communication).
    ---
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
    responses:
      200:
        description: User details
    """
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404