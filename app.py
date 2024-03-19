# Import necessary libraries
from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__, static_folder='templates/static', static_url_path='/static')

# Connect to MongoDB
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://root:nadav@mongo-mongodb:27017/')
client = MongoClient(mongodb_uri)
db = client['expense_tracker']
collection = db['expenses']

# Route to display main menu with expenses and graph
@app.route('/')
def main_menu():
    # Fetch expenses from the MongoDB collection
    expenses = list(collection.find())

    # Aggregate expenses by date and calculate cumulative total amount
    cumulative_total = 0
    cumulative_totals = []
    dates_str = []
    for expense in expenses:
        cumulative_total += expense['amount']
        cumulative_totals.append(cumulative_total)
        dates_str.append(expense['date'].strftime('%Y-%m-%d'))

    # Render index.html template and pass expenses, error message, dates, and amounts to it
    return render_template('index.html', expenses=expenses, dates=dates_str, amounts=cumulative_totals)

# Route to add a new expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    # Get expense data from the form submitted via POST request
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']

    # Ensure that amount is greater than 0
    if amount <= 0:
        return "Expense amount must be greater than 0."

    # Insert the expense data into the MongoDB collection
    expense_data = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }
    result = collection.insert_one(expense_data)

    # Include the ID of the added expense in the redirect URL
    return redirect(url_for('main_menu', expense_id=result.inserted_id))

# Route to remove an expense
@app.route('/remove_expense', methods=['POST'])
def remove_expense():
    # Get expense ID from the form submitted via POST request
    expense_id = request.form['expense_id']

    # Delete the expense from the MongoDB collection
    collection.delete_one({'_id': ObjectId(expense_id)})

    # Redirect to the main page after removing the expense
    return redirect(url_for('main_menu'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
