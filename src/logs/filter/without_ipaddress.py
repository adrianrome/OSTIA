from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface to standardize the filter structure.

class WithoutIpAddress(IFilter):
    """
    A class to filter logs that do not contain an IP address.

    Attributes:
        WITHOUT_IPADDRESS (str): A constant representing the character used to indicate the absence of an IP address.

    Methods:
        filter(log: str) -> bool:
            Checks if the given log entry starts with the `WITHOUT_IPADDRESS` character.
    """

    WITHOUT_IPADDRESS = '-'  # A constant indicating no IP address is present.

    @classmethod
    def filter(cls, log: str) -> bool:
        """
        Filters logs based on whether they lack an IP address.

        Args:
            log (str): A log entry to be evaluated.

        Returns:
            bool: True if the log starts with the `WITHOUT_IPADDRESS` character, False otherwise.
        """
        # Check if the first character of the log matches the WITHOUT_IPADDRESS constant.
        return log[0] == cls.WITHOUT_IPADDRESS
