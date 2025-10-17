# model/activity_package_model.py
class ActivityPackageModel:
    def __init__(self, id=None, destination_id=None, name=None, description=None,  
                 price_per_person=None, duration_hours=None, requirements=None, 
                 image_url=None, created_at=None, updated_at=None):
        self.id = id
        self.destination_id = destination_id  # <-- Foreign Key ke tabel destinations
        self.name = name
        self.description = description
        self.price_per_person = price_per_person
        self.duration_hours = duration_hours
        self.requirements = requirements
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "description": self.description,
            "price_per_person": self.price_per_person,
            "duration_hours": self.duration_hours,
            "requirements": self.requirements,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<ActivityPackage {self.id}: {self.name}>"