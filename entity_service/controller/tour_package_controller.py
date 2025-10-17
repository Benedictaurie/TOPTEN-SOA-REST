from flask import Blueprint, request, jsonify
from service.tour_package_service import TourPackageService

tour_bp = Blueprint('tours', __name__)
tour_service = TourPackageService()

# Endpoint untuk melihat daftar paket (bisa diakses siapa saja)
@tour_bp.route('/', methods=['GET'])
def get_all_tours():
    tours = tour_service.get_all()
    return jsonify([t.to_dict() for t in tours]), 200

# Endpoint untuk menambah paket (hanya untuk admin, bisa ditambahkan validasi token admin)
@tour_bp.route('/', methods=['POST'])
def create_tour():
    data = request.get_json()
    new_tour = tour_service.create(data)
    return jsonify(new_tour.to_dict()), 201

# Endpoint untuk melihat detail paket
@tour_bp.route('/<int:tour_id>', methods=['GET'])
def get_tour_by_id(tour_id):
    tour = tour_service.get_by_id(tour_id)
    if not tour:
        return jsonify({"message": "Tour not found"}), 404
    return jsonify(tour.to_dict()), 200

# ... endpoint lain untuk update dan delete (untuk admin)