# model/destination_model.py
class DestinationModel:
    def __init__(self, id=None, name=None, description=None, location=None, 
                 image_url=None, created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Destination {self.id}: {self.name}>"