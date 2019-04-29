# -*- coding: utf-8 -*-

from collections import defaultdict

from datetime import datetime


class StatData:
    """Represent every traffic data we can accumulate over a given period of time."""
    def __init__(self, date: datetime) -> None:
        self.reset_obj(date)

    def reset_obj(self, date: datetime) -> None:
        """Set the traffic data back to 0"""
        self.last_traffic_report_date: datetime = date
        self.total_hit: int = 0
        self.users: dict = defaultdict(int)
        self.errors: dict = defaultdict(list)
        self.stats: dict = defaultdict(lambda: {
            'hit': 0,
            'bytes': 0,
            'http_verb': defaultdict(int),
            'status': defaultdict(int)
        })

    def add_log_line(self, line: str, section: str, authuser: str, http_verb: str, status: str, bytes: str) -> None:
        """Increment the traffic data with the new info of this line."""
        self.total_hit += 1
        self.users[authuser] += 1

        if status in ('404', '500'):
            self.errors[status].append(line)

        self.stats[section]['http_verb'][http_verb] += 1
        self.stats[section]['status'][status] += 1
        self.stats[section]['hit'] += 1
        self.stats[section]['bytes'] += int(bytes)
