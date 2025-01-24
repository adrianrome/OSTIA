from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for defining the transformation structure.
from src.logs.utils.regex_patterns import HANDLE_BITSTREAM  # Import the HANDLE_BITSTREAM regex for extracting bitstream resource IDs.
import re  # Import the re module for regular expression operations.

class AddBitstreamResourceIdLabel(ITransformer):
    """
    A transformer class that adds a 'resource' label to logs by extracting
    a bitstream resource ID from the given resource string.

    Methods:
        transform(log: dict, resource: str) -> None:
            Extracts the bitstream resource ID from the resource string and
            adds it to the log dictionary under the 'resource' key.
    """

    @classmethod
    def transform(cls, log: dict, resource: str) -> None:
        """
        Extracts a bitstream resource ID from the resource string and adds it to the log.

        Args:
            log (dict): The log dictionary to which the resource ID will be added.
            resource (str): The resource string from which the bitstream ID is extracted.

        Returns:
            None
        """
        # Search for the HANDLE_BITSTREAM pattern in the resource string.
        match = re.search(HANDLE_BITSTREAM, resource)
        
        # If a match is found, extract the first group from the regex match and add it to the log.
        if match:
            log['resource'] = match.group(1)
