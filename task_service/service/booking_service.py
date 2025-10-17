import requests
from model.booking_model import BookingModel

# URL layanan lainnya
UTILITY_SERVICE_URL = "http://localhost:8002/api/users"
ENTITY_SERVICE_URL = "http://localhost:8003/api"
NOTIFICATION_SERVICE_URL = "http://localhost:8004/api/notify"

class BookingService:
    def create_booking(self, user_id, package_id, package_type):
        # 1. Verifikasi user dengan memanggil Utility Service
        try:
            # Asumsikan ada endpoint untuk verifikasi token/user
            response = requests.get(f"{UTILITY_SERVICE_URL}/{user_id}", headers={"Authorization": "Bearer <user_token>"})
            if response.status_code != 200:
                return None, "User not found or invalid token."
        except requests.exceptions.RequestException:
            return None, "Utility service is unavailable."

        # 2. Cek ketersediaan paket dengan memanggil Entity Service
        try:
            entity_url = f"{ENTITY_SERVICE_URL}/{package_type}s/{package_id}"
            response = requests.get(entity_url)
            if response.status_code != 200:
                return None, "Package not found."
            package_data = response.json()
            # Di sini bisa ada logika cek ketersediaan kuota, tanggal, dll.
        except requests.exceptions.RequestException:
            return None, "Entity service is unavailable."

        # 3. Jika semua valid, buat booking di database Task Service
        # ... (logika insert ke tabel bookings) ...
        new_booking = BookingModel(user_id=user_id, package_id=package_id, package_type=package_type, status="confirmed")
        
        # 4. Panggil Notification Service untuk mengirim notifikasi
        try:
            notification_payload = {
                "user_id": user_id,
                "message": f"Your booking for {package_data['name']} is being processed."
            }
            requests.post(NOTIFICATION_SERVICE_URL, json=notification_payload)
        except requests.exceptions.RequestException:
            # Log error, tapi tidak gagalkan proses booking
            print("Failed to send notification.")

        return new_booking, "Booking created successfully."