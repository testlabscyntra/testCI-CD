import pytest
import json
from app import app
from utils.data_processor import DataProcessor

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data

def test_get_users(client):
    """Test get users endpoint"""
    response = client.get('/api/users')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'users' in data
    assert 'count' in data
    assert data['count'] == len(data['users'])

def test_create_user(client):
    """Test create user endpoint"""
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = client.post('/api/users', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['user']['name'] == user_data['name']
    assert data['user']['email'] == user_data['email']

def test_create_user_invalid_data(client):
    """Test create user with invalid data"""
    response = client.post('/api/users',
                          data=json.dumps({'name': 'Test'}),
                          content_type='application/json')
    assert response.status_code == 400

def test_process_data(client):
    """Test data processing endpoint"""
    test_data = {
        'values': [1, 2, 3, 4, 5]
    }
    
    response = client.post('/api/process-data',
                          data=json.dumps(test_data),
                          content_type='application/json')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'result' in data
    assert data['result']['sum'] == 15
    assert data['result']['average'] == 3.0

def test_data_processor():
    """Test DataProcessor class"""
    processor = DataProcessor()
    
    # Test validation
    valid_record = {'id': 1, 'timestamp': '2024-01-01', 'value': 100}
    assert processor.validate_data(valid_record) == True
    
    invalid_record = {'id': 1, 'value': 100}  # missing timestamp
    assert processor.validate_data(invalid_record) == False
    
    # Test processing
    batch = [
        {'id': 1, 'timestamp': '2024-01-01', 'value': 75},
        {'id': 2, 'timestamp': '2024-01-01', 'value': 150}
    ]
    
    processed = processor.process_batch(batch)
    assert len(processed) == 2
    assert processed[0]['category'] == 'medium'
    assert processed[1]['category'] == 'high'