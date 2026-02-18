# Use Python's built-in argparse library for setting up LibraDB CLI
import argparse
# Import database engine
from engine import LibraDB

# Create CLI parser
parser = argparse.ArgumentParser(description="LibraDB CLI")

# Add argument for creating database file
parser.add_argument("--db", default="db", help="Name of database file")

# Parse the arguments
args = parser.parse_args()

## -- Pass the arguments to LibraDB

# Initialize the database engine with the parsed argument
db = LibraDB(f"{args.db}.toon")

print(f"Connected to {args.db}")

# Initialize the database
#db = LibraDB("my_database.toon")

# Initialize a collection
#users = db.collection("users")

# Insert a user
# newUser = users.insert({ "name": "Brent", "age": 21 })

# Find all users
#allUsers = users.find({ "query": {"age": {"$gte": 30}}})

# Find specific users

# Sort users
# allUsers = users.find(sort={"age": 1})
# Retrieve a specific number of users

# Show a specific amount of fields of the user object

#print(allUsers)
