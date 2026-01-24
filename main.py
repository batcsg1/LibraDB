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
                # Try and convert TOON data to Python dictionary
                decoded_data = decode(encoded_data)
                return decoded_data if decoded_data else {}
            except Exception as e:
                print(f"Error reading database file: {e}")
                return {}
              
    # saves the current state of the database to the TOON file
    def _save(self):
        with open(self.db_name, 'w') as f:
            try:
                # Write Python dictionary as TOON encoded data
                encoded_data = encode(self.data)
                f.write(encoded_data)
            except Exception as e:
                print(f"Error writing to database file: {e}")
            
    def collection(self, name):
        if name not in self.data:
            # Add a list for the new collection to the master dictionary (self.data)
            self.data[name] = []
        return Collection(self, name)
    

class Collection:
    def __init__(self, engine, name):
        self.engine = engine
        self.name = name
        print(f"Collection '{self.name}' initialized.")

    def insert(self, data):
        print(f"Inserting data into collection '{self.name}': {data}")
        self.engine.data[self.name].append(data)
        self.engine._save()

    def find(self, query=None):
        print(f"Finding data in collection '{self.name}'")
        data = self.engine.data.get(self.name, [])

        # If no query is provided, return all records
        if not query:
            print("No query provided, returning all records.")
            #return encode(data)
            return data
                
        # Define the matching logic inside a helper function
        def matches(item):
            for k, v in query.items():
                val = item.get(k)
                if isinstance(v, dict):
                    # Logical check for operators
                    if "$gt" in v and not (val > v["$gt"]): return False
                    if "$lt" in v and not (val < v["$lt"]): return False
                    if "$gte" in v and not (val >= v["$gte"]): return False
                    if "$lte" in v and not (val <= v["$lte"]): return False
                elif val != v:
                    return False
            return True

        # Use filter to create an iterator, then cast to list
        return list(filter(matches, data))

    def update(self, query, new_data):
        print(f"Updating data in collection '{self.name}' with query: {query} and new data: {new_data}")

        # Find matching documents
        data = self.find(query)

        # If no documents match the query
        if not data:
            print("No documents matched the query. Nothing updated.")
            return 0

        # Update the matching documents
        for item in data:
            item.update(new_data)

        self.engine._save()

        print(f"Updated {len(data)} documents.")
        return len(data)
    
    def delete(self, query):
        print(f"Deleting data from collection '{self.name}' with query: {query}")

        if not query:
            print("No query provided. Nothing deleted.")
            return 0
        
        # 1. Get ALL current data in this collection
        data = self.engine.data.get(self.name, [])
        initial_count = len(data)

        # 2. Use filter() to keep items that do NOT match the query
        # We wrap it in list() because filter returns an iterator
        self.engine.data[self.name] = list(filter(
            lambda item: not all(item.get(k) == v for k, v in query.items()), 
            data
        ))

        # 3. Calculate and Save
        deleted_count = initial_count - len(self.engine.data[self.name])
        
        if deleted_count > 0:
            self.engine._save()
            print(f"Successfully deleted {deleted_count} document(s).")
        
        return deleted_count

        
# Initialize the database


db = LibraQL("my_database.toon")

# #Example usage:

users = db.collection("users")
# users.insert({"name": "Charlie", "age": 35})
# users.insert({"name": "Alice", "age": 30})
# users.insert({"name": "Bob", "age": 25})
# users.insert({"name": "Diana", "age": 28})
# users.insert({"name": "Eve", "age": 22})
#users.update({"name": "James"}, {"age": 31})


users.delete({"name": "Diana"})
print(users.find())
