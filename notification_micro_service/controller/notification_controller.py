from flask import Blueprint, request, jsonify
from service.notification_service import NotificationService

notification_bp = Blueprint('notifications', __name__)
notification_service = NotificationService()

@notification_bp.route('/send-confirmation', methods=['POST'])
def send_confirmation():
    """
    Endpoint untuk memicu notifikasi konfirmasi booking.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
            booking_code:
              type: string
    responses:
      200:
        description: Notification sent successfully
    """
    data = request.get_json()
    if not data or not 'user_id' in data or not 'booking_code' in data:
        return jsonify({"message": "Invalid input, user_id and booking_code are required"}), 400

    success = notification_service.send_booking_confirmation(data['user_id'], data['booking_code'])
    
    if success:
        return jsonify({"message": "Booking confirmation notification sent successfully."}), 200
    else:
        return jsonify({"message": "Failed to send notification."}), 500

@notification_bp.route('/send-reminder', methods=['POST'])
def send_reminder():
    """Endpoint untuk memicu notifikasi pengingat pembayaran."""
    data = request.get_json()
    if not data or not 'user_id' in data or not 'booking_code' in data:
        return jsonify({"message": "Invalid input"}), 400
        
    success = notification_service.send_payment_reminder(data['user_id'], data['booking_code'])
    
    if success:
        return jsonify({"message": "Payment reminder notification sent successfully."}), 200
    else:
        return jsonify({"message": "Failed to send notification."}), 500

@notification_bp.route('/send-verified', methods=['POST'])
def send_verified():
    """Endpoint untuk memicu notifikasi booking sudah diverifikasi."""
    data = request.get_json()
    if not data or not 'user_id' in data or not 'booking_code' in data:
        return jsonify({"message": "Invalid input"}), 400

    success = notification_service.send_booking_verified_notification(data['user_id'], data['booking_code'])
    
    if success:
        return jsonify({"message": "Booking verified notification sent successfully."}), 200
    else:
        return jsonify({"message": "Failed to send notification."}), 500