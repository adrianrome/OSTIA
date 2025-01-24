from abc import ABC, abstractmethod  # Import ABC and abstractmethod for defining an abstract base class.

class IForwarder(ABC):
    """
    An abstract base class (ABC) that defines the interface for forwarders.

    Forwarders are responsible for sending or saving data, and all implementations
    of this interface must define the `forward` method.

    Methods:
        forward(data: dict) -> int:
            Abstract method that subclasses must implement to define how data is forwarded.
    """

    @abstractmethod
    def forward(self, data: dict) -> int:
        """
        Sends or processes the given data.

        Args:
            data (dict): The data to be forwarded. The specific structure of the dictionary 
                will depend on the implementation.

        Returns:
            int: An integer indicating the result of the forwarding operation. A return value
                of `0` typically indicates success, while other values may indicate errors.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass  # Placeholder indicating subclasses must override this method.
