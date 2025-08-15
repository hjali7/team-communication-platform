import os
import pytest
from app.main import app, db

# Setup a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use an in-memory SQLite database for tests to keep them fast and isolated
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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
    # Post a new message
    post_response = client.post('/messages', json={
        'username': 'tester',
        'text': 'Hello, World!'
    })
    assert post_response.status_code == 201

    # Get all messages
    get_response = client.get('/messages')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert len(data) == 1
    assert data[0]['username'] == 'tester'
    assert data[0]['text'] == 'Hello, World!'
