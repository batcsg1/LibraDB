import os
from toon import encode, decode
from logger import Colors, Logger

logger = Logger(".\logs\log")
colors = Colors()

# the main database engine which reads and writes to a TOON file (Data persistence layer)
class LibraDB:
    # Name and load the database file
    def __init__(self, db_name="db.toon"):
        logger._log(f"Intializing database with filename: {db_name}", colors.info)

        self.db_name = db_name
        self.data = self._load()
    
    # Load the database into a TOON file or create the TOON file
    def _load(self):
        # If the file doesn't exist, create an empty file
        if not os.path.exists(self.db_name):
            logger._log(f"Database file {self.db_name} not found. Creating a new one.", colors.warning)

            with open(self.db_name, 'w') as f:
                f.write("")
            return {}
        
        #Open and read the database file
        with open(self.db_name, 'r') as f:
            try:
                # Read from the file
                encoded_data = f.read()

                # Convert TOON data into dictionary
                decoded_data = decode(encoded_data)

                # If there is TOON data return the TOON data, otherwise return an empty dictionary
                return decoded_data if decoded_data else {}
            except Exception as e:
                # If there is a problem reading the TOON file, e.g. if the file is empty.
                logger._log(f"Error reading database file: {e}", colors.error)
                return {}
              
    # Saves the current state of the database to the database file
    def _save(self):
        # Open and write to the database file
        with open(self.db_name, 'w') as f:
            try:
                # write the data dictionary into TOON data
                encoded_data = encode(self.data)
                f.write(encoded_data)
            except Exception as e:
                # If there is a problem reading the TOON file, e.g. if the file is empty.
                logger._log(f"Error writing to database file: {e}", colors.error)
            
    # Creating a data collection
    def collection(self, name):
        # If there is no data collection
        if name not in self.data:
            # Add a list for the new collection to the 'master' data dictionary (self.data)
            self.data[name] = []
        # Return the new data collection
        return Collection(self, name)
    
# Collection class to handle operations on a specific collection (Data access layer)
class Collection:
    # Reference the engine, and initialize a new data collection
    def __init__(self, engine, name):
        self.engine = engine
        self.name = name
        logger._log(f"Collection '{self.name}' initialized.", colors.success)

    # Insert into the collection
    def insert(self, data):
        logger._log(f"INSERT: Inserting data into collection '{self.name}': {data}", colors.info)

        # Add to the collection list
        self.engine.data[self.name].append(data)

        # Write the list to the database file
        self.engine._save()

    # Select from the collection
    def find(self, options=None):

        options = options or {}

        query = options.get("query")
        select = options.get("select")
        sort = options.get("sort")


        logger._log(f"FIND: Finding data in collection '{self.name}'", colors.info)

        # Get the data from the collection list, return an empty list if there is no data, hence the '[]'
        data = self.engine.data.get(self.name, [])

        # Query the data
        if query:              
            # Find items that match what is specified in the query
            def matches(item):
                # Check each key-value pair in the query
                for k, v in query.items():
                    #{"age": {"$gt": 25}} Query example
                    
                    #query.items() = dict_items([( k: 'age', v: {'$gt': 25})])

                    # Get the current value of the item from the collection

                    val = item.get(k) #E.g. val = {"age": 25}, val would be 25

                    # if the value (v) of the query is a dictionary
                    if isinstance(v, dict):
                        # Logical check for operators
                        if "$gt" in v and not (val > v["$gt"]): return False
                        if "$lt" in v and not (val < v["$lt"]): return False
                        if "$gte" in v and not (val >= v["$gte"]): return False
                        if "$lte" in v and not (val <= v["$lte"]): return False
                    elif val != v:
                        return False
                return True
            # Filter the data collection for values that match what was asked for in the query and return the results as a list
            data = list(filter(matches, data))
        else:
            # If no query is provided, return all records
            logger._log("No query provided, using all records.")

        # If certain fields are selected, filter the data to only include those fields
        if select and isinstance(select, dict):
            data = [
                {k: v for k, v in item.items() if select.get(k, False)} for item in data
            ]

        # If sorting is specified, sort the data accordingly
        if sort and isinstance(sort, dict):
            for key, direction in sort.items():
                reverse = True if direction == -1 else False
                data.sort(key=lambda x: x.get(key, None), reverse=reverse)

        return data

    # Update the collection
    def update(self, query, new_data):
        logger._log(f"UPDATE: Updating data in collection '{self.name}' with query: {query} and new data: {new_data}", colors.info)

        # Find matching documents
        data = self.find(query)

        # If no documents match the query
        if not data:
            logger._log("No documents matched the query. Nothing updated.")
            return 0

        # Update the matching documents
        for item in data:
            item.update(new_data)

        # Write the updated collection to the database file
        self.engine._save()

        logger._log(f"Updated {len(data)} documents.", colors.success)
        return len(data)
    
    # Delete from the collection
    def delete(self, query):
        logger._log(f"DELETE: Deleting data from collection '{self.name}' with query: {query}", colors.info)

        # Find matching documents
        data = self.find(query)

        # If no documents match the query
        if not data:
            logger._log("No documents matched the query. Nothing deleted.")
            return 0

        # 2. Get the full list from the engine
        raw_collection = self.engine.data[self.name]

        # 3. Remove each target from the full list by removing the items specified in the query
        for item in data:
            raw_collection.remove(item)

        # 4. Save the changes to the database file
        self.engine._save()

        logger._log(f"Deleted {len(data)} documents.", colors.success)
        return len(data)
