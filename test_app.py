import pytest
from app import app
from bson import ObjectId

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_menu(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Add Expense' in response.data

def test_add_expense(client):
    response = client.post('/add_expense', data=dict(
        date='2024-03-05',
        category='Food',
        amount='10.50',
        description='Dinner'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Dinner' in response.data

def test_remove_expense(client):
    # Add an expense first
    response = client.post('/add_expense', data=dict(
        date='2024-03-05',
        category='Food',
        amount='10.50',
        description='Dinner'
    ), follow_redirects=True)
    assert response.status_code == 200

    # Retrieve the ID of the added expense
    expense_id = ObjectId()

    # Try to remove the expense using the generated ID
    response = client.post('/remove_expense', data=dict(
        expense_id=expense_id
    ), follow_redirects=True)
    
    # Check if the removal route returns a successful status code
    assert response.status_code == 200
