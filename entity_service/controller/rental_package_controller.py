# controller/rental_package_controller.py
from flask import Blueprint, request, jsonify
from service.rental_package_service import RentalPackageService

rental_bp = Blueprint('rental_packages', __name__)
rental_service = RentalPackageService()

@rental_bp.route('/', methods=['GET'])
def get_all_rentals():
    rentals = rental_service.get_all()
    return jsonify([r.to_dict() for r in rentals]), 200

@rental_bp.route('/<int:rental_id>', methods=['GET'])
def get_rental_by_id(rental_id):
    rental = rental_service.get_by_id(rental_id)
    if rental:
        return jsonify(rental.to_dict()), 200
    return jsonify({"message": "Rental package not found"}), 404

@rental_bp.route('/', methods=['POST'])
def create_rental():
    data = request.get_json()
    if not data or not all(k in data for k in ['type', 'brand', 'model', 'plate_number', 'price_per_day']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    new_rental = rental_service.create(data)
    return jsonify(new_rental.to_dict()), 201

@rental_bp.route('/<int:rental_id>', methods=['PUT'])
def update_rental(rental_id):
    data = request.get_json()
    if not data or not all(k in data for k in ['type', 'brand', 'model', 'plate_number', 'price_per_day']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    updated_rental = rental_service.update(rental_id, data)
    if updated_rental:
        return jsonify(updated_rental.to_dict()), 200
    return jsonify({"message": "Rental package not found"}), 404

@rental_bp.route('/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    if rental_service.delete(rental_id):
        return jsonify({"message": "Rental package deleted successfully"}), 200
    return jsonify({"message": "Rental package not found"}), 404