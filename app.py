from flask import Flask, jsonify, request
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Sample API endpoint to get users"""
    sample_users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
    ]
    
    logger.info(f"Retrieved {len(sample_users)} users")
    return jsonify({
        'users': sample_users,
        'count': len(sample_users)
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    """Sample API endpoint to create a user"""
    user_data = request.get_json()
    
    if not user_data or 'name' not in user_data or 'email' not in user_data:
        return jsonify({'error': 'Invalid user data'}), 400
    
    # Simulate user creation
    new_user = {
        'id': 3,
        'name': user_data['name'],
        'email': user_data['email']
    }
    
    logger.info(f"Created user: {new_user['name']}")
    return jsonify({'user': new_user}), 201

@app.route('/api/process-data', methods=['POST'])
def process_data():
    """Sample data processing endpoint"""
    data = request.get_json()
    
    if not data or 'values' not in data:
        return jsonify({'error': 'No values provided'}), 400
    
    values = data['values']
    if not isinstance(values, list) or not all(isinstance(x, (int, float)) for x in values):
        return jsonify({'error': 'Values must be a list of numbers'}), 400
    
    # Process the data
    result = {
        'original_values': values,
        'sum': sum(values),
        'average': sum(values) / len(values) if values else 0,
        'min': min(values) if values else 0,
        'max': max(values) if values else 0,
        'count': len(values)
    }
    
    logger.info(f"Processed {len(values)} values")
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)