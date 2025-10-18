# TOPTEN BALI TOUR - SOA REST API

Proyek ini adalah implementasi dari aplikasi layanan tour dan rental kendaraan di Bali menggunakan arsitektur Service-Oriented Architecture (SOA) dengan pendekatan REST API. Aplikasi ini dibangun menggunakan Python dan Flask, dan terdiri dari beberapa layanan mikro yang independen.
                    
# Gambaran Umum Arsitektur

Aplikasi ini dipecah menjadi beberapa layanan yang berjalan pada port berbeda untuk memisahkan tanggung jawab dan meningkatkan skalabilitas.
 Entity Service (Port 8003): Mengelola semua data master seperti   destinasi, paket tour, paket aktivitas, dan paket rental.
 
 Utility Service (Port 8002): Menangani fungsi pendukung seperti autentikasi pengguna (login, register) dan manajemen data pengguna.
 
 Task Service (Port 8001): Mengelola proses bisnis inti yang melibatkan beberapa layanan, seperti pembuatan booking dan verifikasi.
 
 Notification Service (Port 8004): Layanan khusus untuk mengirim notifikasi (misalnya, email atau WhatsApp) kepada pengguna terkait status booking atau pengingat jadwal.

# Instalasi dan Setup
1. Kloning Repository
    git clone https://github.com/Benedictaurie/TOPTEN-SOA-REST.git
    cd TOPTEN-SOA-REST

2. Setup Database
- Jalankan server MySQL
- Buat database baru dengan nama topten_bali_tour
- Impor file SQL yang tersedia di folder db_stuff dalam project ini ke dalam database yang dimiliki 

3. Instalasi Dependensi
- Setiap layanan memiliki dependensinya sendiri maka dari itu perlu menginstalnya untuk setiap folder layanan.

- Buka beberapa terminal dan jalankan perintah berikut di setiap folder layanan (entity_service, notification_micro_service, task_service, dan utility_service)

- Daftar dependensi di requirements.txt: 
    Flask
    Flasgger
    requests
    mysql-connector-python
    python-dotenv 

- Cara install dependensinya di terminal:
    cd entity_service
    pip install -r requirements.txt

    cd utility_service
    pip install -r requirements.txt

.. dan seterusnya.

4. Environment Configuration
Setiap layanan memerlukan file konfigurasi 
.env untuk pengaturan koneksi database dan port. Buat file .env di dalam setiap folder layanan.

Contoh .env di entity_service:
    FLASK_APP=app.py
    FLASK_RUN_PORT=8003
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=topten_bali_tour
        
Contoh .env di utility_serive:
    FLASK_APP=app.py
    FLASK_RUN_PORT=8002
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=
    DB_NAME=topten_bali_tour

... dan seterusnya.

# Cara menjalankan Aplikasi
1. Membuka 4 terminal yang berbeda
2. Di setiap terminal, navigasi ke folder layanan yang berbeda

- Terminal 1
    cd entity_service
    python app.py

Layanan akan berjalan di http://localhost:8003

- Terminal 2
    cd notification_micro_service
    python app.py
            
Layanan akan berjalan di http://localhost:8004

- Terminal 3
    cd task_service
    python app.py

Layanan akan berjalan di http://localhost:8001

- Terminal 4
    cd utility_service
    python app.py

Layanan akan berjalan di http://localhost:8002