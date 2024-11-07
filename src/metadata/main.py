from src.metadata.oaipmh.oaiclient import OAIClient

from src.metadata.parser.dim_parser import DimParser

from src.metadata.filter.record_deleted import RecordDeleted

from src.metadata.forwarder.mongodb_forwarder import MongoDbForwarder
from src.metadata.forwarder.filesystem_forwarder import FileSystemForwarder

from src.metadata.utils.get_resource_id import get_resource_id
from src.metadata.utils.constants import SIZE_RECORDS_LIST

import os
import re
import json
import time
import xmltodict
from pathlib import Path
import requests


def process_metadata_batch(client: OAIClient, resumptionToken: str | None, batch: int) -> tuple[str, int]:
    print(f"Processing metadata batch {batch} with resumptionToken: {resumptionToken}")
    metadataList = []
    try:
        records, resumption_token = client.get_records(resumptionToken=resumptionToken)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None, 0
    print(f"Received records: {records}, resumption_token: {resumption_token}")

    endOfRecords = SIZE_RECORDS_LIST
    while endOfRecords > 0:

        try:
            record = records.next()

        except StopIteration:
            break

        data = xmltodict.parse(str(record))['record']
        print(f"Parsed record: {data}")

        if not RecordDeleted.filter(data):

            id = data['header']['identifier']
            setSpec = data['header']['setSpec']
            metadata_list = data['metadata']['mets']['dmdSec']['mdWrap']['xmlData']['dim:dim']['dim:field']

            metadata = {
                'id': get_resource_id(id),
                'identifier': id,
                'setSpec': setSpec,
                'metadata': DimParser.parse(metadata_list)[0]
            }
            metadataList.append(metadata)
            print(f"Appended metadata: {metadata}")

        endOfRecords = endOfRecords - 1

    FileSystemForwarder.forward(metadata_list=metadataList, batch=(batch * int(SIZE_RECORDS_LIST)))
    print(f"Forwarded metadata list: {metadataList}")

    return resumption_token, len(metadataList)


def get_metadata(client: OAIClient) -> dict:
    print("Starting metadata retrieval")
    stats = {'n_metadata': 0, 'time': 0}

    iteration = 0
    emptyMetadata = False
    resumptionToken = None
    while not emptyMetadata:
        resumptionToken, total_metadata = process_metadata_batch(client, resumptionToken=resumptionToken, batch=iteration)
        print(f"Batch {iteration} processed, total metadata: {total_metadata}")

        stats['n_metadata'] = stats['n_metadata'] + total_metadata
        if iteration % 100:
            print('metadata track: ', int(iteration * SIZE_RECORDS_LIST))

        emptyMetadata = resumptionToken is None
        iteration = iteration + 1

    return stats


def process_metadata() -> float:
    print("Processing metadata from filesystem")
    base_path = Path(os.environ.get('METADATA_OUTPUT_PATH'))

    start_time = time.time()
    for batch in base_path.iterdir():
        print(f"Processing batch: {batch.name}")
        if batch.is_dir():
            for metadata_file in batch.iterdir():
                if re.match(pattern=r'.*\/\d+_\d+\.metadata.json', string=str(metadata_file)):
                    print(f"Forwarding metadata file: {metadata_file}")
                    MongoDbForwarder.forward(metadata_file)
    MongoDbForwarder.close()
    end_time = time.time()

    return end_time - start_time

def main():
    print("Starting main process")
    METADATA_IN_SYSTEM = int(os.environ.get('METADATA_IN_SYSTEM'))

    if not METADATA_IN_SYSTEM:

        URL = os.environ.get('UPCOMMONS_METADATA_URL')
        METADATA_PREFIX = os.environ.get('UPCOMMONS_METADATA_PREFIX')

        client = OAIClient(endpoint=URL, metadataPrefix=METADATA_PREFIX)

        start_time = time.time()
        stats = get_metadata(client=client)
        if stats is None:
            print("Failed to retrieve metadata due to HTTP error.")
            return
        end_time = time.time()

        stats['time'] = (end_time - start_time)
        print(json.dumps(stats, indent=4))

    else:
        t = process_metadata()
        print(f'time: {t}')

if __name__ == "__main__":
    main()