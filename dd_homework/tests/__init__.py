# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from .log_analyser_test import LogAnalyserTest
from .log_printer_test import LogPrinterTest
from .stat_data_test import StatDataTest