from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for consistent transformer behavior.
from src.logs.utils.regex_patterns import IPV6_PATTERN  # Import the IPV6_PATTERN regex to identify IPv6 addresses.
import re  # Import the re module for regular expression operations.

class RemoveIPv6Address(ITransformer):
    """
    A transformer class that removes IPv6 addresses from a log string.

    Methods:
        transform(log: str) -> str:
            Iteratively removes all occurrences of IPv6 addresses from the given log string.
    """

    @classmethod
    def transform(cls, log: str) -> str:
        """
        Removes all IPv6 addresses from the given log string.

        Args:
            log (str): The log string from which IPv6 addresses will be removed.

        Returns:
            str: The transformed log string with all IPv6 addresses removed.
        """
        # Use a loop to remove all matches of the IPV6_PATTERN from the log string.
        while re.match(IPV6_PATTERN, log):  # Check if the log starts with an IPv6 address.
            log = re.sub(IPV6_PATTERN, "", log)  # Replace the IPv6 address with an empty string.
        return log  # Return the transformed log string.
