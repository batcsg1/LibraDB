import os
from toon import encode, decode

# the main database engine which reads and writes to a TOON file

class Engine:
    def __init__(self, db_name="db.toon"):
        self.db_name = db_name
        self.registry = self._load()
    
    # loads the database from the TOON file
    def _load(self):
        if not os.path.exists(self.db_name):
            return {}
        with open(self.db_name, 'r') as f:
            encoded_data = f.read()
        decoded_data = decode(encoded_data)
        return decoded_data if decoded_data else {}
    
    # saves the current state of the database to the TOON file
    def _save(self):
        with open(self.db_name, 'w') as f:
            encoded_data = encode(self.registry)
            f.write(encoded_data)


    def collection(self, name):
        if name not in self.registry:
            self.registry[name] = []
        return Collection(self, name)
    

class Collection:
    def __init__(self, engine, name):
        self.engine = engine
        self.name = name

    def insert(self, data):
        self.engine.registry[self.name].append(data)
        self.engine._save()

    def find_all(self):
        return self.engine.registry.get(self.name, [])


db = Engine("my_database.toon")

users = db.collection("users")
users.insert({"name": "Alice", "age": 30})
users.insert({"name": "Bob", "age": 25})

print(users.find_all())
