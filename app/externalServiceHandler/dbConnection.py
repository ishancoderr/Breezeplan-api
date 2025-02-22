import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv("app/externalServiceHandler/mongoDb.env")

class DbConnection:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize MongoDB connection."""
        self.uri = os.getenv("MONGODB_URI")  # Use env variable or fallback
        self.db_name = os.getenv("DB_NAME")
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Connect to MongoDB and ensure the database exists."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.client.admin.command('ping')  # Verify connection
            print(f"Connected to MongoDB: {self.db_name}")

            # Fetch and print the list of collections
            collections = self.db.list_collection_names()
            print(f"Available collections: {collections}")
        except ConnectionFailure as e:
            print("Failed to connect to MongoDB:", e)
            raise ConnectionFailure("Failed to connect to MongoDB: " + str(e))

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

