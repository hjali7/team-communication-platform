import pytest
from app.main import create_app, db

@pytest.fixture
def app():
    # اپلیکیشن را در حالت تست ایجاد می‌کنیم
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    # یک کلاینت تست از اپلیکیشن می‌سازیم
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()

# --- Test Cases ---
def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_post_and_get_messages(client):
    """Test posting a new message and then retrieving it."""
    post_response = client.post('/messages', json={'username': 'tester', 'text': 'Hello, World!'})
    assert post_response.status_code == 201
    get_response = client.get('/messages')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert len(data) == 1
    assert data[0]['username'] == 'tester'
