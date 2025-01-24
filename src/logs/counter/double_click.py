from collections import defaultdict  # Import defaultdict for handling default values in dictionaries.
from datetime import datetime, timedelta  # Import datetime and timedelta for time-based operations.
from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface from the filter module.
from src.logs.utils.date_converter import to_timestamp  # Import the utility function to convert dates to timestamps.

class DoubleClick(IFilter):
    """
    A class to filter out double clicks or repeated accesses within a short time frame.

    Attributes:
        recent_accesses (defaultdict): Tracks recent access times for each unique key (IP, user agent, resource).

    Methods:
        filter(ip_address, date, time, resource, user_agent):
            Determines if the current access should be filtered as a double click.
        _clean_old_entries(current_time):
            Removes outdated entries from the recent accesses dictionary.
    """
    
    recent_accesses = defaultdict(list)  # Tracks access times for unique keys.

    @classmethod
    def filter(cls, ip_address, date, time, resource, user_agent) -> bool:
        """
        Filters out repeated accesses (double clicks) within a 30-second window.

        Args:
            ip_address (str): The IP address of the user.
            date (str): The date of access in a specific format.
            time (str): The time of access in a specific format.
            resource (str): The resource being accessed.
            user_agent (str): The user agent string of the client.

        Returns:
            bool: True if the access is considered a double click, False otherwise.
        """
        # Convert the date and time into a timestamp.
        timestamp = datetime.fromtimestamp(to_timestamp(date, time))
        
        # Create a unique key based on IP, user agent, and resource.
        key = (ip_address, user_agent, resource)
        
        # Remove outdated entries from the recent accesses dictionary.
        cls._clean_old_entries(timestamp)
        
        # Check if the key exists in recent accesses.
        if key in cls.recent_accesses:
            last_access_time = cls.recent_accesses[key][-1]  # Get the last access time for this key.
            
            # If the time difference is within 30 seconds, update the timestamp and return True.
            if timestamp - last_access_time <= timedelta(seconds=30):
                cls.recent_accesses[key][-1] = timestamp
                return True
        
        # Otherwise, add the timestamp for this key and return False.
        cls.recent_accesses[key].append(timestamp)
        return False

    @classmethod
    def _clean_old_entries(cls, current_time):
        """
        Removes entries older than 30 seconds from the recent accesses dictionary.

        Args:
            current_time (datetime): The current time used as a reference to clean old entries.
        """
        # Calculate the threshold time for keeping entries.
        threshold_time = current_time - timedelta(seconds=30)
        
        # List to track keys that need to be deleted.
        keys_to_delete = []
        
        # Iterate over recent accesses and filter timestamps based on the threshold time.
        for key, timestamps in cls.recent_accesses.items():
            cls.recent_accesses[key] = [
                ts for ts in timestamps if ts > threshold_time
            ]
            # If no timestamps remain for the key, mark it for deletion.
            if not cls.recent_accesses[key]:
                keys_to_delete.append(key)
        
        # Remove all keys marked for deletion.
        for key in keys_to_delete:
            del cls.recent_accesses[key]
