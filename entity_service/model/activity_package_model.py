class ActivityPackageModel:
    def __init__(self, id=None, destinations_id=None, name=None, description=None, 
                 price=None, image_url=None, is_available=True, 
                 created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.destinations_id = destinations_id # foreign key dari tabel destinasions
        self.name = name
        self.description = description
        self.price = float(price) if price else 0.0
        self.image_url = image_url
        self.is_available = bool(is_available)
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "destinations_id": self.destinations_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<ActivityPackage {self.id}: {self.name}>"