import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# --- App Initialization ---
app = Flask(__name__)

# --- Database Configuration ---
# آدرس دیتابیس از متغیرهای محیطی خوانده می‌شود
db_user = os.getenv("POSTGRES_USER", "user")
db_password = os.getenv("POSTGRES_PASSWORD", "password")
db_name = os.getenv("POSTGRES_DB", "db")
db_host = "db" # نام سرویس دیتابیس در docker-compose

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'text': self.text
        }

# --- API Endpoints ---
@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "Welcome to the REAL Team Communication Platform!"})

@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    if not data or not 'username' in data or not 'text' in data:
        return jsonify({'error': 'Missing data'}), 400

    new_message = Message(username=data['username'], text=data['text'])
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_json()), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([message.to_json() for message in messages])

# --- Main Execution ---
if __name__ == "__main__":
    # این دستور جدول‌ها را در دیتابیس ایجاد می‌کند اگر وجود نداشته باشند
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
