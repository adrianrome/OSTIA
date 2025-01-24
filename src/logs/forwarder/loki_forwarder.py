from requests.adapters import HTTPAdapter  # For managing retries and mounting HTTP requests.
from src.logs.forwarder.forwarder_interface import IForwarder  # Import the abstract forwarder interface.
from src.logs.utils.date_converter import to_nanoseconds  # Utility function to convert date and time to nanoseconds.
from typing import List, Tuple, Dict  # Type hints for list, tuple, and dictionary.
from urllib3.util.retry import Retry  # Retry mechanism for HTTP requests.
import json  # JSON handling for encoding logs.
import os  # For accessing environment variables.
import requests  # For sending HTTP requests.

class LokiForwarder(IForwarder):
    """
    A class for forwarding logs to a Loki instance.

    Attributes:
        loki_url (str | None): The base URL of the Loki service.
        batch (List[Tuple[Dict, str]]): A batch of logs to be forwarded.
        BATCH_SIZE (int): The maximum number of logs in a batch before sending.
        previous_timestamp (int): Tracks the last used timestamp in nanoseconds.
        previous_date (Tuple[str, str]): Tracks the last processed date and time.

    Methods:
        forward(log: dict, raw_log: str) -> int:
            Adds a log entry to the batch and forwards it if the batch is full.
        forward_batch() -> int:
            Processes and sends the current batch of logs to Loki.
        close() -> None:
            Forwards any remaining logs in the batch.
        _set_log_tags(log: dict) -> dict:
            Generates a dictionary of tags for a log entry.
        _ensure_loki_url() -> None:
            Ensures the Loki URL is set, raising an error if not.
        _set_timestamp(date: str, time: str) -> int:
            Converts a date and time to nanoseconds, ensuring unique timestamps.
    """

    loki_url: str | None = None  # Loki instance URL, set dynamically or from the environment.
    batch: List[Tuple[Dict, str]] = []  # A list to hold log entries and their raw strings.
    BATCH_SIZE = 500  # Maximum number of logs in a batch.
    previous_timestamp: int = 0  # Tracks the previous log's timestamp in nanoseconds.
    previous_date: Tuple[str, str] = ('', '')  # Tracks the previous log's date and time.

    @classmethod
    def forward(cls, log: dict, raw_log: str) -> int:
        """
        Adds a log entry to the batch and sends the batch if it reaches the defined size.

        Args:
            log (dict): A dictionary containing structured log data.
            raw_log (str): The raw log string.

        Returns:
            int: 0 if the batch is not full, 1 if there was an error during forwarding.
        """
        cls.batch.append((log, raw_log))  # Add the log entry to the batch.
        return cls.forward_batch() if len(cls.batch) >= cls.BATCH_SIZE else 0

    @classmethod
    def forward_batch(cls) -> int:
        """
        Processes and sends the current batch of logs to Loki.

        Returns:
            int: 0 if the batch was successfully forwarded, 1 otherwise.
        """
        cls._ensure_loki_url()  # Ensure the Loki URL is set.

        try:
            # Create log streams with associated tags and values.
            streams = [
                {
                    'stream': cls._set_log_tags(log),
                    'values': [[
                        str(cls._set_timestamp(log['date'], log['time'])),
                        json.dumps({
                            "log": raw_log,
                            **({"recurs": log.get("resource")} if log.get("type") in ["recurs", "recurs-bitstream"] else {})
                        })
                    ]]
                }
                for log, raw_log in cls.batch
            ]
        except Exception as e:
            print(f"Error processing batch: {e}")
            return 1

        # Configure HTTP session with retries.
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            # Send the batch to Loki.
            response = session.post(f"{cls.loki_url}/loki/api/v1/push", json={'streams': streams})
            if response.status_code != 204:
                print(f"Status code: {response.status_code}, Response: {response.content.decode('utf-8')}")
                return 1
        except requests.exceptions.RequestException as e:
            print(f"Error sending logs to Loki: {e}")
            return 1

        cls.batch.clear()  # Clear the batch after successful forwarding.
        return 0

    @classmethod
    def close(cls) -> None:
        """
        Forwards any remaining logs in the batch before shutting down.
        """
        if cls.batch:  # Check if there are logs left in the batch.
            cls.forward_batch()

    @staticmethod
    def _set_log_tags(log: dict) -> dict:
        """
        Generates a dictionary of tags for a log entry.

        Args:
            log (dict): The structured log data.

        Returns:
            dict: A dictionary of tags based on the log's content.
        """
        tags = {'service_name': 'log-upcommons', 'content': log['content']}  # Base tags.
        if log['content'] == "error":  # Special case for error logs.
            return tags

        # Add additional tags for non-error logs.
        tags.update({
            'method': log['request']['method'],
            'referer': log['referer'],
            'status_code': log['request']['status_code'],
            'type': log['type'],
        })

        # Add optional keys if they exist in the log.
        optional_keys = ['language', 'type_recurs', 'access']
        tags.update({key: log[key] for key in optional_keys if key in log})
        return tags

    @classmethod
    def _ensure_loki_url(cls) -> None:
        """
        Ensures the Loki URL is set, retrieving it from the environment if necessary.

        Raises:
            ValueError: If the Loki URL is not set.
        """
        if not cls.loki_url:
            cls.loki_url = os.environ.get('LOKI_URL') or \
                ValueError("LOKI_URL environment variable is not set")

    @classmethod
    def _set_timestamp(cls, date: str, time: str) -> int:
        """
        Converts a date and time to nanoseconds, ensuring unique timestamps.

        Args:
            date (str): The date string.
            time (str): The time string.

        Returns:
            int: A timestamp in nanoseconds.
        """
        if (date, time) == cls.previous_date:
            cls.previous_timestamp += 1  # Increment the timestamp to ensure uniqueness.
        else:
            cls.previous_timestamp = to_nanoseconds(date, time)  # Convert to nanoseconds.
            cls.previous_date = (date, time)  # Update the previous date and time.
        return cls.previous_timestamp
