from flask import Flask, request, jsonify
from service.email_service import EmailService

app = Flask(__name__)
email_service = EmailService()

@app.route('/api/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    
    # Di sini bisa juga memanggil Utility Service untuk dapat email user
    # response = requests.get(f"http://localhost:8002/api/users/{user_id}")
    # user_email = response.json()['email']
    
    # email_service.send_email(user_email, "Booking Update", message)
    
    print(f"Notification for user {user_id}: '{message}'") # Simulasi pengiriman
    return jsonify({"message": "Notification sent"}), 200

if __name__ == '__main__':
    print("Notification Service running on port 8004")
    app.run(port=8004, debug=True)