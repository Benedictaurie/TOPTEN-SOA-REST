import os
import jwt
from flask import Blueprint, request, jsonify, g
from functools import wraps 
from service.booking_service import BookingService

booking_bp = Blueprint('bookings', __name__)
booking_service = BookingService()

# Middleware untuk memeriksa token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1] # bearer token
            except IndexError:
                return jsonify({"message": "Token is malformed!"}), 401
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            # Memastikan SECRET_KEY diambil dari config
            from config import SECRET_KEY
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # simpan user info di g (app context)
            g.user_id = decoded_token.get('user_id')
            g.user_role = decoded_token.get('role')

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(*args, **kwargs)
    return decorated

@booking_bp.route('/', methods=['POST'])
@token_required
def create_booking():
    """
    Create a new booking.
    ---
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        description: "Bearer <token>"
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            booking_type:
              type: string
              enum: [tour, activity, rental]
            tour_packages_id:
              type: integer
            activity_packages_id:
              type: integer
            rental_packages_id:
              type: integer
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
            num_persons:
              type: integer
    responses:
      201:
        description: Booking created successfully
    """
    data = request.get_json()
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1]

    #Decode token untuk mendaptkan user info
    from config import SECRET_KEY
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = g.user_id
    
    new_booking, message = booking_service.create_booking(token, data)
    
    if new_booking:
        return jsonify(new_booking.to_dict()), 201
    return jsonify({"message": message}), 400

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@token_required
def get_booking(booking_id):
    """Get a specific booking by its ID."""
    booking = booking_service.get_booking_by_id(booking_id)
    if booking:
        return jsonify(booking.to_dict()), 200
    return jsonify({"message": "Booking not found"}), 404

@booking_bp.route('/<int:booking_id>/status', methods=['PUT'])
@token_required
def update_booking_status(booking_id):
    """Update the status of a booking (e.g., from 'pending' to 'verified')."""
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"message": "Status is required"}), 400
        
    updated_booking, message = booking_service.update_booking_status(booking_id, data['status'])
    
    if updated_booking:
        return jsonify(updated_booking.to_dict()), 200
    return jsonify({"message": message}), 400