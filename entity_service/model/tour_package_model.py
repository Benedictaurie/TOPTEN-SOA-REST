# model/tour_package_model.py

class TourPackageModel:
    def __init__(self, id=None, destination_id= None, name=None, description=None, 
                 duration_days=None, duration_nights=None, price=None, 
                 image_url=None, created_at=None, updated_at=None):
        """
        Model untuk data paket tour.
        """
        self.id = id
        self.destination_id = destination_id #ID foreign key dari DestinationModel
        self.name = name
        self.description = description
        self.duration_days = duration_days
        self.duration_nights = duration_nights
        self.price = price
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        """
        Mengubah objek model menjadi dictionary.
        Ini berguna untuk konversi ke JSON saat memberikan respons API.
        """
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "description": self.description,
            "duration_days": self.duration_days,
            "duration_nights": self.duration_nights,
            "price": self.price,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None, # Konversi datetime ke string ISO
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        """
        Representasi string dari objek, berguna untuk debugging.
        """
        return f"<TourPackage {self.id}: {self.name}>"