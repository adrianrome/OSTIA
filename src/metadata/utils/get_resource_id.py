from src.metadata.utils.regex_patterns import HANDLE  # Import the regex pattern for resource identifiers.
import re  # Import the re module for regular expression operations.

def get_resource_id(resource_identifier: str) -> str:
    """
    Extracts the resource ID from a given resource identifier string.

    This function uses a regular expression defined in `HANDLE` to extract the
    resource ID from the provided string. If no match is found, a `ValueError` 
    is raised.

    Args:
        resource_identifier (str): The string containing the resource identifier.

    Returns:
        str: The extracted resource ID.

    Raises:
        ValueError: If the resource ID cannot be found in the input string.
    """
    # Use the HANDLE regex pattern to search for the resource ID in the input string.
    match = re.search(HANDLE, resource_identifier)
    
    if match:
        # If a match is found, return the first captured group as the resource ID.
        return match.group(1)
    
    # Raise an exception if the resource ID cannot be extracted.
    raise ValueError(f"Resource ID not found in: {resource_identifier}")
