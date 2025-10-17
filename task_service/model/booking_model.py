# model/booking_model.py

class BookingModel:
    def __init__(self, id=None, booking_code=None, user_id=None, package_id=None, 
                 booking_type=None, start_date=None, end_date=None, total_price=None, 
                 status='pending', created_at=None, updated_at=None):
        self.id = id
        self.booking_code = booking_code
        self.user_id = user_id  # ID dari user yang melakukan booking, Foreign Key
        self.package_id = package_id  # ID dari paket (tour, activity, atau rental)
        self.booking_type = booking_type # 'tour', 'activity', atau 'rental'
        self.start_date = start_date # Tanggal mulai perjalanan
        self.end_date = end_date #tanggal selesai perjalanan
        self.total_price = total_price
        self.status = status  # 'pending', 'verified', 'paid', 'completed', 'cancelled'
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "package_id": self.package_id,
            "package_type": self.package_type,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Booking {self.id} for User {self.user_id}>"