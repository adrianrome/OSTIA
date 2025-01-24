from pathlib import Path  # For handling filesystem paths.
from src.logs.counter.double_click import DoubleClick  # Import double-click counter logic.
from src.logs.counter.robots_crawlers import RobotsCrawlers  # Import robot/crawler detection logic.
from src.logs.counter.status_code import StatusCode  # Import HTTP status code counter logic.
from src.logs.filter.access_bitstream import AccessBitstream  # Filter for bitstream-related logs.
from src.logs.filter.access_resource import AccessResource  # Filter for general resource-related logs.
from src.logs.filter.access_resource_bitstream import AccessResourceBitstream  # Filter for resource-bitstream logs.
from src.logs.filter.search_resource import SearchResource  # Filter for search-related resources.
from src.logs.filter.web_resource import WebResource  # Filter for web resources.
from src.logs.filter.with_ipv6address import WithIPv6Address  # Filter for logs containing IPv6 addresses.
from src.logs.filter.without_ipaddress import WithoutIpAddress  # Filter for logs without IP addresses.
from src.logs.forwarder.loki_forwarder import LokiForwarder  # Log forwarder for Loki.
from src.logs.transformer.add_bitstream_resource_id_label import AddBitstreamResourceIdLabel  # Adds bitstream resource labels.
from src.logs.transformer.add_default_ipaddress import AddDefaultIpAddress  # Adds default IP addresses.
from src.logs.transformer.add_label import AddLabel  # Generic label-adding logic.
from src.logs.transformer.add_log_metadata import AddLogMetadata  # Adds metadata to logs.
from src.logs.transformer.add_resource_id_label import AddResourceIdLabel  # Adds resource ID labels.
from src.logs.transformer.add_timestamp import AddTimestamp  # Adds timestamps to logs.
from src.logs.transformer.remove_ipv6address import RemoveIPv6Address  # Removes IPv6 addresses from logs.
from src.logs.transformer.to_json import ToJSON  # Transforms raw logs into JSON format.
from src.logs.utils.constants import LABEL_CONTENT, LABEL_CONTENT_OK, LABEL_CONTENT_ERROR, LABEL_CONTENT_DIFFERENT
from src.logs.utils.constants import LABEL_TYPE, LABEL_TYPE_OTHERS, LABEL_TYPE_SEARCH, LABEL_TYPE_RESOURCE, LABEL_TYPE_RESOURCE_BITSTREAM, LABEL_TYPE_BITSTREAM, LABEL_TYPE_RESOURCE_WEB
from src.logs.utils.constants import LABEL_VALUE
from src.logs.utils.constants import LOG_COUNTER, LOG_COUNTER_STATUS_CODE, LOG_COUNTER_DOUBLE_CLICK, LOG_COUNTER_ROBOTS_CRAWLERS, LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN
import gzip  # For reading compressed log files.
import json  # For handling JSON serialization.
import os  # For accessing environment variables.
import time  # For measuring execution time.

