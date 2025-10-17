# controller/destination_controller.py
from flask import Blueprint, request, jsonify
from service.destination_service import DestinationService

destination_bp = Blueprint('destinations', __name__)
destination_service = DestinationService()

@destination_bp.route('/', methods=['GET'])
def get_all_destinations():
    """
    Get all destinations.
    ---
    responses:
      200:
        description: A list of destinations
    """
    destinations = destination_service.get_all()
    return jsonify([d.to_dict() for d in destinations]), 200

@destination_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination_by_id(destination_id):
    """Get a destination by its ID."""
    destination = destination_service.get_by_id(destination_id)
    if destination:
        return jsonify(destination.to_dict()), 200
    return jsonify({"message": "Destination not found"}), 404

# Tambahkan endpoint untuk create, update, delete di sini