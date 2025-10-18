import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Database
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root05")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iridiumsilver")
DB_NAME = os.getenv("DB_NAME", "topten_bali_tour")

# Konfigurasi Layanan Lain
UTILITY_SERVICE_URL = os.getenv("UTILITY_SERVICE_URL", "http://localhost:8002")
ENTITY_SERVICE_URL = os.getenv("ENTITY_SERVICE_URL", "http://localhost:8003")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004")