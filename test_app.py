import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    submissions.clear()  # Clear memory before each test
    with app.test_client() as client:
        yield client

# Test Case 1: Complete details and a valid submission URL
def test_valid_submission(client):
    response = client.post('/', data={
        'name': 'Ali',
        'reg_no': 'CSC-001',
        'title': 'Lab 1',
        'url': 'https://example.com/file.pdf'
    }, follow_redirects=True)
    
    # Check that it saved and appears in the list
    assert b'CSC-001' in response.data
    assert b'https://example.com/file.pdf' in response.data

# Test Case 2: Missing registration number
def test_missing_registration_number(client):
    response = client.post('/', data={
        'name': 'Ali',
        'reg_no': '', # Missing!
        'title': 'Lab 1',
        'url': 'https://example.com/file.pdf'
    })
    
    # Check that it was rejected with a validation message
    assert b'All fields are required.' in response.data
    assert len(submissions) == 0

# Test Case 3: Invalid submission URL
def test_invalid_url(client):
    response = client.post('/', data={
        'name': 'Ali',
        'reg_no': 'CSC-001',
        'title': 'Lab 1',
        'url': 'not-a-real-url' # Invalid!
    })
    
    # Check that it was rejected and not saved
    assert b'Invalid submission URL' in response.data
    assert len(submissions) == 0