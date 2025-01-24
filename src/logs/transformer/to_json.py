from src.logs.transformer.transformer_interface import ITransformer  # Import the ITransformer interface for consistent transformer behavior.
from typing import Any  # Import Any for type annotations of dynamic data.
from urllib.parse import urlparse  # Import urlparse for parsing URLs.
import re  # Import the re module for regular expression operations.

class ToJSON(ITransformer):
    """
    A transformer class that converts a raw log string into a structured JSON-like dictionary.

    Methods:
        transform(log: str) -> tuple[dict[str, str | dict[str, str | Any]], int]:
            Transforms a raw log string into a structured dictionary and identifies parsing issues with a status code.
    """

    @classmethod
    def transform(cls, log: str) -> tuple[dict[str, str | dict[str, str | Any]], int]:
        """
        Converts a raw log string into a structured JSON-like dictionary and identifies parsing status.

        Args:
            log (str): The raw log string to transform.

        Returns:
            tuple: A tuple containing:
                - dict: A structured dictionary with log details (e.g., IP address, date, request details).
                - int: A status code (0 for success, -1 if parsing issues were encountered).
        """
        status = 0  # Default status code indicating successful parsing.

        # Extract identification section (IP, date, and time) from the log.
        identification = re.compile(r'(^\d.*]) \"').findall(log)[0]

        # Extract the main body of the log entry.
        body = re.compile(r'(\".*)').findall(log)[0]

        # Extract the IP address from the identification section.
        ip = re.match(r'([0-9]+\.){3}[0-9]+', identification).group()

        # Extract the date in the format dd/Mon/yyyy.
        date_match = re.search(r'\d{1,2}/\w{3}/\d{1,4}', identification)
        date = date_match.group()

        # Extract the time with timezone information.
        time_match = re.search(r':(\d{2}:\d{2}:\d{2} [+-]\d{4})\]', identification)
        time = time_match.group(1)

        # Extract HTTP description and split it into its components.
        http_description = re.compile(r'"([^"]*)"').findall(body)
        http_request = re.compile(r'(\S+)').findall(http_description[0])

        # Handle parsing issues when the HTTP request does not match expected format.
        if len(http_request) != 3 or "HTTP" not in http_request[2]:
            http_description = [
                re.compile(r'"(.*HTTP\/\d.\d)"').findall(body)[0],
                re.compile(r'\s(-|\d+) "(.*)" ').findall(body)[0][1],
                re.compile(r'"\s"(.*)(|")$').findall(body)[0][0]
            ]
            http_request = re.compile(r'(^[A-Z]+)\s(.*)\s(HTTP\/\d.\d)$').findall(http_description[0])[0]
            status = -1  # Set status to -1 to indicate parsing issues.

        # Extract HTTP request details.
        http_request_method = http_request[0]
        http_request_resource = http_request[1]
        http_protocol_version = http_request[2]

        # Extract HTTP referer details.
        http_referer_url = http_description[1]
        http_referer_domain = urlparse(http_referer_url).netloc if http_referer_url != "-" else "-"

        # Extract user agent information.
        http_user_agent = http_description[2]

        # Extract HTTP status code and response size.
        http_request_status_code = re.compile(r' (\d+) (-|\d+) ').findall(body)[0][0]
        http_request_response_size = re.compile(r' (\d+) (-|\d+) ').findall(body)[0][1]

        # Construct the structured JSON-like dictionary.
        log_json = {
            'ip_address': ip,
            'date': date,
            'time': time,
            'request': {
                'method': http_request_method,
                'resource': http_request_resource,
                'version': http_protocol_version,
                'status_code': http_request_status_code,
                'response_size': http_request_response_size
            },
            'referer': http_referer_domain,
            'user_agent': http_user_agent
        }

        # Return the structured log dictionary and the status code.
        return log_json, status
