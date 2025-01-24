from abc import ABC, abstractmethod  # Import ABC and abstractmethod for defining abstract base classes.

class IForwarder(ABC):
    """
    An abstract base class (ABC) that defines the interface for log forwarders.

    Classes inheriting from `IForwarder` must implement the `forward` method.

    Methods:
        forward(log: dict, raw_log: str) -> int:
            Abstract method to forward log data. Must be implemented by subclasses.
    """

    @abstractmethod
    def forward(cls, log: dict, raw_log: str) -> int:
        """
        Abstract method that subclasses must override to define how logs are forwarded.

        Args:
            log (dict): A dictionary containing parsed log data.
            raw_log (str): The raw log string before parsing.

        Returns:
            int: The status code indicating the result of the forwarding operation.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        # Raise an error to enforce implementation in subclasses.
        raise NotImplementedError("Subclasses must implement this method")
