import requests
import sys
import time

# Ubah base URLs bila Anda menjalankan di host/port berbeda
UTILITY_URL = "http://localhost:8002"       # utility_service
ENTITY_URL = "http://localhost:8003"        # entity_service
TASK_URL = "http://localhost:8001"          # task_service
NOTIF_URL = "http://localhost:8004"         # notification_micro_service (opsional)

session_token = None
current_user = None

def register():
    print("\n== Register ==")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    phone = input("Phone number: ").strip()

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "phone_number": phone
    }
    try:
        r = requests.post(f"{UTILITY_URL}/api/users/register", json=payload, timeout=5)
    except requests.RequestException as e:
        print("Gagal terhubung ke Utility Service:", e)
        return
    if r.status_code in (200, 201):
        print("Registrasi sukses. Data user:")
        print(r.json())
    else:
        print("Registrasi gagal:", r.status_code, r.text)

def login():
    global session_token, current_user
    print("\n== Login ==")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    payload = {"email": email, "password": password}
    try:
        r = requests.post(f"{UTILITY_URL}/api/users/login", json=payload, timeout=5)
    except requests.RequestException as e:
        print("Gagal terhubung ke Utility Service:", e)
        return
    if r.status_code == 200:
        data = r.json()
        session_token = data.get("token")
        current_user = data.get("user")
        print("Login sukses. Token disimpan.")
        print("User:", current_user)
    else:
        print("Login gagal:", r.status_code, r.text)

def list_packages(package_type):
    # package_type in: 'tour', 'activity', 'rental'
    mapping = {
        "tour": "tour-packages",
        "activity": "activity-packages",
        "rental": "rental-packages"
    }
    endpoint = mapping.get(package_type)
    if not endpoint:
        print("Tipe paket tidak valid.")
        return
    try:
        r = requests.get(f"{ENTITY_URL}/api/{endpoint}", timeout=5)
    except requests.RequestException as e:
        print("Gagal terhubung ke Entity Service:", e)
        return
    if r.status_code == 200:
        items = r.json()
        if not items:
            print("Tidak ada paket.")
            return
        print(f"\n== Daftar {package_type} packages ==")
        for it in items:
            # tampilkan id, nama, price jika ada
            pid = it.get("id") or it.get(f"{package_type}_packages_id") or it.get("id")
            name = it.get("name") or it.get("title") or it.get("package_name") or ""
            price = it.get("price") or it.get("harga") or ""
            print(f"- id: {pid} | name: {name} | price: {price}")
    else:
        print("Gagal mengambil paket:", r.status_code, r.text)

def create_booking():
    global session_token, current_user
    if not session_token:
        print("Silakan login terlebih dahulu.")
        return
    print("\n== Create Booking ==")
    print("Pilih tipe paket: 1) tour  2) activity  3) rental")
    choice = input("Choice: ").strip()
    types = {"1": "tour", "2": "activity", "3": "rental"}
    package_type = types.get(choice)
    if not package_type:
        print("Pilihan tidak valid.")
        return

    # Tampilkan paket untuk dipilih
    list_packages(package_type)
    package_id = input(f"Masukkan id paket {package_type} yang dipilih: ").strip()
    booking_date = input("Tanggal booking (YYYY-MM-DD) [optional]: ").strip()
    num_persons = input("Jumlah orang [1]: ").strip()
    if not num_persons:
        num_persons = 1
    else:
        try:
            num_persons = int(num_persons)
        except:
            num_persons = 1

    # nama field id sesuai implementasi backend: e.g. 'tour_packages_id'
    id_field = f"{package_type}_packages_id"
    payload = {
        "booking_type": package_type,
        id_field: int(package_id),
        "num_persons": num_persons
    }
    if booking_date:
        payload["booking_date"] = booking_date

    headers = {"Authorization": f"Bearer {session_token}"} if session_token else {}
    try:
        r = requests.post(f"{TASK_URL}/api/bookings", json=payload, headers=headers, timeout=10)
    except requests.RequestException as e:
        print("Gagal terhubung ke Task Service:", e)
        return
    if r.status_code in (200,201):
        print("Booking berhasil dibuat. Response:")
        print(r.json())
        # kemungkinan booking service sudah memicu notifikasi yang akan muncul
        print("\nPerhatikan terminal Notification Service; notifikasi dikirimkan dan dicetak di sana (simulasi).")
    else:
        print("Gagal membuat booking:", r.status_code, r.text)

def send_manual_notification():
    # Hanya untuk pengujian: memicu endpoint notifikasi manual (jika ada)
    print("\n== Manual Notification (opsional) ==")
    user_id = input("user_id: ").strip()
    booking_code = input("booking_code: ").strip()
    print("Pilih tipe notifikasi: 1) confirmation  2) verified")
    c = input("Choice: ").strip()
    if c == "1":
        endpoint = "send-confirmation"
    else:
        endpoint = "send-verified"
    # Asumsi blueprint di-registrasi dengan prefix /api/notifications
    url = f"{NOTIF_URL}/api/notifications/{endpoint}"
    try:
        r = requests.post(url, json={"user_id": int(user_id), "booking_code": booking_code}, timeout=5)
        print("Response:", r.status_code, r.text)
    except requests.RequestException as e:
        print("Gagal memanggil Notification Service:", e)
        print("Jika URL berbeda, periksa prefix di notification_micro_service/app.py")

def menu():
    print("=== TOPTEN CLI ===")
    print("1) Register")
    print("2) Login")
    print("3) Lihat Tour Packages")
    print("4) Lihat Activity Packages")
    print("5) Lihat Rental Packages")
    print("6) Create Booking")
    print("7) (Opsional) Kirim Manual Notification")
    print("0) Exit")

def main_loop():
    while True:
        menu()
        choice = input("Pilihan: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            list_packages("tour")
        elif choice == "4":
            list_packages("activity")
        elif choice == "5":
            list_packages("rental")
        elif choice == "6":
            create_booking()
        elif choice == "7":
            send_manual_notification()
        elif choice == "0":
            print("Keluar.")
            sys.exit(0)
        else:
            print("Pilihan tidak dimengerti.")
        print("\n---\n")
        time.sleep(0.2)

if __name__ == "__main__":
    print("Client CLI untuk TOPTEN-SOA-REST")
    print("Pastikan semua service berjalan:")
    print(" - utility_service (port 8002)")
    print(" - entity_service  (port 8003)")
    print(" - task_service    (port 8001)")
    print(" - notification_micro_service (port 8004)\n")
    main_loop()