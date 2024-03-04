# app.py

# Import necessary libraries
from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import plotly.graph_objs as go
import json
from bson import ObjectId


# Initialize Flask app
app = Flask(__name__, static_folder='templates/static', static_url_path='/static')

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
  dates_str = [expense['date'].strftime('%Y-%m-%d') for expense in expenses]
  amounts = [expense['amount'] for expense in expenses]

  # Create Plotly graph
  graph = go.Figure()
  graph.add_trace(go.Scatter(x=dates_str, y=amounts, mode='lines+markers'))
  graph_layout = dict(title='Expenses Over Time', xaxis_title='Date', yaxis_title='Amount')

  # Convert graph data to JSON format
  graph_json = graph.to_json()

  # Render index.html template and pass expenses, error message, and graph JSON to it
  return render_template('index.html', expenses=expenses, graph_json=graph_json, graph_layout=graph_layout)

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

  # Insert the expense data into the MongoDB collection
  collection.insert_one(expense_data)

  # Redirect to the main page after adding the expense
  return redirect(url_for('main_menu'))

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
  app.run(debug=True)
