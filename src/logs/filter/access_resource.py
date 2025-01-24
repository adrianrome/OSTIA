from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface to enforce filter behavior.
from src.logs.utils.regex_patterns import HANDLE  # Import the HANDLE regex pattern for identifying specific resources.
import re  # Import the re module for regular expression handling.

class AccessResource(IFilter):
    """
    A class to filter and identify resources that match the HANDLE pattern.

    Methods:
        filter(resource: str) -> bool:
            Checks if the provided resource matches the HANDLE regex pattern.
    """

    @classmethod
    def filter(cls, resource: str) -> bool:
        """
        Filters resources based on whether they match the HANDLE regex pattern.

        Args:
            resource (str): The resource string to be evaluated.

        Returns:
            bool: True if the resource matches the HANDLE pattern, False otherwise.
        """
        # Use re.search to check if the HANDLE pattern is found in the resource string.
        return bool(re.search(HANDLE, resource))
