import unittest
from context import wx_rep_parser
from wx_rep_parser.metar import MetarReportDateTimeGroupSegmentParser


class MetarReportTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_metar_dtg_can_convert_to_local_time(self):

        test_dtg = '161753Z'

        report_instance = MetarReportDateTimeGroupSegmentParser()

        parsed_value = report_instance._parse_raw_string(test_dtg)

        print(parsed_value)


if __name__ == '__main__':
    unittest.main()