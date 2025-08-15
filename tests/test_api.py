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

def test_post_get_and_update_tasks(client):
    """Test creating, listing, and updating a task."""
    # 1. Verify there are no tasks initially
    get_initial_response = client.get('/tasks')
    assert get_initial_response.status_code == 200
    assert get_initial_response.get_json() == []

    # 2. Post a new task
    post_response = client.post('/tasks', json={
        'title': 'My first task',
        'description': 'Test the task API'
    })
    assert post_response.status_code == 201
    post_data = post_response.get_json()
    assert post_data['title'] == 'My first task'
    assert post_data['is_completed'] is False
    task_id = post_data['id']

    # 3. Get the list of tasks and verify the new task is there
    get_response = client.get('/tasks')
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert len(get_data) == 1
    assert get_data[0]['title'] == 'My first task'

    # 4. Update the task to be completed
    put_response = client.put(f'/tasks/{task_id}')
    assert put_response.status_code == 200
    put_data = put_response.get_json()
    assert put_data['is_completed'] is True

    # 5. Verify the task is updated in the main list
    get_final_response = client.get('/tasks')
    assert get_final_response.get_json()[0]['is_completed'] is True
