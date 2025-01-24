from sickle import Sickle  # Import Sickle for interacting with OAI-PMH endpoints.
from typing import Any, Optional, Iterator  # Import type hints for better code clarity.
import json  # Import json for potential serialization of records (not used here).
import os  # Import os for environment variable access (not used here).
import xmltodict  # Import xmltodict for processing XML responses (not used here).

class OAIClient:
    """
    A client for interacting with an OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting) endpoint.

    This client provides functionality to fetch records from the specified endpoint using the `Sickle` library.

    Attributes:
        url (str): The URL of the OAI-PMH endpoint.
        prefix (str): The metadata format prefix for the records.
        client (Sickle): An instance of the `Sickle` client for OAI-PMH operations.

    Methods:
        __init__(endpoint: str, metadataPrefix: str) -> None:
            Initializes the OAIClient with the specified endpoint and metadata prefix.
        get_records(resumptionToken: Optional[str]) -> tuple[Iterator, Optional[str]]:
            Fetches records from the OAI-PMH endpoint, optionally using a resumption token.
    """

    def __init__(self, endpoint: str, metadataPrefix: str) -> None:
        """
        Initializes the OAIClient with the specified endpoint and metadata prefix.

        Args:
            endpoint (str): The URL of the OAI-PMH endpoint.
            metadataPrefix (str): The metadata format prefix (e.g., "oai_dc").
        """
        self.url = endpoint  # Store the OAI-PMH endpoint URL.
        self.prefix = metadataPrefix  # Store the metadata format prefix.
        self.client = Sickle(endpoint)  # Initialize the Sickle client with the endpoint.

    def get_records(self, resumptionToken: Optional[str]) -> tuple[Iterator, Optional[str]]:
        """
        Fetches records from the OAI-PMH endpoint.

        If a `resumptionToken` is provided, it will continue fetching records from where the previous request left off.
        If no `resumptionToken` is provided, it will fetch records using the specified metadata prefix.

        Args:
            resumptionToken (Optional[str]): The resumption token for continuing a previous request. 
                If None, the request starts from the beginning using the metadata prefix.

        Returns:
            tuple[Iterator, Optional[str]]:
                - An iterator over the fetched records.
                - The next resumption token, if available; otherwise, None.
        """
        # Use the resumption token if provided; otherwise, use the metadata prefix.
        records = self.client.ListRecords(
            metadataPrefix=self.prefix if resumptionToken is None else None,
            resumptionToken=resumptionToken
        )
        # Extract the next resumption token, if available.
        return records, getattr(records.resumption_token, "token", None)