def process_log(line: str) -> dict:
    """
    Processes a single log entry and extracts relevant information.

    Args:
        line (str): The raw log entry as a string.

    Returns:
        dict: A dictionary containing extracted log data or processing statistics.
    """
    stats = {}
    # Handle missing or IPv6 addresses.
    if WithoutIpAddress.filter(line):
        line = AddDefaultIpAddress.transform(line)
    elif WithIPv6Address.filter(line):
        line = RemoveIPv6Address.transform(line)
    
    try:
        # Attempt to parse the log into JSON format.
        log, status = ToJSON.transform(line)
        ip_address = log['ip_address']
        date = log['date']
        time = log['time']
        resource = log['request']['resource']
        status_code = int(log['request']['status_code'])
        user_agent = log['user_agent']
    except Exception as e:
        # Handle parsing errors.
        log = {LABEL_VALUE: line, LABEL_CONTENT: LABEL_CONTENT_ERROR}
        try:
            AddTimestamp.transform(log, line)
            LokiForwarder.forward(log, line)
        except Exception as inner_e:
            print(f"Error forwarding log: {inner_e}")
        stats[LABEL_CONTENT] = LABEL_CONTENT_ERROR
        return stats
    
    # Process based on extracted log details.
    if StatusCode.filter(status_code):
        stats[LOG_COUNTER] = LOG_COUNTER_STATUS_CODE
        return stats
    if DoubleClick.filter(ip_address, date, time, resource, user_agent):
        stats[LOG_COUNTER] = LOG_COUNTER_DOUBLE_CLICK
        return stats
    robot_name = RobotsCrawlers.filter(user_agent)
    if robot_name:
        stats[LOG_COUNTER] = LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN
        stats['robot_name'] = robot_name
        return stats

    # Add labels and metadata based on resource type.
    AddLabel.transform(log, LABEL_CONTENT, LABEL_CONTENT_OK if status == 0 else LABEL_CONTENT_DIFFERENT)
    if AccessResource.filter(resource):
        AddResourceIdLabel.transform(log, resource)
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_RESOURCE)
        AddLogMetadata.transform(log, log["resource"])
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE
    elif AccessResourceBitstream.filter(resource):
        AddBitstreamResourceIdLabel.transform(log, resource)
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_RESOURCE_BITSTREAM)
        AddLogMetadata.transform(log, log["resource"])
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE_BITSTREAM
    elif AccessBitstream.filter(resource):
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_BITSTREAM)
        stats[LABEL_TYPE] = LABEL_TYPE_BITSTREAM
    elif WebResource.filter(resource):
        stats[LABEL_TYPE] = LABEL_TYPE_RESOURCE_WEB
        return stats
    elif SearchResource.filter(resource):
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_SEARCH)
        stats[LABEL_TYPE] = LABEL_TYPE_SEARCH
    else:
        AddLabel.transform(log, LABEL_TYPE, LABEL_TYPE_OTHERS)
        stats[LABEL_TYPE] = LABEL_TYPE_OTHERS
    
    # Forward the processed log to Loki.
    if LokiForwarder.forward(log, line) == -1:
        stats[LABEL_CONTENT] = LABEL_CONTENT_ERROR
    return stats

def process_logs_for_day(log_file, monthly_stats):
    """
    Processes all logs in a single day's log file.

    Args:
        log_file (Path): Path to the compressed log file.
        monthly_stats (dict): Dictionary to store monthly statistics.
    """
    with gzip.open(log_file, mode='rt', encoding='utf-8', errors='ignore') as file:
        for log in file:
            stats = process_log(log)
            if not stats:
                continue
            # Update counters based on the log's classification.
            if counter_type := stats.get(LOG_COUNTER):
                if counter_type == LOG_COUNTER_STATUS_CODE:
                    monthly_stats[LOG_COUNTER_STATUS_CODE] += 1
                elif counter_type == LOG_COUNTER_DOUBLE_CLICK:
                    monthly_stats[LOG_COUNTER_DOUBLE_CLICK] += 1
                elif counter_type == LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN:
                    robot_name = stats['robot_name']
                    monthly_stats[LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN][robot_name] = \
                        monthly_stats[LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN].get(robot_name, 0) + 1
            elif stats.get(LABEL_CONTENT) == LABEL_CONTENT_ERROR:
                monthly_stats[LABEL_CONTENT_ERROR] += 1
            else:
                monthly_stats[stats[LABEL_TYPE]] += 1

def update_yearly_stats(yearly_stats, monthly_stats):
    """
    Updates yearly statistics with data from a given month's statistics.

    Args:
        yearly_stats (dict): Dictionary to store yearly statistics.
        monthly_stats (dict): Monthly statistics to incorporate into the yearly totals.
    """
    keys_to_update = [
        LOG_COUNTER_STATUS_CODE, LOG_COUNTER_DOUBLE_CLICK, LOG_COUNTER_ROBOTS_CRAWLERS, LABEL_TYPE_RESOURCE,
        LABEL_TYPE_RESOURCE_BITSTREAM, LABEL_TYPE_BITSTREAM, LABEL_TYPE_SEARCH,
        LABEL_TYPE_RESOURCE_WEB, LABEL_TYPE_OTHERS, LABEL_CONTENT_ERROR
    ]
    for key in keys_to_update:
        yearly_stats[key] += monthly_stats.get(key, 0)
    # Update robot/crawler breakdown statistics.
    breakdown = yearly_stats[LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN]
    for robot_name, count in monthly_stats.get(LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN, {}).items():
        breakdown[robot_name] = breakdown.get(robot_name, 0) + count
    yearly_stats['time'] += monthly_stats.get('time', 0)
    yearly_stats['total_logs'] += monthly_stats.get('total_logs', 0)

