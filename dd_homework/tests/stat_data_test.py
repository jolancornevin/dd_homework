# -*- coding: utf-8 -*-

from datetime import datetime
from unittest import TestCase

from stat_data import StatData


class StatDataTest(TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.stat = StatData(self.now)

    def test_init(self):
        self.assertEqual(self.stat.last_traffic_report_date, self.now)

    def test_add_log_line(self):
        args_list = [
            (
                '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 404 123',
                '/report', 'james', 'GET', '404', '123'
            ),
            (
                '127.0.0.1 - james [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
                '/api', 'james', 'GET', '200', '234'
            ),
            (
                '127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
                '/api', 'jill', 'GET', '200', '234'
            ),
            (
                '127.0.0.1 - jill [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 200 34',
                '/api', 'jill', 'POST', '200', '34'
            ),

        ]

        for args in args_list:
            self.stat.add_log_line(*args)

        self.assertEqual(self.stat.total_hit, 4)
        self.assertEqual(self.stat.users['james'], 2)
        self.assertEqual(self.stat.users['jill'], 2)
        self.assertEqual(
            self.stat.errors['404'], ['127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 404 123']
        )
        self.assertEqual(self.stat.stats['/api']['http_verb']['GET'], 2)
        self.assertEqual(self.stat.stats['/api']['http_verb']['POST'], 1)
        self.assertEqual(self.stat.stats['/api']['status']['200'], 3)
        self.assertEqual(self.stat.stats['/api']['hit'], 3)
        self.assertEqual(self.stat.stats['/api']['bytes'], 234 * 2 + 34)

        self.assertEqual(self.stat.stats['/report']['http_verb']['GET'], 1)
        self.assertEqual(self.stat.stats['/report']['status']['404'], 1)
        self.assertEqual(self.stat.stats['/report']['hit'], 1)
        self.assertEqual(self.stat.stats['/report']['bytes'], 123)
