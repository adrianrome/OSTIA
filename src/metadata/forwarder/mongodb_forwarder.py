from src.metadata.forwarder.forwarder_interface import IForwarder

import os
import json
from pathlib import Path
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDbForwarder(IForwarder):

    mongodb_url: Optional[str] = None
    mongodb_database_name: Optional[str] = None
    mongodb_collection_name: Optional[str] = None

    mongoDbClient: Optional[MongoClient] = None
    mongoDbCollection: Optional[Collection] = None

    @classmethod
    def forward(cls, metadata_path: Path) -> int:
        """
        Forwards the metadata list located in the *metadata_path* to *MongoDB*.

        :param metadata_path: Directory where the metadata is stored.
        :type metadata_path: Path
        :return: Status code of the action.
        :rtype: int
        """
        print(f"Forwarding metadata from path: {metadata_path}")
        collection = cls._get_mongodb_collection()
        metadata_list = cls._preprocess_metadata(metadata_path)
        print(f"Metadata list to insert: {metadata_list}")
        collection.insert_many(metadata_list)

        return 0

    @classmethod
    def close(cls) -> None:
        """
        Close the *MongoDB* client.

        :return: None
        """
        print("Closing MongoDB client")
        if cls.mongoDbClient is not None:
            cls.mongoDbClient.close()

    @classmethod
    def _preprocess_metadata(cls, metadata_path: Path) -> list:
        """
        Adapt the metadata key to be supported by MongoDB

        :param metadata_path: Directory where the metadata is stored.
        :type metadata_path: Path
        :return: List of metadata entries where the key does NOT contain a dot (.).
        :rtype: list
        """
        print(f"Preprocessing metadata from path: {metadata_path}")
        with open(metadata_path, 'r', encoding='utf-8') as file:
            metadata_list = json.load(file)
            for metadata in metadata_list:
                if 'metadata' in metadata:
                    updated_metadata = {}
                    for key, value in metadata['metadata'].items():
                        updated_key = key.replace('.', '-')
                        updated_metadata[updated_key] = value
                    metadata['metadata'] = updated_metadata
        print(f"Preprocessed metadata list: {metadata_list}")
        return metadata_list

    @classmethod
    def _get_mongodb_credentials(cls) -> None:
        """
        Obtains the *MongoDB* credentials from environment variables.

        :return: None
        """
        print("Getting MongoDB credentials from environment variables")
        cls.mongodb_url = os.environ.get('MONGODB_URL')
        cls.mongodb_database_name = os.environ.get('MONGODB_DATABASE')
        cls.mongodb_collection_name = os.environ.get('MONGODB_COLLECTION')

    @classmethod
    def _get_mongodb_collection(cls) -> Collection:
        """
        Obtains the *MongoDB* collection where the metadata will be stored.

        :return: *MongoDB*'s metadata collection.
        :rtype: Collection
        """
        if cls.mongoDbClient is None:
            cls._get_mongodb_credentials()
            print(f"Connecting to MongoDB at {cls.mongodb_url}")
            cls.mongoDbClient = MongoClient(cls.mongodb_url)
            cls.mongoDbCollection = cls.mongoDbClient[cls.mongodb_database_name][cls.mongodb_collection_name]

        return cls.mongoDbCollection
