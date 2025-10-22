# from datetime import datetime
# import mysql.connector
# from config import DB_CONFIG

class BookingModel:
    def __init__(self, id=None, booking_code=None, user_id=None,
                 booking_type=None, tour_packages_id=None, activity_packages_id=None, 
                 rental_pacakges_id=None, start_date=None, end_date=None, num_persons=None, 
                 status=None, total_price=None, created_at=None, updated_at=None):
        self.id = id
        self.booking_code = booking_code
        self.user_id = user_id
        self.booking_type = booking_type # 'tour', 'activity', 'rental'
        self.tour_packages_id = tour_packages_id
        self.activity_packages_id = activity_packages_id
        self.rental_packages_id = rental_packages_id
        self.start_date = start_date
        self.end_date = end_date
        self.num_persons = num_persons
        self.status = status
        self.total_price = float(total_price) if total_price else 0.0
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "booking_code": self.booking_code,
            "user_id": self.user_id,
            "booking_type": self.booking_type,
            "tour_packages_id": self.tour_packages_id,
            "activity_packages_id": self.activity_packages_id,
            "rental_packages_id": self.rental_packages_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "num_persons": self.num_persons,
            "status": self.status,
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Booking {self.id}: {self.booking_code}>"