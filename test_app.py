import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_menu(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Expense Tracker' in response.data

def test_add_expense(client):
    response = client.post('/add_expense', data={
        'date': '2024-03-05',
        'category': 'Food',
        'amount': '20.50',
        'description': 'Lunch'
    })
    assert response.status_code == 302  # Redirect status code
    assert 'expense_id' in response.headers['Location']

    # Extract the expense ID from the redirect URL
    expense_id = response.headers['Location'].split('=')[-1]

    # Test removing the added expense
    remove_response = client.post('/remove_expense', data={
        'expense_id': expense_id
    })
    assert remove_response.status_code == 302  # Redirect status code

if __name__ == '__main__':
    pytest.main()
