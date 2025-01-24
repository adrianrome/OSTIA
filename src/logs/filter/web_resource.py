from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface to ensure a consistent filter structure.
from src.logs.utils.regex_patterns import WEB_EXTENSIONS  # Import the WEB_EXTENSIONS regex pattern for matching web resources.
import re  # Import the re module for regular expression operations.

class WebResource(IFilter):
    """
    A class to filter and identify resources that match specific web-related extensions.

    Methods:
        filter(resource: str) -> bool:
            Checks if the given resource matches the WEB_EXTENSIONS regex pattern.
    """

    @classmethod
    def filter(cls, resource: str) -> bool:
        """
        Filters resources based on whether they match the WEB_EXTENSIONS regex pattern.

        Args:
            resource (str): The resource string to be evaluated.

        Returns:
            bool: True if the resource matches the WEB_EXTENSIONS pattern, False otherwise.
        """
        # Use re.search to check if the WEB_EXTENSIONS pattern matches any part of the resource string.
        return bool(re.search(WEB_EXTENSIONS, resource))
