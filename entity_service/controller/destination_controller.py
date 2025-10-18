from flask import Blueprint, request, jsonify
from service.destination_service import DestinationService

destination_bp = Blueprint('destinations', __name__)
destination_service = DestinationService()

@destination_bp.route('/', methods=['GET'])
def get_all_destinations():
    destinations = destination_service.get_all()
    return jsonify([d.to_dict() for d in destinations]), 200

@destination_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination_by_id(destination_id):
    destination = destination_service.get_by_id(destination_id)
    if destination:
        return jsonify(destination.to_dict()), 200
    return jsonify({"message": "Destination not found"}), 404

@destination_bp.route('/', methods=['POST'])
def create_destination():
    data = request.get_json()
    if not data or not 'name' in data:
        return jsonify({"message": "Invalid input"}), 400
    new_destination = destination_service.create(data)
    return jsonify(new_destination.to_dict()), 201

@destination_bp.route('/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.get_json()
    if not data or not 'name' in data:
        return jsonify({"message": "Invalid input"}), 400
    updated_destination = destination_service.update(destination_id, data)
    if updated_destination:
        return jsonify(updated_destination.to_dict()), 200
    return jsonify({"message": "Destination not found"}), 404

@destination_bp.route('/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    if destination_service.delete(destination_id):
        return jsonify({"message": "Destination deleted successfully"}), 200
    return jsonify({"message": "Destination not found"}), 404