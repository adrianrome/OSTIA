from abc import ABC, abstractmethod  # Import ABC and abstractmethod to define an abstract base class.

class IFilter(ABC):
    """
    An abstract base class (ABC) that defines the interface for filters.

    Classes inheriting from `IFilter` must implement the `filter` method. 
    This interface is used to ensure consistency across all filter implementations.

    Methods:
        filter(record: dict) -> bool:
            Abstract method that subclasses must override to define the filtering logic.
    """

    @abstractmethod
    def filter(cls, record: dict) -> bool:
        """
        Abstract method to filter records based on custom criteria.

        Args:
            record (dict): A dictionary representing the record to be evaluated.

        Returns:
            bool: True if the record satisfies the filter criteria, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        # Raise an error to enforce implementation in subclasses.
        raise NotImplementedError(f"{cls.__name__} must implement the 'filter' method.")
