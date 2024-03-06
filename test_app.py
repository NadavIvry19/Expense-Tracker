import pytest
from datetime import datetime

from app import app, collection  # Assuming your app is in a file named 'your_app.py'

# Test data for expenses
TEST_EXPENSES = [
    {
        "date": datetime.strptime("2024-03-05", "%Y-%m-%d"),
        "category": "Food",
        "amount": 25.50,
        "description": "Groceries",
    },
    {
        "date": datetime.strptime("2024-03-04", "%Y-%m-%d"),
        "amount": 10.00,
        "description": "Movie ticket",
    },
]


@pytest.fixture
def client():
    with app.test_client() as client:
        # Clear the collection before each test
        collection.delete_many({})
        yield client


def test_main_menu_empty(client):
    # Test with an empty collection
    response = client.get("/")
    assert response.status_code == 200
    assert b"No expenses yet" in response.data  # Check for empty message


def test_main_menu_with_expenses(client):
    # Insert test data
    for expense in TEST_EXPENSES:
        collection.insert_one(expense)

    response = client.get("/")
    assert response.status_code == 200

    # Check if all expenses are displayed
    for expense in TEST_EXPENSES:
        assert expense["description"] in response.data.decode()


def test_add_expense(client):
    new_expense = {
        "date": datetime.strptime("2024-03-06", "%Y-%m-%d"),
        "category": "Transportation",
        "amount": 15.75,
        "description": "Bus fare",
    }

    response = client.post("/add_expense", data=new_expense)
    assert response.status_code == 302  # Redirect for successful POST

    # Check if the new expense is added to the collection
    inserted_expense = collection.find_one(new_expense)
    assert inserted_expense is not None


def test_remove_expense(client):
    # Insert test data
    for expense in TEST_EXPENSES:
        collection.insert_one(expense)

    # Get the ID of the first expense
    expense_to_remove = collection.find_one()
    expense_id = str(expense_to_remove["_id"])

    response = client.post("/remove_expense", data={"expense_id": expense_id})
    assert response.status_code == 302  # Redirect for successful POST

    # Check if the removed expense is gone
    removed_expense = collection.find_one({"_id": ObjectId(expense_id)})
    assert removed_expense is None
