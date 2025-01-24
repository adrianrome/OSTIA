from abc import ABC, abstractmethod  # Import ABC and abstractmethod for defining an abstract base class.

class IFilter(ABC):
    """
    An abstract base class (ABC) that defines the interface for log filters.

    Classes inheriting from `IFilter` must implement the `filter` method.

    Methods:
        filter(log: str) -> bool:
            Abstract method that must be implemented by subclasses to define 
            filtering logic for log entries.
    """

    @abstractmethod
    def filter(cls, log: str) -> bool:
        """
        Abstract method that subclasses must override to implement specific filtering logic.

        Args:
            log (str): A log entry to be evaluated.

        Returns:
            bool: The result of the filtering operation. True if the log meets the filter criteria, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        # Raise an error to enforce implementation in subclasses.
        raise NotImplementedError("Subclasses must implement this method")
