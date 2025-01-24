from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface for standardizing filters.
from src.logs.utils.regex_patterns import BITSTREAM  # Import the BITSTREAM regex pattern for matching bitstream URLs.
import re  # Import the `re` module for regular expression operations.

class AccessBitstream(IFilter):
    """
    A class to filter and identify resources that match a bitstream pattern.

    Methods:
        filter(resource: str) -> bool:
            Determines if the given resource matches the defined BITSTREAM pattern.
    """

    @classmethod
    def filter(cls, resource: str) -> bool:
        """
        Filters resources based on whether they match the BITSTREAM regex pattern.

        Args:
            resource (str): The resource string to be evaluated.

        Returns:
            bool: True if the resource matches the BITSTREAM pattern, False otherwise.
        """
        # Perform a regular expression search using the BITSTREAM pattern on the provided resource.
        return bool(re.search(BITSTREAM, resource))
