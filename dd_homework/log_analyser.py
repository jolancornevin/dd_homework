# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime, timedelta
from time import sleep
from typing import TextIO, Tuple

from log_printer import LogPrinter
from stat_data import StatData


class LogAnalyser:
    # The common logfile format is as follows:
    #   remotehost rfc931 authuser [date] "request" status bytes
    LOG_REGEX = re.compile(r'([\d\.]+) (.+?) (.+?) \[(.*?)\] "(.*?) (.*?) (.*?)" (\d+) (\d+)')
    # The number of seconds before each report.
    ANALYSIS_DURATION = 10
    # The number of seconds we sleep before trying to read the log file again once we've reached the end.
    SLEEP_TIME = 0.1
    DATE_FORMAT = '%d/%b/%Y:%H:%M:%S'

    def __init__(self, alert_threshold: int, log_limit: int, log_file: TextIO) -> None:
        self.log_file = log_file
        self.stat_data = StatData(datetime.now())
        self.log_printer = LogPrinter(alert_threshold, log_limit)

    @classmethod
    def read_file(cls, log_file: TextIO):
        """
        Read the file indefinitely and yield it's lines.

        :param log_file:
        :yield: line by line of the file until you close the connection
        """
        log_file.seek(0, os.SEEK_END)
        while True:
            line = log_file.readline()
            # If nothing is new in the file, we pause and loop again.
            if not line:
                sleep(cls.SLEEP_TIME)
                # We still want to return an empty line to alert if there is no traffic.
                yield (datetime.now(),) + ('',) * 6  # type: ignore
                continue

            yield cls.extract_lines_info(line)

    @classmethod
    def extract_lines_info(cls, line: str) -> Tuple[datetime, str, str, str, str, str, str]:
        """Extract data from the log line via our regex and return those that we are interested in."""
        _, rfc931, authuser, date, http_verb, route, http_method, status, bytes = cls.LOG_REGEX.match(  # type: ignore
            line
        ).groups()

        # The section is only the first part of the URL.
        section = '/' + route.split('/')[1].split('?')[0]
        date = datetime.strptime(date.split(' ')[0], cls.DATE_FORMAT)
        return date, line, section, authuser, http_verb, status, bytes

    def analyse(self) -> None:
        """
        Read the file, analyse each line and eventually shows stat about the traffic.
        :return:
        """
        for args in self.read_file(self.log_file):
            self._analyse_line(*args)

    def _analyse_line(
            self, date: datetime, line: str, section: str, authuser: str, http_verb: str, status: str, bytes: str
    ) -> None:
        """
        Compute traffic stat with the log line and eventually print stats to the user.

        :param date: The date of the log line
        :param line: The complete log line
        :param section: The url section of the website
        :param rfc931: The remote logname of the user.
        :param http_verb: The HTTP verb of the log line
        :param status: The HTTP status of the log line
        :param bytes: The number of bytes returned to the user.
        :return:
        """
        # It's time to alert the user
        if date > self.stat_data.last_traffic_report_date + timedelta(seconds=self.ANALYSIS_DURATION):
            self.log_printer.show(date, self.stat_data)
            # We reset our data object to compute stat for the next 10 seconds.
            self.stat_data.reset_obj(date)

        if not line:
            return

        self.stat_data.add_log_line(line, section, authuser, http_verb, status, bytes)