def process_month(year, month, yearly_stats):
    """
    Processes logs for an entire month.

    Args:
        year (int): The year of the logs being processed.
        month (int): The month of the logs being processed.
        yearly_stats (dict): Dictionary to store yearly statistics.
    """
    # Initialize monthly statistics.
    monthly_stats = {
        'year': year,
        'total_logs': 0,
        LOG_COUNTER_STATUS_CODE: 0,
        LOG_COUNTER_DOUBLE_CLICK: 0,
        LOG_COUNTER_ROBOTS_CRAWLERS: 0,
        LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN: {},
        LABEL_TYPE_RESOURCE: 0,
        LABEL_TYPE_SEARCH: 0,
        LABEL_TYPE_RESOURCE_WEB: 0,
        LABEL_TYPE_RESOURCE_BITSTREAM: 0,
        LABEL_TYPE_BITSTREAM: 0,
        LABEL_TYPE_OTHERS: 0,
        LABEL_CONTENT_ERROR: 0,
        'time': 0.0,
        'month': month
    }
    start_time = time.time()
    folder = Path(os.environ.get('LOGS_OUTPUT_PATH', '').strip())
    for day in range(int(os.environ.get('START_DAY')), int(os.environ.get('END_DAY')) + 1):
        log_file = folder / f'anon_upc_access_log.{year}-{month:02}-{day:02}.txt.gz'
        if log_file.exists():
            print(f"Processing: {log_file.name}")
            process_logs_for_day(log_file, monthly_stats)
    monthly_stats[LOG_COUNTER_ROBOTS_CRAWLERS] = sum(monthly_stats[LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN].values())
    keys_to_sum = [
        LOG_COUNTER_STATUS_CODE, LOG_COUNTER_DOUBLE_CLICK, LOG_COUNTER_ROBOTS_CRAWLERS,
        LABEL_TYPE_RESOURCE, LABEL_TYPE_RESOURCE_BITSTREAM, LABEL_TYPE_BITSTREAM,
        LABEL_TYPE_SEARCH, LABEL_TYPE_RESOURCE_WEB, LABEL_TYPE_OTHERS
    ]
    monthly_stats['total_logs'] = sum(monthly_stats.get(key, 0) for key in keys_to_sum)
    monthly_stats['time'] = round((time.time() - start_time) / 60, 2)
    update_yearly_stats(yearly_stats, monthly_stats)
    print(json.dumps(monthly_stats, indent=4))

def main():
    """
    Main function to process logs for the specified range of years and months.
    """
    for year in range(int(os.environ.get('START_YEAR')), int(os.environ.get('END_YEAR')) + 1):
        yearly_stats = {
            'year': year,
            'total_logs': 0,
            LOG_COUNTER_STATUS_CODE: 0,
            LOG_COUNTER_DOUBLE_CLICK: 0,
            LOG_COUNTER_ROBOTS_CRAWLERS: 0,
            LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN: {},
            LABEL_TYPE_RESOURCE: 0,
            LABEL_TYPE_SEARCH: 0,
            LABEL_TYPE_RESOURCE_WEB: 0,
            LABEL_TYPE_RESOURCE_BITSTREAM: 0,
            LABEL_TYPE_BITSTREAM: 0,
            LABEL_TYPE_OTHERS: 0,
            LABEL_CONTENT_ERROR: 0,
            'time': 0.0
        }
        for month in range(int(os.environ.get('START_MONTH')), int(os.environ.get('END_MONTH')) + 1):
            process_month(year, month, yearly_stats)
        yearly_stats[LOG_COUNTER_ROBOTS_CRAWLERS] = sum(
            yearly_stats[LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN].values()
        )
        print(json.dumps(yearly_stats, indent=4))
    LokiForwarder.close()

if __name__ == "__main__":
    main()
