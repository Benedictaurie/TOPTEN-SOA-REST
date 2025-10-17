# model/rental_package_model.py

class RentalPackageModel:
    def __init__(self, id=None, name=None, description=None, price_per_day=None, availability_status=None, image_url=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.price_per_day = price_per_day
        self.availability_status = availability_status  # Bisa 'available', 'rented', 'maintenance'
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price_per_day": self.price_per_day,
            "availability_status": self.availability_status,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<RentalPackage {self.id}: {self.name}>"