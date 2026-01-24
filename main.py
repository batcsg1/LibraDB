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
            # Check each key-value pair in the query

            for k, v in query.items():

                #{"age": {"$gt": 25}} Query example
                #dict_items([( k: 'age', v: {'$gt': 25})])

                # Get the value from the item from the collection
                val = item.get(k) #E.g. val = {"$gt": 25}} or 25

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

        # Find matching documents
        data = self.find(query)

        # If no documents match the query
        if not data:
            print("No documents matched the query. Nothing updated.")
            return 0

        # 2. Get the full list from the engine
        raw_collection = self.engine.data[self.name]

        # 3. Remove each target from the main list
        for item in data:
            raw_collection.remove(item)

        # 4. Save the changes to the TOON file
        self.engine._save()

        print(f"Deleted {len(data)} documents.")
        return len(data)

        
# Initialize the database


db = LibraQL("my_database.toon")

# #Example usage:

users = db.collection("users")
# users.insert({"name": "Alice", "age": 30})
# users.insert({"name": "Bob", "age": 25})
# users.insert({"name": "Diana", "age": 28})


users.delete({"name": "Charlie"})
print(users.find())
