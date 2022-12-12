from datetime import datetime
from dateutil import tz
from precipitation_segment_parsers import PrecipitationDiscriminatorSegmentParser, \
    PrecipitationSegmentParser   

class MetarReport:

    def __init__(self) -> None:
        self._segment_parsers: dict = {}
        self._parsed_segments = []
        
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