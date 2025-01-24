from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface for enforcing a standard filter structure.
from src.logs.utils.regex_patterns import SEARCH_KEYS  # Import the SEARCH_KEYS list, which contains keys to filter resources.

class SearchResource(IFilter):
    """
    A class to filter and identify resources that contain specific search keys.

    Methods:
        filter(resource: str) -> bool:
            Checks if any of the predefined search keys are present in the provided resource string.
    """

    @classmethod
    def filter(cls, resource: str) -> bool:
        """
        Filters resources based on the presence of predefined search keys.

        Args:
            resource (str): The resource string to be evaluated.

        Returns:
            bool: True if any search key from `SEARCH_KEYS` is found in the resource string, False otherwise.
        """
        # Check if any key from the SEARCH_KEYS list exists in the resource string.
        return any(key in resource for key in SEARCH_KEYS)
