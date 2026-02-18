# Import CLI
from cli import LibraCLI
# Import database engine
from engine import LibraDB


# Setup CLI
interface = LibraCLI()
args = interface.get_args()

# Initialize database
db = LibraDB(f"{args.db}.toon")

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
