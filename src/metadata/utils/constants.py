# Constants for metadata processing.

RECORD_DELETED = "deleted"  
"""
str: A constant representing the status of a deleted record. 
Used to identify records marked as deleted in metadata headers.
"""

HEADER_STATUS_KEY = "@status"
"""
str: A constant representing the key for the status field in metadata headers.
This key is used to check the status of a record (e.g., active or deleted).
"""

SIZE_RECORDS_LIST = 100
"""
int: The default size for a batch of records. 
Used for splitting large sets of metadata into manageable chunks during processing.
"""
