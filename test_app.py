import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_main_menu(client):
    """Test if the main menu page is accessible."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Expense Tracker" in response.data


def test_add_expense(client):
    """Test adding a new expense."""
    # Data for the expense form
    data = {
        'date': '2024-03-05',
        'category': 'Groceries',
        'amount': '50.00',
        'description': 'Weekly groceries shopping'
    }

    # Send a POST request to add the expense
    response = client.post('/add_expense', data=data, follow_redirects=True)

    # Check if the expense is added successfully
    assert response.status_code == 200
    assert b"Groceries" in response.data
    assert b"50.00" in response.data
    assert b"Weekly groceries shopping" in response.data
