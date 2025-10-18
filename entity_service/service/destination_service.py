import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from model.destination_model import DestinationModel

class DestinationService:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.connection.is_connected():
                print("Successfully connected to the database (Destination Service)")
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    # CRUD Operations
    ## GET all destinations
    def get_all(self):
        if not self.connection:
            return []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM destinations WHERE deleted_at IS NULL")
        results = cursor.fetchall()
        cursor.close()
        return [DestinationModel(**result) for result in results]
    
    ## GET destination by ID
    def get_by_id(self, destination_id):
        if not self.connection:
            return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM destinations WHERE id = %s AND deleted_at IS NULL"
        cursor.execute(query, (destination_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return DestinationModel(**result)
        return None

    ##Create new destination
    def create(self, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            INSERT INTO destinations (name, description, location, image_url)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data['name'], data['description'], data['location'], data['image_url']))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return self.get_by_id(new_id)

    ## Update destination by ID
    def update(self, destination_id, data):
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        query = """
            UPDATE destinations SET name = %s, description = %s, location = %s, image_url = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data['name'], data['description'], data['location'], data['image_url'], destination_id))
        self.connection.commit()
        cursor.close()
        return self.get_by_id(destination_id)

    ## Soft Delete destination by ID
    def delete(self, destination_id):
        if not self.connection:
            return False
        cursor = self.connection.cursor()
        # Soft delete
        query = "UPDATE destinations SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (destination_id,))
        self.connection.commit()
        cursor.close()
        return cursor.rowcount > 0