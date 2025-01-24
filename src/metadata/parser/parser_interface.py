from abc import ABC, abstractmethod  # Import ABC and abstractmethod to define an abstract base class.

class IParser(ABC):
    """
    An abstract base class (ABC) that defines the interface for metadata parsers.

    This interface ensures that all parser classes implement the `parse` method to
    standardize how metadata is processed and transformed.

    Methods:
        parse(metadata: dict) -> list[dict]:
            Abstract method to parse metadata into a structured format.
    """

    @abstractmethod
    def parse(cls, metadata: dict) -> list[dict]:
        """
        Parses the provided metadata into a standardized format.

        Args:
            metadata (dict): A dictionary containing metadata to be processed. 
                The structure and keys of this dictionary will depend on the implementation.

        Returns:
            list[dict]: A list of dictionaries representing the parsed metadata.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        # Raise an error to enforce implementation in subclasses.
        raise NotImplementedError(f"{cls.__name__} must implement the 'parse' method.")
