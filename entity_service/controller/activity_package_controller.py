# controller/activity_package_controller.py
from flask import Blueprint, request, jsonify
from service.activity_package_service import ActivityPackageService

activity_bp = Blueprint('activity_packages', __name__)
activity_service = ActivityPackageService()

@activity_bp.route('/', methods=['GET'])
def get_all_activities():
    activities = activity_service.get_all()
    return jsonify([a.to_dict() for a in activities]), 200

@activity_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    activity = activity_service.get_by_id(activity_id)
    if activity:
        return jsonify(activity.to_dict()), 200
    return jsonify({"message": "Activity package not found"}), 404

@activity_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()
    if not data or not all(k in data for k in ['destinations_id', 'name', 'price']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    new_activity = activity_service.create(data)
    return jsonify(new_activity.to_dict()), 201

@activity_bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    data = request.get_json()
    if not data or not all(k in data for k in ['destinations_id', 'name', 'price']):
        return jsonify({"message": "Invalid input, required fields missing"}), 400
    updated_activity = activity_service.update(activity_id, data)
    if updated_activity:
        return jsonify(updated_activity.to_dict()), 200
    return jsonify({"message": "Activity package not found"}), 404

@activity_bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    if activity_service.delete(activity_id):
        return jsonify({"message": "Activity package deleted successfully"}), 200
    return jsonify({"message": "Activity package not found"}), 404