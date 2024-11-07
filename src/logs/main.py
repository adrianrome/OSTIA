from src.logs.filter.web_resource import WebResource
from src.logs.filter.search_resource import SearchResource
from src.logs.filter.access_resource import AccessResource
from src.logs.filter.with_ipv6address import WithIPv6Address
from src.logs.filter.without_ipaddress import WithoutIpAddress
from src.logs.filter.access_resource_bitstream import AccessResourceBitstream

from src.logs.transformer.to_json import ToJSON
from src.logs.transformer.add_label import AddLabel
from src.logs.transformer.add_timestamp import AddTimestamp
from src.logs.transformer.remove_ipv6address import RemoveIPv6Address
from src.logs.transformer.add_resource_id_label import AddResourceIdLabel
from src.logs.transformer.add_default_ipaddress import AddDefaultIpAddress

from src.logs.forwarder.loki_forwarder import LokiForwarder

from src.logs.utils.constants import LABEL_VALUE
from src.logs.utils.constants import LABEL_TYPE, LABEL_TYPE_OTHERS, LABEL_TYPE_SEARCH, LABEL_TYPE_RESOURCE, LABEL_TYPE_RESOURCE_WEB
from src.logs.utils.constants import LABEL_CONTENT, LABEL_CONTENT_OK, LABEL_CONTENT_ERROR, LABEL_CONTENT_DIFFERENT

import os
import json
import time
import gzip
from pathlib import Path

YEAR_START = 2006
YEAR_END = 2023
BATCH_SIZE = 1000
INPUT_PATH = os.environ.get('LOGS_OUTPUT_PATH', '').strip()

def process_log(line: str) -> tuple[dict, dict]:
    log = {}
    stats = {}

    if WithoutIpAddress.filter(line):
        line = AddDefaultIpAddress.transform(line)
    elif WithIPv6Address.filter(line):
        line = RemoveIPv6Address.transform(line)

    try:
        log, status = ToJSON.transform(line)
        resource = log['request']['resource']
    except Exception as e:
        log = {LABEL_VALUE: line, LABEL_CONTENT: LABEL_CONTENT_ERROR}
        try:
            AddTimestamp.transform(log, line)
        except Exception as e:
            print(f"Error processing log: {e}")
        stats[LABEL_CONTENT] = LABEL_CONTENT_ERROR
        return log, stats

    AddLabel.transform(log, LABEL_CONTENT, LABEL_CONTENT_OK if status == 0 else LABEL_CONTENT_DIFFERENT)

    if AccessResource.filter(resource):
        AddResourceIdLabel.transform(log, resource)
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_RESOURCE)
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE
    elif AccessResourceBitstream.filter(resource):
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_RESOURCE)
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE
    elif WebResource.filter(resource):
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE_WEB
        log[LABEL_TYPE] = LABEL_TYPE_RESOURCE_WEB
        return log, stats
    elif SearchResource.filter(resource):
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_SEARCH)
        stats[LABEL_TYPE] = LABEL_TYPE_SEARCH
    else:
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_OTHERS)
        stats[LABEL_TYPE] = LABEL_TYPE_OTHERS

    log[LABEL_TYPE] = stats[LABEL_TYPE]
    return log, stats

def process_logs_for_date(year: int, month: int, day: int, folder: Path, batch: list, monthly_stats: dict) -> int:
    log_file = folder / Path(f'anon_upc_access_log.{year}-{month:02}-{day:02}.txt.gz')
    if not log_file.exists():
        return 0

    print(f'Processing anon_upc_access_log.{year}-{month:02}-{day:02}...')
    with gzip.open(log_file, mode='rt', encoding='utf-8', errors='ignore') as file:
        logs = file.readlines()
        for log in logs:
            processed_log, stats = process_log(log)
            batch.append((processed_log, log))
            if len(batch) >= BATCH_SIZE:
                LokiForwarder.forward_batch(batch)
                batch.clear()
            if LABEL_CONTENT in stats:
                monthly_stats[LABEL_CONTENT_ERROR] += 1
            else:
                monthly_stats[stats[LABEL_TYPE]] += 1
    return len(logs)

batch = []
for year in range(YEAR_START, YEAR_END + 1):
    yearly_stats = {
        'year': year,
        'total_logs': 0,
        LABEL_TYPE_RESOURCE: 0,
        LABEL_TYPE_SEARCH: 0,
        LABEL_TYPE_RESOURCE_WEB: 0,
        LABEL_TYPE_OTHERS: 0,
        LABEL_CONTENT_ERROR: 0,
        'time': 0.0
    }
    for month in range(1, 13):
        total_logs = 0
        monthly_stats = {
            'year': year,
            'month': month,
            'total_logs': 0,
            LABEL_TYPE_RESOURCE: 0,
            LABEL_TYPE_SEARCH: 0,
            LABEL_TYPE_RESOURCE_WEB: 0,
            LABEL_TYPE_OTHERS: 0,
            LABEL_CONTENT_ERROR: 0,
            'time': 0.0
        }
        start_time = time.time()
        folder = Path(INPUT_PATH)
        for day in range(1, 32):
            total_logs += process_logs_for_date(year, month, day, folder, batch, monthly_stats)
        if batch:
            LokiForwarder.forward_batch(batch)
            batch.clear()
        end_time = time.time()
        monthly_stats['total_logs'] = total_logs
        monthly_stats['time'] = (end_time - start_time) / 60
        yearly_stats['total_logs'] += total_logs
        yearly_stats[LABEL_TYPE_RESOURCE] += monthly_stats[LABEL_TYPE_RESOURCE]
        yearly_stats[LABEL_TYPE_SEARCH] += monthly_stats[LABEL_TYPE_SEARCH]
        yearly_stats[LABEL_TYPE_RESOURCE_WEB] += monthly_stats[LABEL_TYPE_RESOURCE_WEB]
        yearly_stats[LABEL_TYPE_OTHERS] += monthly_stats[LABEL_TYPE_OTHERS]
        yearly_stats[LABEL_CONTENT_ERROR] += monthly_stats[LABEL_CONTENT_ERROR]
        yearly_stats['time'] += monthly_stats['time']
        print(json.dumps(monthly_stats, indent=4))
    print(json.dumps(yearly_stats, indent=4))
LokiForwarder.close()
