import unittest
from metartestabc import MetarTestAbc
from context import wx_rep_parser
from wx_rep_parser.metar.metarreport import  MetarSegmentParser, \
        MetarReportDateTimeGroupSegmentParser, \
        ReportModifierSegmentParser, \
        WindSegmentParser


class MetarWindSegmentParserTest(MetarTestAbc):
    _parser: WindSegmentParser = None
    def setUp(self) -> None:
        self._parser = WindSegmentParser()

    def test_can_parse_wind_speed_variable(self):
        variable_wind_segment_only = 'VRB21G26KT'
        output = self._parser._parse_wind_speed(variable_wind_segment_only)
        print(output)
        self.assertEqual('21 kts gusting to 26 kts', \
            output)
            
    def test_can_parse_extreme_variable_string(self):
        segment = '030V091'
        v = segment[3:4].lower()
        self.assertEqual('v', v)

    def test_can_parse_wind_variable(self):
        metar_example_string_extreme_variable_wind = 'METAR KGGG 161753Z AUTO VRB21G26KT 030V091  3/4SM ' \
            + '+TSRA BR BKN008 OVC012CB 18/17 A2970 RMK PRESFR'
        variable_wind_segment_only = 'VRB21G26KT'
        parser_instance = WindSegmentParser()
        parsed_result_wind_segment_only = parser_instance._parse_raw_string(variable_wind_segment_only)
        print(parsed_result_wind_segment_only)
        self.assertEqual('Wind is blowing from variable directions at 21 kts gusting to 26 kts', \
            parsed_result_wind_segment_only)

    def test_can_parse_with_extreme_variable_wind_segment(self):
        metar_example_string_extreme_variable_wind = 'METAR KGGG 161753Z AUTO VRB21G26KT 030V091  3/4SM ' \
            + '+TSRA BR BKN008 OVC012CB 18/17 A2970 RMK PRESFR'
        parser_instance = WindSegmentParser()
        output = parser_instance.parse(metar_example_string_extreme_variable_wind)
        print(output)
        self.assertEqual('Wind is blowing from variable directions at 21 kts gusting to 26 kts ' +  \
            'Winds from directions ranging from 030 degrees to 091 degrees', \
            output)

    def test_can_parse_normal_wind_segment(self):
        parser_instance = WindSegmentParser()
        output = parser_instance.parse(self.metar_example_string_normal)
        print(output)

    def test_can_parse_normal_wind_segment_kphx(self):
        parser_instance = WindSegmentParser()
        output = parser_instance.parse(self.metar_example_string_phx)
        print(output)


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