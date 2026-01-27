from engine import LibraQL

db = LibraQL("my_database.toon")

users = db.collection("users")

print(users.find())