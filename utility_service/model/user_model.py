# model/user_model.py
class UserModel:
    def __init__(self, id=None, name=None, email=None, password=None, 
                 phone_number=None, role='customer', created_at=None, 
                 updated_at=None, deleted_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password # Di service, ini akan di-hash
        self.phone_number = phone_number
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        # JANGAN sertakan password dalam respons JSON
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"