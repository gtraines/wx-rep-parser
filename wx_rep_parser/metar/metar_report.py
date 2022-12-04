from datetime import datetime
from dateutil import tz
from wx_rep_parser.abscore import ParsableSegmentAbc


class MetarSegmentParser(ParsableSegmentAbc):
    
    def _parse_raw_string(self, raw_string: str) -> str:
        if raw_string.lower() == 'metar':
            return "Routine Weather Report (METAR)"
        if raw_string.lower() == 'speci':
            return "Special Meteorological Report (SPECI)"

class StationIdentifierSegmentParser(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        return raw_string.upper()

class MetarReportDateTimeGroupSegmentParser(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        day_of_month = raw_string[0:2]
        zulu_time = raw_string[2:4]
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcnow()
        date_utc = str.format('{0}-{1}-{2}', utc.year, utc.month, day_of_month)
        date_time_utc = str.format('{0} {1}', date_utc, zulu_time)
        utc = datetime.strptime(date_time_utc, '%Y-%m-%d %H:%M')

        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        local_time = utc.astimezone(tz=to_zone)

        return str.format('{0} hours Zulu on Day {1} ({2} local time)', zulu_time, day_of_month, local_time)

class MetarReport:

    def __init__(self) -> None:
        self._raw_segments: list[str] = []
        self._raw_metar_string: str = ''
        self._raw_metar_type: str = 'METAR'
        self._raw_station_identifier: str = 'KXXX'
        self._raw_report_date_time_group: str = '00000'
        self._raw_modifier: str = ''
        self._raw_wind: str = ''
        self._raw_visibility: str = ''
        self._raw_weather_group: str = ''
        self._raw_sky_condition_group: str = ''
        self._raw_temperature_and_dew_point_group: str = ''
        self._raw_altimeter_setting: str = ''
        self._raw_zulu_time: str = ''
        self._raw_remarks: str = ''
        self._segment_parsers: dict = {}
        
    def _set_segment_parsers(self):
        self._segment_parsers[0] = MetarSegmentParser()
        self._segment_parsers[1] = StationIdentifierSegmentParser()
        self._segment_parsers[2] = MetarReportDateTimeGroupSegmentParser()

    def _assign_raw_segments(self, raw_metar_string: str) -> None:
        self._raw_metar_string = raw_metar_string
        self._raw_segments = raw_metar_string.split()
        
    def _parse_raw_segments(self) -> list[str]:
        parsed_segements = []
        return parsed_segements

    def parse(self, raw_metar_string:str) -> list[str]:
        self._assign_raw_segments(raw_metar_string)
        parsed_segments = self._parse_raw_segments()
        return parsed_segments