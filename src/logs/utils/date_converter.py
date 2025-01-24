from datetime import datetime  # Import the datetime module for handling date and time conversions.

def to_iso_format(date: str, time: str) -> tuple[str, str]:
    """
    Converts a given date and time into ISO 8601 format.

    Args:
        date (str): The date string in the format '%d/%b/%Y' (e.g., '01/Jan/2023').
        time (str): The time string in the format '%H:%M:%S %z' (e.g., '12:34:56 +0000').

    Returns:
        tuple[str, str]: A tuple containing the date in ISO format (YYYY-MM-DD) and time in ISO format (HH:MM:SS+TZ).
    """
    # Convert the date string to ISO 8601 format (YYYY-MM-DD).
    date_iso = datetime.strptime(date, '%d/%b/%Y').date().isoformat()
    
    # Convert the time string to ISO 8601 format (HH:MM:SS+TZ).
    time_iso = datetime.strptime(time, '%H:%M:%S %z').time().isoformat()
    
    return date_iso, time_iso  # Return the date and time in ISO format as a tuple.

def to_timestamp(date: str, time: str) -> int:
    """
    Converts a given date and time into a UNIX timestamp (seconds since epoch).

    Args:
        date (str): The date string in the format '%d/%b/%Y' (e.g., '01/Jan/2023').
        time (str): The time string in the format '%H:%M:%S %z' (e.g., '12:34:56 +0000').

    Returns:
        int: The UNIX timestamp in seconds.
    """
    # Combine the date and time strings, parse them, and convert to a UNIX timestamp.
    return int(datetime.strptime(date + ' ' + time, '%d/%b/%Y %H:%M:%S %z').timestamp())

def to_nanoseconds(date: str, time: str) -> int:
    """
    Converts a given date and time into a UNIX timestamp in nanoseconds.

    Args:
        date (str): The date string in the format '%d/%b/%Y' (e.g., '01/Jan/2023').
        time (str): The time string in the format '%H:%M:%S %z' (e.g., '12:34:56 +0000').

    Returns:
        int: The UNIX timestamp in nanoseconds.
    """
    # Convert the date and time to seconds since epoch and multiply by 1e9 to get nanoseconds.
    return int(to_timestamp(date, time) * 1e9)
