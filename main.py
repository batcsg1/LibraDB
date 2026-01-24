import os
from toon import encode, decode

# the main database engine which reads and writes to a TOON file

class LibraQL:
    def __init__(self, db_name="db.toon"):
        self.db_name = db_name
        self.data = self._load()
    
    # loads the database from the TOON file
    def _load(self):
        if not os.path.exists(self.db_name):
            print(f"Database file {self.db_name} not found. Creating a new one.")
            with open(self.db_name, 'w') as f:
                f.write("")
            return {}
        with open(self.db_name, 'r') as f:
            try:
                encoded_data = f.read()
                decoded_data = decode(encoded_data)
                return decoded_data if decoded_data else {}
            except Exception as e:
                print(f"Error reading database file: {e}")
                return {}
              
    # saves the current state of the database to the TOON file
    def _save(self):
        with open(self.db_name, 'w') as f:
            try:
                encoded_data = encode(self.data)
                f.write(encoded_data)
            except Exception as e:
                print(f"Error writing to database file: {e}")
            
    def collection(self, name):
        if name not in self.data:
            self.data[name] = []
        return Collection(self, name)
    

class Collection:
    def __init__(self, engine, name):
        self.engine = engine
        self.name = name
        print(f"Collection '{self.name}' initialized.")

    def insert(self, data):
        self.engine.data[self.name].append(data)
        self.engine._save()

    def find(self):
        return self.engine.data.get(self.name, [])


db = LibraQL("my_database.toon")

# Example usage:

# users = db.collection("users")
# users.insert({"name": "Alice", "age": 30})
# users.insert({"name": "Bob", "age": 25})
# print(users.find())
