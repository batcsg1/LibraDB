import argparse

# Class for setting up the CLI
class LibraCLI:
    def __init__(self):
        # Setting up parser
        self.parser = argparse.ArgumentParser(description="LibraDB v1.0.0 - A simple no BS serverless No-SQL database management system")
        # Argument for specifying database name
        self.parser.add_argument("--db", default="db", help="Name of database file you want to load or create")
        self.parser.add_argument("--collection", "-c", help="Name of data collection within the database")
        self.parser.add_argument(
            "--find",
            "-f", 
            nargs="?",
            const="all",
            default=None,
            help="Find data from a collection")

    # Return the arguments
    def get_args(self):
        return self.parser.parse_args()

    