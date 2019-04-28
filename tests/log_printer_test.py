#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from freezegun import freeze_time
from mock import Mock, call, patch

from src.log_printer import LogPrinter
from src.stat_data import StatData


class LogPrinterTest(unittest.TestCase):
    @freeze_time('2018-05-09 16:00:35')
    def setUp(self):
        self.now = datetime.now()
        self.printer = LogPrinter()
        self.stat = StatData(self.now)

    @patch('src.log_printer.colored.yellow')
    @patch('src.log_printer.puts')
    def test_show_empty_logs(self, p_puts, p_yellow):
        colored_return_value = 'colored_return_value'
        p_yellow.return_value = colored_return_value

        self.printer.show(None, self.stat)
        p_yellow.assert_called_once_with(' ----- You got 0 hits over the last 10 seconds -----')
        p_puts.assert_called_once_with(colored_return_value)

    @patch('src.log_printer.colored.green')
    @patch('src.log_printer.colored.red')
    @patch('src.log_printer.puts')
    def test_alert_hight_traffic(self, p_puts, p_red, p_green):
        red_colored_return_value = 'red_colored_return_value'
        p_red.return_value = red_colored_return_value

        green_colored_return_value = 'green_colored_return_value'
        p_green.return_value = green_colored_return_value

        self.printer.last_two_minutes_report_date = datetime(2018, 5, 9, 16, 3)
        self.printer.total_hit_over_two_minutes = self.printer.alert_threshold + 10

        self.printer.print_alert_messages(1, datetime(2018, 5, 9, 16, 5, 1), self.stat)

        p_red.assert_called_once_with('High traffic generated an alert - hits = 20, triggered at 2018-05-09 16:05:01')
        p_puts.assert_called_once_with(red_colored_return_value)
        p_puts.reset_mock()

        self.printer.total_hit_over_two_minutes = self.printer.alert_threshold - 10
        self.printer.print_alert_messages(1, datetime(2018, 5, 9, 16, 7, 2), self.stat)

        p_green.assert_called_once_with('High traffic recovered')
        p_puts.assert_called_once_with(green_colored_return_value)
        p_green.reset_mock()
        p_puts.reset_mock()

        self.printer.print_alert_messages(1, datetime(2018, 5, 9, 16, 9, 3), self.stat)

        p_green.assert_not_called()

    @patch('src.log_printer.colored.red')
    @patch('src.log_printer.puts')
    def test_alert_hight_traffic(self, p_puts, p_red):
        red_colored_return_value = 'red_colored_return_value'
        p_red.return_value = red_colored_return_value
