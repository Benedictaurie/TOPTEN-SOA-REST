# controller/tour_package_controller.py
from flask import Blueprint, request, jsonify
from service.tour_package_service import TourPackageService

tour_bp = Blueprint('tour_packages', __name__)
tour_service = TourPackageService()

@tour_bp.route('/', methods=['GET'])
def get_all_tours():
    tours = tour_service.get_all()
    return jsonify([t.to_dict() for t in tours]), 200

@tour_bp.route('/<int:tour_id>', methods=['GET'])
def get_tour_by_id(tour_id):
    tour = tour_service.get_by_id(tour_id)
    if tour:
        return jsonify(tour.to_dict()), 200
    return jsonify({"message": "Tour package not found"}), 404

@tour_bp.route('/', methods=['POST'])
def create_tour():
    data = request.get_json()
    if not data or not all(k in data for k in ['destination_id', 'name', 'price']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    new_tour = tour_service.create(data)
    return jsonify(new_tour.to_dict()), 201

@tour_bp.route('/<int:tour_id>', methods=['PUT'])
def update_tour(tour_id):
    data = request.get_json()
    if not data or not all(k in data for k in ['destination_id', 'name', 'price']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    updated_tour = tour_service.update(tour_id, data)
    if updated_tour:
        return jsonify(updated_tour.to_dict()), 200
    return jsonify({"message": "Tour package not found"}), 404

@tour_bp.route('/<int:tour_id>', methods=['DELETE'])
def delete_tour(tour_id):
    if tour_service.delete(tour_id):
        return jsonify({"message": "Tour package deleted successfully"}), 200
    return jsonify({"message": "Tour package not found"}), 404