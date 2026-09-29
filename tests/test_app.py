import pytest
from app import create_app, db
from app.models import User, JobApplication

@pytest.fixture
def app():
    """Sets up an isolated, configuration-overridden test app instance."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory DB so tests never pollute app.db
        "WTF_CSRF_ENABLED": False  # Disable CSRF tokens to make testing forms easy
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a simulated browser client to make testing requests."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Helper fixture to quickly inject a standard user into the test database."""
    with app.app_context():
        # Password hashing matches what auth routes look for
        from app import bcrypt
        hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='testcoder', email='test@example.com', password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return user.id

# ==============================================================================
# 🔐 AUTHENTICATION & VIEW TESTS
# ==============================================================================

def test_home_redirects_anonymous_user(client):
    """Ensure a logged-out guest trying to visit the homepage is redirected to login."""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_user_registration(client, app):
    """Verify that registering a new user creates a matching record in the database."""
    response = client.post('/register', data={
        'username': 'newdeveloper',
        'email': 'new@example.com',
        'password': 'securepassword123',
        'confirm_password': 'securepassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.username == 'newdeveloper'

# ==============================================================================
# 📡 RESTful API ENDPOINT TESTS
# ==============================================================================

def test_api_get_jobs_empty(client):
    """Verify GET /api/jobs returns an empty list when no data exists."""
    response = client.get('/api/jobs')
    assert response.status_code == 200
    
    # parse the response data as a JSON dictionary
    data = response.get_json()
    assert "jobs" in data
    assert len(data["jobs"]) == 0

def test_api_create_job_success(client, test_user):
    """Verify POST /api/jobs successfully appends a job application record."""
    payload = {
        "company": "Stripe",
        "role": "Backend Engineer",
        "user_id": test_user
    }
    
    # We send real json headers and dump our payload dictionary
    response = client.post('/api/jobs', json=payload)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data["message"] == "Job tracked successfully!"
    assert "job_id" in data

def test_api_create_job_missing_fields(client):
    """Verify POST /api/jobs rejects invalid data structures with a 400 error."""
    incomplete_payload = {
        "company": "Incomplete Inc"
        # Missing 'role' and 'user_id'
    }
    response = client.post('/api/jobs', json=incomplete_payload)
    assert response.status_code == 400
    
    data = response.get_json()
    assert "error" in data

def test_api_delete_job_success(client, app, test_user):
    """Verify DELETE /api/jobs/<id> successfully deletes a tracked record."""
    # 1. Manually add a job record to delete
    with app.app_context():
        job = JobApplication(company="Meta", role="Data Engineer", user_id=test_user)
        db.session.add(job)
        db.session.commit()
        target_id = job.id

    # 2. Issue the delete call via the API client wrapper
    response = client.delete(f'/api/jobs/{target_id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert "deleted successfully" in data["message"]

    # 3. Confirm it's gone from the database
    with app.app_context():
        deleted_job = JobApplication.query.get(target_id)
        assert deleted_job is None
