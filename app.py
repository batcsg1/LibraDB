# Import CLI
from cli import LibraCLI
# Import database engine
from engine import LibraDB


# Setup CLI
interface = LibraCLI()
args = interface.get_args()

# Initialize database
db = LibraDB(f"{args.db}.toon")

# Create an empty data collection
collection = None

# Initialize a collection
if args.collection:
    collection = db.collection(f"{args.collection}")

# If a collection exists and data is findable
if collection:
    # Return all data (--find)
    if args.find == "all":
        data = collection.find()
        print(data)

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
