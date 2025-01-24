from src.metadata.filter.filter_interface import IFilter  # Import the IFilter interface to define a standard filtering structure.
from src.metadata.utils.constants import RECORD_DELETED, HEADER_STATUS_KEY  # Import constants for deleted record status and header key.

class RecordDeleted(IFilter):
    """
    A filter class that checks whether a record has been marked as deleted.

    This filter evaluates the status of a record's header and returns `True` 
    if the record is marked as deleted, based on predefined constants.

    Methods:
        filter(record: dict) -> bool:
            Checks if the given record's status in the header indicates it is deleted.
    """

    @classmethod
    def filter(cls, record: dict) -> bool:
        """
        Determines if the given record has a status of 'deleted'.

        Args:
            record (dict): A dictionary representing the record to be evaluated. 
                The dictionary must contain a 'header' key with a status field.

        Returns:
            bool: True if the record's status matches the `RECORD_DELETED` constant, False otherwise.
        """
        # Check the 'header' field in the record and return True if the status matches `RECORD_DELETED`.
        return record['header'].get(HEADER_STATUS_KEY) == RECORD_DELETED
