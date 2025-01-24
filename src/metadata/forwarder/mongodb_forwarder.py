from pathlib import Path  # Import Path for handling file paths.
from pymongo import MongoClient  # Import MongoClient for MongoDB connections.
from pymongo.collection import Collection  # Import Collection for MongoDB collection operations.
from src.metadata.forwarder.forwarder_interface import IForwarder  # Import the IForwarder interface for standardizing forwarders.
from typing import Optional  # Import Optional for type hinting optional attributes.
import json  # Import json for reading and processing metadata files.
import os  # Import os for accessing environment variables.

class MongoDbForwarder(IForwarder):
    """
    A forwarder class that sends metadata to a MongoDB database.

    Attributes:
        mongodb_url (Optional[str]): The MongoDB connection URL, retrieved from environment variables.
        mongodb_database_name (Optional[str]): The name of the MongoDB database.
        mongodb_collection_name (Optional[str]): The name of the MongoDB collection.
        mongoDbClient (Optional[MongoClient]): The MongoDB client instance.
        mongoDbCollection (Optional[Collection]): The MongoDB collection instance.

    Methods:
        forward(metadata_path: Path) -> int:
            Sends metadata from the given file to the MongoDB collection.
        close() -> None:
            Closes the MongoDB client connection.
        _preprocess_metadata(metadata_path: Path) -> list:
            Preprocesses metadata by replacing invalid MongoDB field characters.
        _get_mongodb_credentials() -> None:
            Retrieves MongoDB connection details from environment variables.
        _get_mongodb_collection() -> Collection:
            Returns the MongoDB collection instance, initializing the connection if necessary.
        count_documents() -> int:
            Counts the number of documents in the MongoDB collection.
        get_metadata_by_id(resource_id: str) -> dict:
            Retrieves metadata for a specific resource by ID.
    """

    # MongoDB connection details and client/collection placeholders.
    mongodb_url: Optional[str] = None
    mongodb_database_name: Optional[str] = None
    mongodb_collection_name: Optional[str] = None
    mongoDbClient: Optional[MongoClient] = None
    mongoDbCollection: Optional[Collection] = None

    @classmethod
    def forward(cls, metadata_path: Path) -> int:
        """
        Sends metadata from the given file to the MongoDB collection.

        Args:
            metadata_path (Path): The path to the metadata file.

        Returns:
            int: 0 if successful, 1 if an error occurred.
        """
        try:
            print(f"Forwarding metadata from: {metadata_path}")
            collection = cls._get_mongodb_collection()
            metadata_list = cls._preprocess_metadata(metadata_path)
            if metadata_list:
                collection.insert_many(metadata_list)
            else:
                print("No metadata to insert.")
            return 0
        except Exception as e:
            print(f"Error while forwarding metadata: {e}")
            return 1

    @classmethod
    def close(cls) -> None:
        """
        Closes the MongoDB client connection if it exists.
        """
        if cls.mongoDbClient:
            print("Closing MongoDB client.")
            cls.mongoDbClient.close()
            cls.mongoDbClient = None

    @classmethod
    def _preprocess_metadata(cls, metadata_path: Path) -> list:
        """
        Preprocesses metadata by replacing invalid MongoDB field characters.

        Args:
            metadata_path (Path): The path to the metadata file.

        Returns:
            list: A list of preprocessed metadata records.
        """
        print(f"Preprocessing metadata from: {metadata_path}")
        with metadata_path.open('r', encoding='utf-8') as file:
            metadata_list = json.load(file)
        for metadata in metadata_list:
            if 'metadata' in metadata:
                # Replace invalid field characters (e.g., '.') with valid characters (e.g., '-').
                metadata['metadata'] = {
                    key.replace('.', '-'): value
                    for key, value in metadata['metadata'].items()
                }
        return metadata_list

    @classmethod
    def _get_mongodb_credentials(cls) -> None:
        """
        Retrieves MongoDB connection details from environment variables.
        """
        cls.mongodb_url = os.getenv('MONGODB_URL')
        cls.mongodb_database_name = os.getenv('MONGODB_DATABASE')
        cls.mongodb_collection_name = os.getenv('MONGODB_COLLECTION')

    @classmethod
    def _get_mongodb_collection(cls) -> Collection:
        """
        Returns the MongoDB collection instance, initializing the connection if necessary.

        Returns:
            Collection: The MongoDB collection instance.
        """
        if not cls.mongoDbClient:
            cls._get_mongodb_credentials()
            cls.mongoDbClient = MongoClient(cls.mongodb_url)
            cls.mongoDbCollection = cls.mongoDbClient[cls.mongodb_database_name][cls.mongodb_collection_name]
            # Ensure an index on the "id" field for uniqueness.
            cls.mongoDbCollection.create_index("id", unique=True)
        return cls.mongoDbCollection

    @classmethod
    def count_documents(cls) -> int:
        """
        Counts the number of documents in the MongoDB collection.

        Returns:
            int: The number of documents in the collection.
        """
        try:
            collection = cls._get_mongodb_collection()
            return collection.count_documents({})
        except Exception as e:
            print(f"Error counting documents in MongoDB: {e}")
            return 0

    @classmethod
    def get_metadata_by_id(cls, resource_id: str) -> dict:
        """
        Retrieves metadata for a specific resource by ID.

        Args:
            resource_id (str): The ID of the resource to retrieve metadata for.

        Returns:
            dict: A dictionary containing the metadata fields `language`, `type_recurs`, and `access`.
                  Returns an empty dictionary if no metadata is found.
        """
        # Define the projection for the query to limit retrieved fields.
        projection = {
            "metadata.dc-language-iso": 1,
            "metadata.dc-type": 1,
            "metadata.dc-rights-access": 1,
            "_id": 0
        }
        # Query the MongoDB collection for the specified resource ID.
        result = cls._get_mongodb_collection().find_one({"id": resource_id}, projection)
        return {
            "language": result.get("metadata", {}).get("dc-language-iso"),
            "type_recurs": result.get("metadata", {}).get("dc-type"),
            "access": result.get("metadata", {}).get("dc-rights-access")
        } if result else {}
