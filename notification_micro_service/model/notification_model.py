class NotificationModel:
    def __init__(self, user_id=None, booking_code=None, message=None, contact_info=None):
        self.user_id = user_id
        self.booking_code = booking_code
        self.message = message
        self.contact_info = contact_info # Bisa email atau nomor telepon

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "booking_code": self.booking_code,
            "message": self.message,
            "contact_info": self.contact_info
        }