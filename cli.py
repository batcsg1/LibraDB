import argparse

# Class for setting up the CLI
class LibraCLI:
    def __init__(self):
        # Setting up parser
        self.parser = argparse.ArgumentParser(description="LibraDB v1.0.0 CLI")
        # Argument for specifying database name
        self.parser.add_argument("--db", default="db", help="Name of database file")
        self.parser.add_argument("--collection", "-c", help="Setup a data collection" )
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

    