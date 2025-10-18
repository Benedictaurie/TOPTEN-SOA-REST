# service/rental_package_service.py
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from model.rental_package_model import RentalPackageModel

class RentalPackageService:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.connection.is_connected():
                print("Successfully connected to the database (Rental Package Service)")
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    # CRUD Operations
    def get_all(self):
        if not self.connection:
            return []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rental_packages WHERE deleted_at IS NULL")
        results = cursor.fetchall()
        cursor.close()
        return [RentalPackageModel(**result) for result in results]

    def get_by_id(self, package_id):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM rental_packages WHERE id = %s AND deleted_at IS NULL"
        cursor.execute(query, (package_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return RentalPackageModel(**result)
        return None

    def create(self, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            INSERT INTO rental_packages (type, brand, model, plate_number, description, price_per_day, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['type'], data['brand'], data['model'], data['plate_number'], data['description'], data['price_per_day'], data['image_url']))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return self.get_by_id(new_id)

    def update(self, package_id, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            UPDATE rental_packages SET type = %s, brand = %s, model = %s, plate_number = %s, description = %s, price_per_day = %s, image_url = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data['type'], data['brand'], data['model'], data['plate_number'], data['description'], data['price_per_day'], data['image_url'], package_id))
        self.connection.commit()
        cursor.close()
        return self.get_by_id(package_id)

    def delete(self, package_id):
        if not self.connection:
            return False
        cursor = self.connection.cursor()
        query = "UPDATE rental_packages SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (package_id,))
        self.connection.commit()
        cursor.close()
        return cursor.rowcount > 0