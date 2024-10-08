# -*- coding: utf-8 -*-

import argparse

from log_analyser import LogAnalyser


def get_user_params():
    parser = argparse.ArgumentParser(description='Real time analyse of your HTTP logs')
    parser.add_argument(
        '-t', '--alert_threshold', type=int, help='The threshold to hit before alerting for high traffic'
    )

    parser.add_argument(
        '-f', '--file', type=argparse.FileType('r', encoding='UTF-8'),
        help='The file containing your HTTP logs', default='/tmp/access.log'
    )
    parser.add_argument(
        '-l', '--log_limit', type=int,
        help='The number of logs you want to print every 10 seconds', default=10
    )
    args = parser.parse_args()

    return args.alert_threshold, args.log_limit, args.file


if __name__ == '__main__':
    alert_threshold, log_limit, log_file = get_user_params()
    LogAnalyser(alert_threshold, log_limit, log_file).analyse()
