# model/rental_package_model.py

class RentalPackageModel:
    def __init__(self, id=None, type=None, brand=None, model=None, plate_number=None,
                 description=None, image_url=None, price_per_day=None, is_available=True, 
                 created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.type = type
        self.brand = brand
        self.model = model
        self.plate_number = plate_number
        self.description = description
        self.image_url = image_url
        self.price_per_day = price_per_day
        self.is_available = bool(is_available)  # Bisa 'available', 'rented', 'maintenance'
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "brand": self.brand,
            "model": self.model,
            "plate_number":self.plate_number,
            "description": self.description,
            "image_url": self.image_url,
            "price_per_day": self.price_per_day,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<RentalPackage {self.id}: {self.name}>"