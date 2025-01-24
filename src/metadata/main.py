from pathlib import Path  # Import Path for handling filesystem paths.
from src.metadata.filter.record_deleted import RecordDeleted  # Import filter to identify deleted records.
from src.metadata.forwarder.filesystem_forwarder import FileSystemForwarder  # Forwarder for writing metadata to the filesystem.
from src.metadata.forwarder.mongodb_forwarder import MongoDbForwarder  # Forwarder for sending metadata to MongoDB.
from src.metadata.oaipmh.oaiclient import OAIClient  # Client for interacting with an OAI-PMH endpoint.
from src.metadata.parser.dim_parser import DimParser  # Parser for metadata transformation.
from src.metadata.utils.constants import SIZE_RECORDS_LIST  # Constant defining the size of metadata batches.
from src.metadata.utils.get_resource_id import get_resource_id  # Utility to extract resource IDs.
import json  # Import json for handling serialization and deserialization.
import os  # Import os for accessing environment variables.
import re  # Import re for regular expression handling.
import requests  # Import requests for HTTP communication.
import time  # Import time for measuring execution time.
import xmltodict  # Import xmltodict for parsing XML responses.

def process_metadata_batch(client: OAIClient, resumptionToken: str | None, batch: int) -> tuple[str, int]:
    """
    Processes a single batch of metadata from the OAI-PMH endpoint.

    Args:
        client (OAIClient): The OAI-PMH client used to retrieve records.
        resumptionToken (str | None): The token to continue fetching records. None for the first request.
        batch (int): The current batch number.

    Returns:
        tuple[str, int]: A tuple containing the next resumption token (or None) and the number of metadata records processed.
    """
    print(f"Processing metadata batch {batch} with resumptionToken: {resumptionToken}")
    metadataList = []
    try:
        # Fetch records using the OAI-PMH client.
        records, resumption_token = client.get_records(resumptionToken=resumptionToken)
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors during record retrieval.
        print(f"HTTP error occurred: {e}")
        return None, 0

    endOfRecords = SIZE_RECORDS_LIST  # Set the number of records to process in this batch.

    while endOfRecords > 0:
        try:
            # Fetch the next record.
            record = records.next()
        except StopIteration:
            # Stop when there are no more records.
            break
        
        # Parse the XML record into a dictionary.
        data = xmltodict.parse(str(record))['record']
        # Skip records marked as deleted.
        if not RecordDeleted.filter(data):
            id = data['header']['identifier']  # Extract the record identifier.
            setSpec = data['header']['setSpec']  # Extract the setSpec information.
            metadata_list = data['metadata']['mets']['dmdSec']['mdWrap']['xmlData']['dim:dim']['dim:field']
            
            # Construct the metadata dictionary.
            metadata = {
                'id': get_resource_id(id),  # Extract the resource ID.
                'identifier': id,
                'setSpec': setSpec,
                'metadata': DimParser.parse(metadata_list)[0]  # Parse the metadata fields.
            }
            metadataList.append(metadata)  # Add the metadata to the list.
        endOfRecords -= 1

    # Forward the processed metadata to the filesystem.
    FileSystemForwarder.forward(metadata_list=metadataList, batch=(batch * int(SIZE_RECORDS_LIST)))
    return resumption_token, len(metadataList)

def get_metadata(client: OAIClient) -> dict:
    """
    Retrieves metadata from the OAI-PMH endpoint in batches.

    Args:
        client (OAIClient): The OAI-PMH client used to retrieve metadata.

    Returns:
        dict: A dictionary containing statistics on the metadata retrieval process.
    """
    print("Starting metadata retrieval")
    stats = {'n_metadata': 0, 'time': 0}  # Initialize statistics.
    iteration = 0
    resumptionToken = None

    while True:
        # Process a batch of metadata.
        resumptionToken, total_metadata = process_metadata_batch(client, resumptionToken=resumptionToken, batch=iteration)
        print(f"Batch {iteration} processed, total metadata: {total_metadata}")
        stats['n_metadata'] += total_metadata

        if iteration % 100 == 0:
            print(f"Metadata track: {iteration * SIZE_RECORDS_LIST}")
        
        # Break the loop if there are no more records.
        if resumptionToken is None:
            break
        
        iteration += 1

    return stats

def process_metadata() -> float:
    """
    Processes metadata from the filesystem and forwards it to MongoDB.

    Returns:
        float: The total time taken to process the metadata, in seconds.
    """
    print("Processing metadata from filesystem")
    base_path = Path(os.environ.get('METADATA_OUTPUT_PATH'))  # Retrieve the base path from environment variables.
    start_time = time.time()  # Record the start time.

    # Iterate through each batch directory in the base path.
    for batch in base_path.iterdir():
        if batch.is_dir():
            print(f"Processing batch: {batch.name}")
            # Process each metadata file in the batch directory.
            for metadata_file in batch.glob("*.metadata.json"):
                print(f"Forwarding metadata file: {metadata_file}")
                MongoDbForwarder.forward(metadata_file)
    
    MongoDbForwarder.close()  # Close the MongoDB connection.
    return time.time() - start_time  # Calculate the total time taken.

def main():
    """
    The main function to control metadata processing.

    Depending on the environment variable `METADATA_IN_SYSTEM`, this function either retrieves metadata 
    from an OAI-PMH endpoint or processes existing metadata files from the filesystem.
    """
    print("Starting main process")
    
    # Check if metadata should be retrieved or processed from the filesystem.
    if int(os.environ.get('METADATA_IN_SYSTEM', 0)) == 0:
        url = os.environ.get('UPCOMMONS_METADATA_URL')
        metadata_prefix = os.environ.get('UPCOMMONS_METADATA_PREFIX')
        
        # Ensure required environment variables are set.
        if not url or not metadata_prefix:
            print("Environment variables UPCOMMONS_METADATA_URL or UPCOMMONS_METADATA_PREFIX are missing.")
            return
        
        # Initialize the OAI-PMH client.
        client = OAIClient(endpoint=url, metadataPrefix=metadata_prefix)
        start_time = time.time()
        
        try:
            stats = get_metadata(client=client)  # Retrieve metadata from the endpoint.
        except requests.exceptions.HTTPError as e:
            print(f"Failed to retrieve metadata due to HTTP error: {e}")
            return
        
        stats['time'] = time.time() - start_time  # Calculate the time taken for metadata retrieval.
        print(json.dumps(stats, indent=4))  # Print retrieval statistics as a JSON object.
    else:
        # Process metadata from the filesystem.
        elapsed_time = process_metadata()
        print(f"Time taken to process metadata: {elapsed_time:.2f} seconds")
    
    # Count and print the total number of documents in MongoDB.
    total_documents = MongoDbForwarder.count_documents()
    print(f"Total documents in MongoDB: {total_documents}")

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly.
