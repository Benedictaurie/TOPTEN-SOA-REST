import os
import requests
import jwt
import mysql.connector
import uuid
from datetime import datetime
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, UTILITY_SERVICE_URL, ENTITY_SERVICE_URL, NOTIFICATION_SERVICE_URL, SECRET_KEY
from model.booking_model import BookingModel

class BookingService:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def _verify_user(self, token):
        """Memverifikasi token JWT dan mengembalikan user_id."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def _get_package_details(self, package_type, package_id):
        """Mengambil detail paket dari Entity Service."""
        try:
            if package_type == 'tour':
                response = requests.get(f"{ENTITY_SERVICE_URL}/api/tour-packages/{package_id}")
            elif package_type == 'activity':
                response = requests.get(f"{ENTITY_SERVICE_URL}/api/activity-packages/{package_id}")
            elif package_type == 'rental':
                response = requests.get(f"{ENTITY_SERVICE_URL}/api/rental-packages/{package_id}")
            else:
                return None, "Invalid package type"
            
            if response.status_code == 200:
                return response.json(), None
            return None, "Package not found"
        except requests.exceptions.RequestException:
            return None, "Entity service is unavailable"

    def _trigger_notification(self, endpoint, user_id, booking_code):
        """Memanggil Notification Service untuk mengirim notifikasi."""
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/api/notify/{endpoint}", json={
                "user_id": user_id,
                "booking_code": booking_code
            })
        except requests.exceptions.RequestException as e:
            print(f"Failed to trigger notification: {e}")

    def create_booking(self, token, booking_data):
        """
        Proses lengkap membuat booking:
        1. Verifikasi user dari token.
        2. Ambil detail paket dari Entity Service.
        3. Hitung total harga.
        4. Simpan booking ke database.
        5. Trigger notifikasi.
        """
        # 1. Verifikasi User
        user_id = self._verify_user(token)
        if not user_id:
            return None, "Invalid or expired token"

        # 2. Ambil Detail Paket
        package_type = booking_data['booking_type']
        package_id = booking_data[f'{package_type}_packages_id']
        package_details, error = self._get_package_details(package_type, package_id)
        if error:
            return None, error
        
        package_price = package_details['price']
        
        # 3. Hitung Total Harga
        num_persons = booking_data.get('num_persons', 1)
        total_price = package_price * num_persons

        # 4. Simpan ke Database
        if not self.connection:
            return None, "Database connection failed"
        
        cursor = self.connection.cursor()
        booking_code = f"TOPTEN-{uuid.uuid4().hex[:8].upper()}"
        
        query = """
            INSERT INTO bookings (booking_code, user_id, 
            booking_type, tour_packages_id, activity_packages_id, 
            rental_packages_id, start_date, end_date, num_persons, total_price, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            booking_code, user_id, package_type,
            booking_data.get('tour_packages_id'),
            booking_data.get('activity_packages_id'),
            booking_data.get('rental_packages_id'),
            booking_data['start_date'],
            booking_data['end_date'],
            num_persons,
            total_price,
            'pending'
        )
        cursor.execute(query, values)
        self.connection.commit()
        new_booking_id = cursor.lastrowid
        cursor.close()

        # 5. Trigger Notifikasi (asinkron, tidak perlu menunggu)
        self._trigger_notification("send-confirmation", user_id, booking_code)

        # Kembalikan booking yang baru dibuat
        return self.get_booking_by_id(new_booking_id), "Booking created successfully"

    def get_booking_by_id(self, booking_id):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE id = %s"
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return BookingModel(**result)
        return None

    def update_booking_status(self, booking_id, new_status):
        """Memperbarui status booking dan memicu notifikasi yang sesuai."""
        if not self.connection:
            return None, "Database connection failed"
        
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return None, "Booking not found"

        cursor = self.connection.cursor()
        query = "UPDATE bookings SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (new_status, booking_id))
        self.connection.commit()
        cursor.close()

        # Trigger notifikasi berdasarkan status baru
        if new_status == 'verified':
            self._trigger_notification("send-verified", booking.user_id, booking.booking_code)
        
        return self.get_booking_by_id(booking_id), f"Booking status updated to {new_status}"