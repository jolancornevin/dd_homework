# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from clint.textui import colored, columns, puts  # type: ignore

from stat_data import StatData


class LogPrinter:
    def __init__(self, alert_threshold=10, log_limit=10, abusing_user_threshold=30) -> None:
        self.alert_threshold = alert_threshold
        self.log_limit = log_limit
        self.abusing_user_threshold = abusing_user_threshold

        self.total_hit_over_two_minutes = 0
        self.last_two_minutes_report_date = datetime.now()
        self.is_alerting = False

    def show(self, date: datetime, stat_data: StatData) -> None:
        """
        Prints traffic information to the console.

        :param date:            The date of the last log we've read
        :param stat_data:      A dict of traffic statistics.

        :return: None
        """
        total_hit = stat_data.total_hit
        color_method = colored.yellow if total_hit == 0 else colored.blue
        puts(color_method(
            ' ----- You got {} hits over the last 10 seconds -----'.format(total_hit)
        ))

        if total_hit:
            self.total_hit_over_two_minutes += total_hit
            self.print_alert_messages(total_hit, date, stat_data)
            self.print_stat_table(stat_data)

    def print_alert_messages(self, total_hits: int, date: datetime, stat_data: StatData) -> None:
        """Alert the user about worrying stats"""
        if date > self.last_two_minutes_report_date + timedelta(minutes=2):
            if self.total_hit_over_two_minutes > self.alert_threshold:
                puts(colored.red(
                    'High traffic generated an alert - hits = {}, triggered at {}'.format(
                        self.total_hit_over_two_minutes, date
                    )
                ))
                self.is_alerting = True
            elif self.is_alerting:
                puts(colored.green('High traffic recovered'))
                self.is_alerting = False

            self.total_hit_over_two_minutes = 0
            self.last_two_minutes_report_date = date

        for user, hits in stat_data.users.items():
            if hits > total_hits * self.abusing_user_threshold / 100:
                puts(colored.red(
                    '  /!\ {} takes more than {}% of your traffic ({}%)'.format(
                        user, self.abusing_user_threshold, hits * 100 / total_hits
                    )
                ))

        for error, lines in stat_data.errors.items():
            puts(colored.red(
                '  /!\ You had {}:'.format(error)
            ))
            puts(colored.red(
                ''.join(['    - {}'.format(line) for line in lines])
            ))

    def print_stat_table(self, stat_data: StatData) -> None:
        def _print_column(section: str, hits: str, bytes: str, status: str, verbs: str) -> None:
            """A small helper to show a report line"""
            puts(columns([section, 20], [hits, 5], [bytes, 8], [status, 10], [verbs, 10]))

        # Print the header of the report
        _print_column(
            colored.green('Section'), colored.green('Hits'), colored.green('Bytes'),
            colored.green('Status'), colored.green('HTTP verbs')
        )

        for section, stat in sorted(
                stat_data.stats.items(), key=lambda k_v: k_v[1]['hit'], reverse=True
        )[:self.log_limit]:
            # Compute the status line as a section may return different status over a period of time.
            status_line = ''
            for verb, hit in stat['status'].items():
                status_line += '{} x {} '.format(verb, hit)

            # Compute the HTTP verb line as a section may be queried with different verbs over a period of time.
            verbs_line = ''
            for verb, hit in stat['http_verb'].items():
                verbs_line += '{} x {} '.format(verb, hit)

            # Compute the color of the section depending on the status that the section returned.
            if any([str(server_code) in stat['status'] for server_code in range(500, 528)]):
                section_color = colored.red
            elif any([str(client_code) in stat['status'] for client_code in range(400, 457)]):
                section_color = colored.yellow
            else:
                section_color = colored.white

            _print_column(section_color(section), str(stat['hit']), str(stat['bytes']), status_line, verbs_line)
