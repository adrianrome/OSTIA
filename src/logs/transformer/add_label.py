from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for standardizing transformation behavior.

class AddLabel(ITransformer):
    """
    A transformer class that adds a label and its corresponding value to a log dictionary.

    Methods:
        transform(log: dict, label: str, value: str) -> None:
            Adds the given label and value to the log dictionary.
    """

    @classmethod
    def transform(cls, log: dict, label: str, value: str) -> None:
        """
        Adds a label and its value to the provided log dictionary.

        Args:
            log (dict): The log dictionary to which the label and value will be added.
            label (str): The label (key) to add to the log.
            value (str): The value to associate with the given label.

        Returns:
            None
        """
        # Add the label and its value to the log dictionary.
        log[label] = value
