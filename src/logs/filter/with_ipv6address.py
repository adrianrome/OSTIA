from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface to define a standardized filter structure.
from src.logs.utils.regex_patterns import IPV6_PATTERN  # Import the IPV6_PATTERN regex for identifying IPv6 addresses.
import re  # Import the re module for regular expression matching.

class WithIPv6Address(IFilter):
    """
    A class to filter logs that contain IPv6 addresses.

    Methods:
        filter(log: str) -> bool:
            Checks if the given log entry contains an IPv6 address using the IPV6_PATTERN regex.
    """

    @classmethod
    def filter(cls, log: str) -> bool:
        """
        Filters logs based on whether they contain an IPv6 address.

        Args:
            log (str): A log entry to be evaluated.

        Returns:
            bool: True if an IPv6 address is found in the log entry, False otherwise.
        """
        # Use re.search to check if the log contains a match for the IPV6_PATTERN regex.
        return bool(re.search(IPV6_PATTERN, log))
