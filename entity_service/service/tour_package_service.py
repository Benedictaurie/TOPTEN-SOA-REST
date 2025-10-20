import mysql.connector
from config import DB_HOST, DB_USER, DB_PORT, DB_PASSWORD, DB_NAME
from model.tour_package_model import TourPackageModel

class TourPackageService:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                port=DB_PORT,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.connection.is_connected():
                print("Successfully connected to the database (Tour Package Service)")
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    # CRUD Operations 
    def get_all(self):
        if not self.connection:
            return []
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT tp.*, d.name as destination_name 
            FROM tour_packages tp 
            JOIN destinations d ON tp.destination_id = d.id 
            WHERE tp.deleted_at IS NULL
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return [TourPackageModel(**result) for result in results]

    def get_by_id(self, package_id):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT tp.*, d.name as destination_name 
            FROM tour_packages tp 
            JOIN destinations d ON tp.destination_id = d.id 
            WHERE tp.id = %s AND tp.deleted_at IS NULL
        """
        cursor.execute(query, (package_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return TourPackageModel(**result)
        return None

    def create(self, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            INSERT INTO tour_packages (destination_id, name, description, price, duration_days, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['destination_id'], data['name'], data['description'], data['price'], data.get('duration_days'), data['image_url']))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return self.get_by_id(new_id)

    def update(self, package_id, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            UPDATE tour_packages SET destination_id = %s, name = %s, description = %s, price = %s, duration_days = %s, image_url = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data['destination_id'], data['name'], data['description'], data['price'], data.get('duration_days'), data['image_url'], package_id))
        self.connection.commit()
        cursor.close()
        return self.get_by_id(package_id)

    def delete(self, package_id):
        if not self.connection:
            return False
        cursor = self.connection.cursor()
        query = "UPDATE tour_packages SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (package_id,))
        self.connection.commit()
        cursor.close()
        return cursor.rowcount > 0