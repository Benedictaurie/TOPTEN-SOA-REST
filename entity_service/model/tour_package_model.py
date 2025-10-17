# model/tour_package_model.py
class TourPackageModel:
    def __init__(self, id=None, destination_id=None, name=None, description=None, 
                 price=None, duration_days=None, image_url=None, is_available=True, 
                 created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.destination_id = destination_id #Foreign key dari tabel destinations
        self.name = name
        self.description = description
        self.price = float(price) if price else 0.0
        self.duration_days = duration_days
        self.image_url = image_url
        self.is_available = bool(is_available)
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "duration_days": self.duration_days,
            "image_url": self.image_url,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<TourPackage {self.id}: {self.name}>"