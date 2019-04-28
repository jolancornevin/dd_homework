#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time
from mock import Mock, call, patch

from src.log_analyser import LogAnalyser


class LogAnalyserTest(TestCase):
    @freeze_time('2018-05-09 16:00:35')
    def setUp(self):
        self.log_file = Mock()
        self.log_file.readline.side_effect = [
            '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 404 123',
            '127.0.0.1 - james [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
            None,
            '127.0.0.1 - jill [09/May/2018:16:01:00 +0000] "GET /api/user HTTP/1.0" 200 234'
        ]
        self.analyser = LogAnalyser(10, 10, self.log_file)

    @freeze_time('2018-05-09 16:00:41')
    @patch('src.log_analyser.sleep')
    def test_analyse(self, p_sleep):
        p_stat_data_add_log_line = Mock()
        p_stat_data_reset_obj = Mock()
        self.analyser.stat_data.add_log_line = p_stat_data_add_log_line
        self.analyser.stat_data.reset_obj = p_stat_data_reset_obj

        with patch.object(self.analyser, 'log_printer') as p_log_printer:
            self.analyser.analyse()

            p_sleep.assert_called_once_with(self.analyser.SLEEP_TIME)

            last_log_date = datetime(2018, 5, 9, 16, 1, 0)
            p_log_printer.show.assert_called_once_with(last_log_date, self.analyser.stat_data)
            p_stat_data_add_log_line.assert_has_calls([
                call(
                    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 404 123',
                    '/report', 'james', 'GET', '404', '123'
                ),
                call(
                    '127.0.0.1 - james [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
                    '/api', 'james', 'GET', '200', '234'
                ),
                call(
                    '127.0.0.1 - jill [09/May/2018:16:01:00 +0000] "GET /api/user HTTP/1.0" 200 234',
                    '/api', 'jill', 'GET', '200', '234'
                )
            ])
            p_stat_data_reset_obj.assert_called_once_with(last_log_date)

