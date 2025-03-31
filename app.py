from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS desteği eklemek için
import sqlite3

app = Flask(__name__)
CORS(app)  # Tüm istekler için CORS desteği aç

# Veritabanı bağlantısı
def connect_db():
    return sqlite3.connect("car_meeting.db")

# Veritabanında tablo oluştur (Eğer yoksa)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            car_model TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Kayıt ekleme endpointi
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get("name")
    surname = data.get("surname")
    phone = data.get("phone")
    email = data.get("email")
    car_model = data.get("car_model")

    if not all([name, surname, phone, email, car_model]):
        return jsonify({"error": "Eksik bilgi girdiniz!"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registrations (name, surname, phone, email, car_model) VALUES (?, ?, ?, ?, ?)",
                   (name, surname, phone, email, car_model))
    conn.commit()
    conn.close()

    return jsonify({"message": "Kayıt başarıyla eklendi!"})

# Kayıtlı kullanıcıları listeleme endpointi
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registrations")
    users = cursor.fetchall()
    conn.close()

    users_list = [{"id": row[0], "name": row[1], "surname": row[2], "phone": row[3], "email": row[4], "car_model": row[5]} for row in users]
    return jsonify(users_list)

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
