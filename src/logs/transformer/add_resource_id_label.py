from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface to standardize the transformer behavior.
from src.logs.utils.regex_patterns import HANDLE  # Import the HANDLE regex pattern to extract resource IDs.
import re  # Import the re module for regular expression operations.

class AddResourceIdLabel(ITransformer):
    """
    A transformer class that adds a 'resource' label to logs by extracting a resource ID from the provided resource string.

    Methods:
        transform(log: dict, resource: str) -> None:
            Extracts a resource ID using the HANDLE regex pattern and adds it to the log dictionary.
    """

    @classmethod
    def transform(cls, log: dict, resource: str) -> None:
        """
        Extracts a resource ID from the given resource string and adds it to the log.

        If the HANDLE regex pattern matches a portion of the resource string, the extracted value is 
        added to the log dictionary under the key 'resource'.

        Args:
            log (dict): The log dictionary to which the resource ID will be added.
            resource (str): The resource string from which the ID is extracted.

        Returns:
            None
        """
        # Search for the HANDLE pattern in the resource string.
        match = re.search(HANDLE, resource)
        
        # If a match is found, add the first group from the match to the log dictionary as 'resource'.
        if match:
            log['resource'] = match.group(1)
