import pytest
from app import app, collection
from bson import ObjectId
from flask import request
import pymongo
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_menu(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Add Expense' in response.data

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
    added_expense = collection.find_one({'description': 'Dinner'})
    expense_id = added_expense['_id']

    # Try to remove the expense using the obtained ID
    response = client.post('/remove_expense', data=dict(
        expense_id=str(expense_id)
    ), follow_redirects=True)

    # Check if the removal route returns a successful status code
    assert response.status_code == 200

    # Check if the expense is removed from the collection
    removed_expense = collection.find_one({'_id': expense_id})
    assert removed_expense is None

