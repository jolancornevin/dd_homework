#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict


class StatData(object):
    """Represent every traffic data we can accumulate over a given period of time."""
    def __init__(self, date):
        self.reset_obj(date)

    def reset_obj(self, date):
        """Set the traffic data back to 0"""
        self.last_traffic_report_date = date
        self.total_hit = 0
        self.users = defaultdict(int)
        self.errors = defaultdict(list)
        self.stats = defaultdict(lambda: {
            'hit': 0,
            'bytes': 0,
            'http_verb': defaultdict(int),
            'status': defaultdict(int)
        })

    def add_log_line(self, line, section, authuser, http_verb, status, bytes):
        """Increment the traffic data with the new info of this line."""
        self.total_hit += 1
        self.users[authuser] += 1

        if status in ('404', '500'):
            self.errors[status].append(line)

        self.stats[section]['http_verb'][http_verb] += 1
        self.stats[section]['status'][status] += 1
        self.stats[section]['hit'] += 1
        self.stats[section]['bytes'] += int(bytes)