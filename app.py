from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['expense_tracker']
collection = db['expenses']

# Route to display main menu
@app.route('/')
def main_menu():
    # Fetch expenses from the MongoDB collection
    expenses = list(collection.find())
    
    # Check if there are any error messages from a previous request
    error_message = request.args.get('error_message')

    # Render index.html template and pass expenses and error message to it
    return render_template('index.html', expenses=expenses, error_message=error_message)

# Route to add a new expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    # Get expense data from the form submitted via POST request
    expense_data = {
        "date": datetime.strptime(request.form['date'], '%Y-%m-%d'),  # Convert to datetime object
        "category": request.form['category'],
        "amount": float(request.form['amount']),  # Convert to float
        "description": request.form['description']
    }

    # Check if any input is missing except for the description field
    if not all(expense_data.values()) or not expense_data['description']:
        error_message = 'Form not filled'
        return redirect(url_for('main_menu', error_message=error_message))

    # Insert the expense data into the MongoDB collection
    collection.insert_one(expense_data)

    # Redirect to the main page after adding the expense
    return redirect(url_for('main_menu'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
