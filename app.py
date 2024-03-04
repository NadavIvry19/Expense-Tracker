from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import plotly.graph_objs as go

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['expense_tracker']
collection = db['expenses']

# Route to display main menu with expenses and graph
@app.route('/')
def main_menu():
    # Fetch expenses from the MongoDB collection
    expenses = list(collection.find())

    # Extract dates and amounts from expenses for graph
    dates = [expense['date'] for expense in expenses]
    amounts = [expense['amount'] for expense in expenses]

    # Create Plotly graph
    graph = go.Figure()
    graph.add_trace(go.Scatter(x=dates, y=amounts, mode='lines+markers'))
    graph_layout = dict(title='Expenses Over Time', xaxis_title='Date', yaxis_title='Amount')
    graph_json = graph.to_json()

    # Check if there are any error messages from a previous request
    error_message = request.args.get('error_message')

    # Render index.html template and pass expenses, error message, and graph JSON to it
    return render_template('index.html', expenses=expenses, error_message=error_message, graph_json=graph_json, graph_layout=graph_layout)

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

    # Check if the amount is greater than 0
    if expense_data['amount'] <= 0:
        error_message = 'Expense amount must be greater than 0'
        return redirect(url_for('main_menu', error_message=error_message))

    # Append ILS currency to the amount
    expense_data['amount'] = str(expense_data['amount']) + " ILS"

    # Insert the expense data into the MongoDB collection
    collection.insert_one(expense_data)

    # Redirect to the main page after adding the expense
    return redirect(url_for('main_menu'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
