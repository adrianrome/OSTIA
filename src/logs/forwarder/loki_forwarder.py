from src.logs.forwarder.forwarder_interface import IForwarder
from src.logs.utils.date_converter import to_nanoseconds

import os
import requests
import json
from typing import List


class LokiForwarder(IForwarder):
    loki_url: str | None = None

    previous_timestamp: int = 0
    previous_date: tuple[str, str] = ('', '')

    @classmethod
    def forward_batch(cls, batch: List[tuple[dict, str]]) -> int:
        """
        Forwards a batch of log entries to Loki.

        :param batch: A list of tuples containing the processed log entry and the raw log entry.
        :type batch: List[tuple[dict, str]]
        :return: Status code of the action.
        :rtype: int
        """

        cls._ensure_loki_url()

        streams = []
        for log, raw_log in batch:
            try:
                time = cls._set_timestamp(log['date'], log['time'])
            except:
                continue

            log_entry = {
                "log": raw_log,
                "recurs": log.get("resource") if log.get("type") == "recurs" else None
            }
            
            log_entry_str = json.dumps(log_entry)

            streams.append({
                'stream': cls._set_log_tags(log),
                'values': [[str(time), log_entry_str]]
            })

        data = {'streams': streams}

        response = requests.post(f"{cls.loki_url}/loki/api/v1/push", json=data)
        return response.status_code

    @classmethod
    def close(cls) -> None:
        """
        Close the *Loki* handler.

        :return: None
        """
        pass

    @staticmethod
    def _set_log_tags(log: dict) -> dict:
        """
        Defines the *Loki* tags based on the content of the log entry.

        :param log: The log entry, represented as a dictionary.
        :type log: dict
        :return: A dictionary with the specific tags.
        :rtype: dict
        """
        if log['content'] == "error":
            return {'content': "error"}
        else:
            return {
                'service_name': 'log-upcommons',
                'content': log['content'],
                'method': log['request']['method'],
                'status_code': log['request']['status_code'],
                'type': log['type']            
            }

    @classmethod
    def _ensure_loki_url(cls) -> None:
        """
        Ensures that the Loki URL is set.

        :return: None
        """
        if cls.loki_url is None:
            cls.loki_url = os.environ.get('LOKI_URL')
            if cls.loki_url is None:
                raise ValueError("LOKI_URL environment variable is not set")

    @classmethod
    def _set_timestamp(cls, date: str, time: str) -> int:
        """
        Converts the date, time pair in to a UNIX timestamp.

        At every collision with *previous_timestamp* one second is added.

        :param date: Date in dd-mm-yyyy format.
        :type date: str
        :param time: Time in hh:mm:ss z format.
        :type time: str
        :return: Timestamp of the <date,time> pair.
        :rtype: int
        """

        ts = to_nanoseconds(date, time)

        if (date, time) == cls.previous_date:
            ts = cls.previous_timestamp = cls.previous_timestamp + 1
        else:
            cls.previous_timestamp = ts

        cls.previous_date = (date, time)
        return ts
