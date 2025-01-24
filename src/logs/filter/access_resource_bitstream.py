from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface for standardizing filter operations.
from src.logs.utils.regex_patterns import HANDLE_BITSTREAM  # Import the HANDLE_BITSTREAM regex pattern for matching specific resources.
import re  # Import the re module for handling regular expression operations.

class AccessResourceBitstream(IFilter):
    """
    A class to filter and identify resources that match the HANDLE_BITSTREAM pattern.

    Methods:
        filter(resource: str) -> bool:
            Checks if the provided resource matches the HANDLE_BITSTREAM regex pattern.
    """

    @classmethod
    def filter(cls, resource: str) -> bool:
        """
        Filters resources based on whether they match the HANDLE_BITSTREAM regex pattern.

        Args:
            resource (str): The resource string to be evaluated.

        Returns:
            bool: True if the resource matches the HANDLE_BITSTREAM pattern, False otherwise.
        """
        # Use the re.search method to check if the HANDLE_BITSTREAM pattern is found in the resource.
        return bool(re.search(HANDLE_BITSTREAM, resource))
