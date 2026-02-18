import argparse

# Class for setting up the CLI
class LibraCLI:
    def __init__(self):
        # Setting up parser
        self.parser = argparse.ArgumentParser(description="LibraDB v1.0.0 CLI")
        # Argument for specifying database name
        self.parser.add_argument("--db", default="db", help="Name of database file")

    # Return the arguments
    def get_args(self):
        return self.parser.parse_args()

    