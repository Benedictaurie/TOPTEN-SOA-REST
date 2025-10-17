# model/user_model.py
class UserModel:
    def __init__(self, id=None, name=None, email=None, phone_number=None, password_hash=None, full_name=None, role='customer', created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        # Jangan sertakan password_hash dalam respons JSON!
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
        return f"<User {self.id}: {self.username}>"