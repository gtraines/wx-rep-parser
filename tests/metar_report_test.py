import unittest
from abc import ABCMeta, abstractmethod

from context import wx_rep_parser
from wx_rep_parser.metar.metar_report import  MetarSegmentParser, \
        MetarReportDateTimeGroupSegmentParser, \
        ReportModifierSegmentParser

class MetarTestAbc(unittest.TestCase):

    __metaclass__ = ABCMeta

    metar_example_string_normal = 'METAR KGGG 161753Z AUTO 14021G26KT 3/4SM ' \
            + '+TSRA BR BKN008 OVC012CB 18/17 A2970 RMK PRESFR'

    metar_example_string_phx = 'KPHX 110051Z 24004KT 10SM CLR 16/05 A3004 RMK AO2 SLP168 T01560050'


class MetarSegmentParserTest(MetarTestAbc):

    def setUp(self) -> None:
        pass

    def test_can_parse_metar_normal_segment(self):

        normal_metar_segment = 'Routine Weather Report (METAR)'

        parser_instance = MetarSegmentParser()
        parsed_value = parser_instance.parse(self.metar_example_string_normal)

        self.assertEqual(normal_metar_segment, parsed_value)

    def test_can_parse_metar_kphx_segment(self):

        normal_metar_segment = 'Routine Weather Report (METAR)'

        parser_instance = MetarSegmentParser()
        parsed_value = parser_instance.parse(self.metar_example_string_phx)

        self.assertEqual(normal_metar_segment, parsed_value)


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