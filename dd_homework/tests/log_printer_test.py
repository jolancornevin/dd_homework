# -*- coding: utf-8 -*-

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, call, patch

from freezegun import freeze_time  # type: ignore

from log_printer import LogPrinter
from stat_data import StatData


class LogPrinterTest(TestCase):
    @freeze_time('2018-05-09 16:00:35')
    def setUp(self):
        self.now = datetime.now()
        self.printer = LogPrinter()
        self.stat = StatData(self.now)

    @patch('log_printer.colored.blue')
    @patch('log_printer.puts')
    def test_show(self, p_puts, p_blue):
        colored_return_value = 'colored_return_value'
        p_blue.return_value = colored_return_value

        self.stat.total_hit = 1
        self.printer.show(datetime(2018, 5, 9, 16, 5, 1), self.stat)
        p_blue.assert_called_once_with(' ----- You got 1 hits over the last 10 seconds -----')

    @patch('log_printer.colored.yellow')
    @patch('log_printer.puts')
    def test_show_empty_logs(self, p_puts, p_yellow):
        colored_return_value = 'colored_return_value'
        p_yellow.return_value = colored_return_value

        self.printer.show(None, self.stat)
        p_yellow.assert_called_once_with(' ----- You got 0 hits over the last 10 seconds -----')
        p_puts.assert_called_once_with(colored_return_value)

    @patch('log_printer.colored.green')
    @patch('log_printer.colored.red')
    @patch('log_printer.puts')
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

    @patch('log_printer.colored.red')
    @patch('log_printer.puts')
    def test_print_alert_messages_user_traffic(self, p_puts, p_red):
        red_colored_return_value = 'red_colored_return_value'
        p_red.return_value = red_colored_return_value

        self.stat.users['-'] = 1

        self.printer.print_alert_messages(1, datetime(2018, 5, 9, 16, 5, 1), self.stat)

        p_red.assert_called_once_with('  /!\ - takes more than 30% of your traffic (100.0%)')
        p_puts.assert_called_once_with(red_colored_return_value)

    @patch('log_printer.colored.red')
    @patch('log_printer.puts')
    def test_print_alert_messages_errors(self, p_puts, p_red):
        red_colored_return_value = 'red_colored_return_value'
        p_red.return_value = red_colored_return_value

        self.stat.errors['404'] = ['log line one', 'log line two']

        self.printer.print_alert_messages(1, datetime(2018, 5, 9, 16, 5, 1), self.stat)

        p_red.assert_has_calls([
            call('  /!\ You had 404:'),
            call('    - log line one    - log line two')
        ])
        p_puts.assert_called()

    @patch('log_printer.colored.red')
    @patch('log_printer.colored.yellow')
    @patch('log_printer.colored.green')
    @patch('log_printer.colored.white')
    @patch('log_printer.columns')
    @patch('log_printer.puts')
    def test_print_stat_table(self, p_puts, p_columns, p_white, p_green, p_yellow, p_red):
        white_colored_return_value = 'white_colored_return_value'
        p_white.return_value = white_colored_return_value

        green_colored_return_value = 'green_colored_return_value'
        p_green.return_value = green_colored_return_value

        yellow_colored_return_value = 'yellow_colored_return_value'
        p_yellow.return_value = yellow_colored_return_value

        red_colored_return_value = 'red_colored_return_value'
        p_red.return_value = red_colored_return_value

        args_list = [
            (
                '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 404 123',
                '/report', 'james', 'GET', '404', '123'
            ),
            (
                '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "POST /error HTTP/1.0" 500 123',
                '/error', 'james', 'GET', '500', '123'
            ),
            (
                '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123',
                '/report', 'james', 'GET', '200', '123'
            ),
            (
                '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123',
                '/report', 'james', 'GET', '200', '123'
            ),
            (
                '127.0.0.1 - james [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
                '/api', 'james', 'GET', '200', '234'
            ),
        ]

        for args in args_list:
            self.stat.add_log_line(*args)

        self.printer.print_stat_table(self.stat)

        p_green.assert_has_calls([
            call('Section'), call('Hits'), call('Bytes'), call('Status'), call('HTTP verbs'),
        ])
        p_red.assert_has_calls([
            call('/error'),
        ])
        p_yellow.assert_has_calls([
            call('/report'),
        ])
        p_white.assert_has_calls([
            call('/api')
        ])
        p_columns.assert_has_calls([
            call(
                ['green_colored_return_value', 20], ['green_colored_return_value', 5],
                ['green_colored_return_value', 8], ['green_colored_return_value', 10],
                ['green_colored_return_value', 10]
            ),
            call(['yellow_colored_return_value', 20], ['3', 5], ['369', 8], ['404 x 1 200 x 2 ', 10], ['GET x 3 ', 10]),
            call(['red_colored_return_value', 20], ['1', 5], ['123', 8], ['500 x 1 ', 10], ['GET x 1 ', 10]),
            call(['white_colored_return_value', 20], ['1', 5], ['234', 8], ['200 x 1 ', 10], ['GET x 1 ', 10])
        ])
        p_puts.assert_called()
