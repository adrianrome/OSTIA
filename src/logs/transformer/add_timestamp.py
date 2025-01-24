from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for standardized transformation behavior.
import re  # Import the re module for regular expression operations.

class AddTimestamp(ITransformer):
    """
    A transformer class that extracts and adds timestamp information (date and time) from a raw log string to a log dictionary.

    Methods:
        transform(log: dict, raw_log: str) -> None:
            Extracts the date and time from the raw log string using regular expressions and adds them to the log dictionary.
    """

    @classmethod
    def transform(cls, log: dict, raw_log: str) -> None:
        """
        Extracts the date and time from the raw log string and adds them to the log dictionary.

        Args:
            log (dict): The log dictionary where the extracted date and time will be added.
            raw_log (str): The raw log string from which the date and time are extracted.

        Returns:
            None
        """
        # Use a regular expression to extract the date in the format `dd/Mon/yyyy`.
        log['date'] = re.compile(r'\d{1,2}/\w{3}/\d{1,4}').findall(raw_log)[0]
        
        # Use a regular expression to extract the time from the raw log string.
        log['time'] = re.compile(r':(.*)]').findall(raw_log)[0]
