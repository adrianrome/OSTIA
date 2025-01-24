from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface to enforce the transformation structure.

class AddDefaultIpAddress(ITransformer):
    """
    A transformer class that replaces missing IP addresses in logs with a default IP address.

    Attributes:
        WITHOUT_IPADDRESS (str): A constant representing the placeholder for missing IP addresses.
        DEFAULT_IPADDRESS (str): A constant representing the default IP address to replace missing ones.

    Methods:
        transform(log: str) -> str:
            Replaces the first occurrence of the placeholder for missing IP addresses with the default IP address.
    """

    WITHOUT_IPADDRESS = '-'  # Placeholder for logs with no IP address.
    DEFAULT_IPADDRESS = '0.0.0.0'  # Default IP address to use when no IP is present.

    @classmethod
    def transform(cls, log: str) -> str:
        """
        Replaces the first occurrence of the missing IP address placeholder with the default IP address.

        Args:
            log (str): The log entry as a string.

        Returns:
            str: The transformed log entry with the default IP address replacing the placeholder.
        """
        # Replace the first occurrence of WITHOUT_IPADDRESS with DEFAULT_IPADDRESS in the log string.
        return log.replace(cls.WITHOUT_IPADDRESS, cls.DEFAULT_IPADDRESS, 1)
