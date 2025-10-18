import os
from dotenv import load_dotenv
import requests # Akan digunakan untuk memanggil utility service

load_dotenv()

# URL layanan lain untuk mendapatkan data pengguna
UTILITY_SERVICE_URL = os.getenv("UTILITY_SERVICE_URL", "http://localhost:8002")

class NotificationService:
    def __init__(self):
        # Di sini bisa inisialisasi klien email/SMS gateway
        pass

    def _get_user_details(self, user_id):
        """Helper method untuk mengambil detail user dari Utility Service."""
        try:
            # Asumsikan ada endpoint di utility service untuk mendapatkan user by ID
            response = requests.get(f"{UTILITY_SERVICE_URL}/api/users/{user_id}")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user details: {e}")
        return None

    def send_booking_confirmation(self, user_id, booking_code):
        """
        Mengirim notifikasi konfirmasi booking.
        """
        # 1. Ambil detail user (termasuk email/nomor telepon)
        user_details = self._get_user_details(user_id)
        if not user_details:
            print(f"Failed to send notification. User with ID {user_id} not found.")
            return False

        user_email = user_details.get('email')
        user_name = user_details.get('name')

        # 2. Buat pesan notifikasi
        subject = "Booking Confirmation - TOPTEN BALI TOUR"
        message = f"""
        Dear {user_name},

        Your booking with code {booking_code} has been successfully created and is now pending payment.

        Please complete the payment to confirm your booking.

        Thank you,
        TOPTEN BALI TOUR Team
        """

        # 3. KIRIM NOTIFIKASI (SIMULASI)
        # Di dunia nyata, di sinilah Anda memanggil library email seperti SMTP atau API pihak ketiga.
        print("--- SENDING NOTIFICATION ---")
        print(f"To: {user_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message.strip()}")
        print("--- NOTIFICATION SENT ---")
        
        return True

    def send_payment_reminder(self, user_id, booking_code):
        """
        Mengirim notifikasi pengingat pembayaran.
        """
        user_details = self._get_user_details(user_id)
        if not user_details:
            return False

            
        user_email = user_details.get('email')
        user_name = user_details.get('name')

        subject = "Payment Reminder - TOPTEN BALI TOUR"
        message = f"""
        Dear {user_name},

        This is a friendly reminder for your booking with code {booking_code}.
        The payment is still pending. Please complete it soon to avoid cancellation.

        Thank you,
        TOPTEN BALI TOUR Team
        """
        
        print("--- SENDING NOTIFICATION ---")
        print(f"To: {user_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message.strip()}")
        print("--- NOTIFICATION SENT ---")
        
        return True

    def send_booking_verified_notification(self, user_id, booking_code):
        """
        Mengirim notifikasi bahwa booking telah diverifikasi (sudah dibayar).
        """
        user_details = self._get_user_details(user_id)
        if not user_details:
            return False

        user_email = user_details.get('email')
        user_name = user_details.get('name')

        subject = "Booking Verified - TOPTEN BALI TOUR"
        message = f"""
        Dear {user_name},

        Great news! Your booking with code {booking_code} has been verified and confirmed.
        We are looking forward to seeing you on your tour date.

        Thank you,
        TOPTEN BALI TOUR Team
        """

        print("--- SENDING NOTIFICATION ---")
        print(f"To: {user_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message.strip()}")
        print("--- NOTIFICATION SENT ---")
        
        return True