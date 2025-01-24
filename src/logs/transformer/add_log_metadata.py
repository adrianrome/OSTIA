from functools import lru_cache  # Import lru_cache to cache results of metadata retrieval for efficiency.
from src.logs.transformer.add_label import AddLabel  # Import AddLabel for adding labels to the log.
from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for standardization.
from src.metadata.forwarder.mongodb_forwarder import MongoDbForwarder  # Import MongoDbForwarder to fetch metadata.

class AddLogMetadata(ITransformer):
    """
    A transformer class that enriches logs with metadata from an external database.

    Methods:
        get_metadata(resource: str) -> dict:
            Retrieves metadata for a given resource, using caching to improve performance.

        transform(log: dict, resource: str) -> dict:
            Enriches a log dictionary with metadata by mapping metadata keys to specific log labels.
    """

    @classmethod
    @lru_cache(maxsize=1024)
    def get_metadata(cls, resource: str) -> dict:
        """
        Retrieves metadata for a given resource from the MongoDB forwarder.

        Args:
            resource (str): The identifier of the resource for which metadata is fetched.

        Returns:
            dict: A dictionary containing metadata for the resource. Returns an empty dictionary if no metadata is found.
        """
        # Fetch metadata using the MongoDbForwarder. If none is found, return an empty dictionary.
        return MongoDbForwarder.get_metadata_by_id(resource) or {}

    @classmethod
    def transform(cls, log: dict, resource: str) -> dict:
        """
        Enriches the given log dictionary with metadata.

        Metadata keys are mapped to specific log labels using a predefined mapping. 
        If metadata for a key exists, it is added to the log using the `AddLabel` transformer.

        Args:
            log (dict): The log dictionary to enrich with metadata.
            resource (str): The resource identifier for retrieving metadata.

        Returns:
            dict: The enriched log dictionary.
        """
        # Fetch metadata for the given resource.
        metadata = cls.get_metadata(resource)

        # Define the mapping of metadata keys to log labels.
        label_mapping = {
            'language': 'language',
            'type_recurs': 'type_recurs',
            'access': 'access'
        }

        # Iterate over the mapping and add metadata values to the log if they exist.
        for meta_key, label in label_mapping.items():
            if meta_value := metadata.get(meta_key):  # Retrieve the metadata value if it exists.
                AddLabel.transform(log, label, meta_value)  # Add the metadata value to the log using AddLabel.

        return log  # Return the enriched log.
