from datetime import datetime
from dateutil import tz
from abscore.parsablesegmentabc import ParsableSegmentAbc
from segmentparsers import MetarSegmentParser, StationIdentifierSegmentParser, MetarReportDateTimeGroupSegmentParser
from precipitationsegmentparsers import PrecipitationDiscriminatorSegmentParser, \
    PrecipitationSegmentParser   

class MetarReport:

    def __init__(self) -> None:
        self._parsed_segments: list[str] = []
        self._segment_parsers: list[ParsableSegmentAbc] = [
            MetarSegmentParser(),
            StationIdentifierSegmentParser(),
            MetarReportDateTimeGroupSegmentParser(),
            PrecipitationDiscriminatorSegmentParser(),
            PrecipitationSegmentParser(),
            
        ]

    def parse(self, raw_metar_string:str) -> list[str]:
        self._parsed_segments = []
        for parser in self._segment_parsers:
            parsed_value = parser.parse(raw_metar_string)
            if parsed_value is not None and parsed_value != '':
                self._parsed_segments.append(parsed_value)
        
        return self._parsed_segments