from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface for consistency with the filtering framework.

class StatusCode(IFilter):
    """
    A class to filter HTTP status codes that are not considered successful or cached responses.

    Methods:
        filter(status_code: int) -> bool:
            Determines if the given HTTP status code is neither 200 (OK) nor 304 (Not Modified).
    """

    @classmethod
    def filter(cls, status_code: int) -> bool:
        """
        Filters out HTTP status codes that are not 200 (OK) or 304 (Not Modified).

        Args:
            status_code (int): The HTTP status code to evaluate.

        Returns:
            bool: True if the status code is not 200 or 304, False otherwise.
        """
        # Return True if the status code is neither 200 nor 304; otherwise, return False.
        return status_code != 200 and status_code != 304
