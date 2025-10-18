# TOPTEN BALI TOUR - SOA REST API

Proyek ini adalah implementasi dari aplikasi layanan tour dan rental kendaraan di Bali menggunakan arsitektur Service-Oriented Architecture (SOA) dengan pendekatan REST API. Aplikasi ini dibangun menggunakan Python dan Flask, dan terdiri dari beberapa layanan mikro yang independen.
                    
# Gambaran Umum Arsitektur

Aplikasi ini dipecah menjadi beberapa layanan yang berjalan pada port berbeda untuk memisahkan tanggung jawab dan meningkatkan skalabilitas.
- Entity Service (Port 8003): Mengelola semua data master seperti   destinasi, paket tour, paket aktivitas, dan paket rental.
 
- Utility Service (Port 8002): Menangani fungsi pendukung seperti autentikasi pengguna (login, register) dan manajemen data pengguna.
 
- Task Service (Port 8001): Mengelola proses bisnis inti yang melibatkan beberapa layanan, seperti pembuatan booking dan verifikasi.
 
- Notification Service (Port 8004): Layanan khusus untuk mengirim notifikasi (misalnya, email atau WhatsApp) kepada pengguna terkait status booking atau pengingat jadwal.

# Requirements
- Flask
- Flasgger
- requests
- mysql-connector-python
- python-dotenv 

# Setup Database
**Import Database**
- Import file database yang sudah tersedia di direktori file `db_stuff/topten_bali_tour.sql`
**Import Postman Collection**
- Import file API collection yang sudah tersedia di direktori file `documentation/toptenbalitour_api_collection.json` ke Postman

# Instalasi 
### 1. Clone repository
```
git clone https://github.com/Benedictaurie/TOPTEN-SOA-REST.git 
cd TOPTEN-SOA-REST
```
### 2. Instalasi requitrements
`pip install -r requirements.txt`

# Environment Configuration
Setiap layanan memerlukan file konfigurasi .env untuk pengaturan koneksi database dan port. Buat file .env di dalam setiap folder layanan.

Contoh .env di entity_service:
```
FLASK_APP=app.py
FLASK_RUN_PORT=8003
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=topten_bali_tour
```
        
Contoh .env di utility_serive:
```
FLASK_APP=app.py
FLASK_RUN_PORT=8002
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=topten_bali_tour
```
... dan seterusnya.

# Cara menjalankan Aplikasi
- Membuka 4 terminal yang berbeda**
- Di setiap terminal, navigasi ke folder layanan yang berbeda

**Terminal 1 - entity_service**
- `cd entity_service`
- `python app.py`

**Terminal 2 - notification_micro_service**
- `cd notification_micro_service`
- ` python app.py`

**Terminal 3 - task_service**
- `cd task_service`
- `python app.py`

**Terminal 4 - utility_service**
- `cd utility_service`
- `python app.py`
