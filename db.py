from pymongo import MongoClient
from datetime import datetime
#Testcommitfromvscode
# Connect to the MongoDB server running on localhost at default port 27017
client = MongoClient('mongo', 27017)

# Access a specific database, create it if not exists
db = client['expense_tracker']

# Access a specific collection in the database, create it if not exists
expenses_collection = db['expenses']

# Check if the expenses collection is empty
if expenses_collection.count_documents({}) == 0:
    # Define sample expense data
    expenses_data = [
        {
            "date": datetime(2024, 1, 5),
            "category": "Groceries",
            "amount": 50.25,
            "description": "Weekly groceries shopping"
        },
        {
            "date": datetime(2024, 1, 10),
            "category": "Utilities",
            "amount": 120.00,
            "description": "Electricity bill for January"
        },
        
    ]

    # Insert sample expense data into the expenses collection
    insert_result = expenses_collection.insert_many(expenses_data)
    print("Inserted", len(insert_result.inserted_ids), "expenses")
else:
    print("Expenses collection is not empty. Skipping insertion.")

# Close the connection to the MongoDB server
client.close()
