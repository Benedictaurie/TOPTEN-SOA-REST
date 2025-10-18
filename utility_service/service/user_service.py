import os
import jwt
import mysql.connector
from datetime import datetime, timedelta
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from model.user_model import UserModel

class UserService:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None
        # Kunci rahasia untuk JWT. HARUS DIJAGA KERAHASIAANNYA.
        # Di production, simpan di environment variable yang benar-benar aman.
        self.SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_changed")

    def get_user_by_email(self, email):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s AND deleted_at IS NULL"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return UserModel(**result)
        return None

    def get_user_by_id(self, user_id):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s AND deleted_at IS NULL"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return UserModel(**result)
        return None

    def register_user(self, data):
        if not self.connection:
            return None, "Database connection failed"
        
        # Cek apakah email sudah terdaftar
        if self.get_user_by_email(data['email']):
            return None, "Email already registered"

        # Buat objek user baru
        new_user = UserModel(
            name=data['name'],
            email=data['email'],
            phone_number=data.get('phone_number'),
            role=data.get('role', 'customer')
        )
        # Hash password sebelum disimpan
        new_user.hash_password(data['password'])

        # Simpan ke database
        cursor = self.connection.cursor()
        query = """
            INSERT INTO users (name, email, password, phone_number, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (new_user.name, new_user.email, new_user.password, new_user.phone_number, new_user.role))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        # Kembalikan user yang baru dibuat (tanpa password)
        return self.get_user_by_id(new_id), "User created successfully"

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    def generate_auth_token(self, user_id, user_role):
        """Generate JWT token."""
        payload = {
            'user_id': user_id,
            'role': user_role,
            'exp': datetime.utcnow() + timedelta(hours=24) # Token berlaku 24 jam
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token