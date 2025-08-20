import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()

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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed
        }

# --- Application Factory ---
def create_app(testing=False):
    app = Flask(__name__)
    
    # --- این بخش اضافه شود ---
    if not testing:
        PrometheusMetrics(app)
    # -------------------------

    # --- Database Configuration ---
    if testing:
        # در حالت تست، از دیتابیس SQLite در حافظه استفاده می‌کنیم
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        db_user = os.getenv("POSTGRES_USER", "user")
        db_password = os.getenv("POSTGRES_PASSWORD", "password")
        db_name = os.getenv("POSTGRES_DB", "db")
        db_host = os.getenv("DB_HOST", "db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # آبجکت db را به اپلیکیشن متصل می‌کنیم
    db.init_app(app)

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

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_json() for task in tasks])

    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        if not data or not 'title' in data:
            return jsonify({'error': 'Title is required'}), 400
        
        new_task = Task(
            title=data['title'],
            description=data.get('description', '')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_json()), 201

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)
        task.is_completed = True
        db.session.commit()
        return jsonify(task.to_json())

    return app
