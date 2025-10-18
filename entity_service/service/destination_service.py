import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from model.destination_model import DestinationModel

class DestinationService:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    def get_all(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM destinations WHERE deleted_at IS NULL")
        results = cursor.fetchall()
        cursor.close()
        return [DestinationModel(**result) for result in results]

    def get_by_id(self, destination_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM destinations WHERE id = %s AND deleted_at IS NULL"
        cursor.execute(query, (destination_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return DestinationModel(**result)
        return None

    # method create, update, delete tambahkan di sini