from abscore.parsablesegmentabc import ParsableSegmentAbc

class MetarSegmentParser(ParsableSegmentAbc):
    
    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        segment = string_segments[0]
        if segment.lower().startswith('k'):
            return 'METAR'
        return segment

    def _parse_raw_string(self, raw_string: str) -> str:
        if raw_string.lower() == 'metar':
            return "Routine Weather Report (METAR)"
        if raw_string.lower() == 'speci':
            return "Special Meteorological Report (SPECI)"


class StationIdentifierSegmentParser(ParsableSegmentAbc):

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        segment = string_segments[0]
        if segment.lower().startswith('k'):
            return segment
        return segment

    def _parse_raw_string(self, raw_string: str) -> str:
        return 'Conditions at: ' + raw_string.upper()


class MetarReportDateTimeGroupSegmentParser(ParsableSegmentAbc):

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        segment = string_segments[1]
        if segment.lower().startswith('k'):
            return string_segments[2]
        return segment

    def _parse_date_time_group_string(self, raw_string: str) -> str:
        day_of_month = raw_string[0:2]
        zulu_time_h = raw_string[2:4]
        zulu_time_m = raw_string[4:6]
        zulu_time = str.format('{0}:{1}', zulu_time_h, zulu_time_m)
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
    
    def _parse_raw_string(self, raw_string: str) -> str:
        parsed_dtg = self._parse_date_string(raw_string)
        return 'observed ' + parsed_dtg


class ReportModifierSegmentParser(ParsableSegmentAbc):

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        for segment in string_segments:
            if segment.lower() == 'auto' or segment.lower() == 'cor':
                return segment
        return ''

    def _parse_raw_string(self, raw_string: str) -> str:
        if raw_string.lower() == 'auto':
            return 'Automated source'
        if raw_string.lower() == 'cor':
            return 'Correction report'
        return 'unknown report modifier'


class WindSegmentParser(ParsableSegmentAbc):

    def _is_extreme_variable_wind_segment(self, segment: str) -> bool:
        if len(segment.lower()) == 7 \
            and str.isalnum(segment[0:3]) \
            and segment[3:4].lower() == 'v' \
            and str.isalnum(segment[4:]):
            return True
        return False

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        wind_segments = []
        for segment in string_segments:
            if segment.lower().endswith('kt'):
                wind_segments.append(segment)
            if self._is_extreme_variable_wind_segment(segment):
                wind_segments.append(segment)
        
        return str.join(' ', wind_segments)

    # account for the extreme variable wind segment (> 60 degrees variable == xxxVxxx)
    def _get_extreme_variable_wind_report(self, raw_string: str) -> str:
        bottom_degree_range = raw_string[0:3]
        top_degree_range = raw_string[4:]
        return 'Winds from directions ranging from ' + bottom_degree_range + ' degrees to ' + top_degree_range + ' degrees'

    def _get_normal_wind_report(self, raw_string: str) -> str:
        wind_from_direction = raw_string[0:3]
        if wind_from_direction.lower() == 'vrb':
            wind_from_direction = 'variable directions'
        else:
            wind_from_direction = str.format('{0} degrees', wind_from_direction)
        windspeed_segment = self._parse_wind_speed(raw_string)
        return str.format('Wind is blowing from {0} at {1}', wind_from_direction, windspeed_segment, )
        
    def _parse_wind_speed(self, raw_segment_string: str) -> str:
        windspeed_str = ''
        windspeed_segment = raw_segment_string[3:-2]
        if windspeed_segment.lower().find('g') != -1:
            speed_segments = windspeed_segment.lower().split(sep='g')
            windspeed_str = str.format('{0} kts gusting to {1} kts', speed_segments[0], speed_segments[1])
        else:
            windspeed_str = str.format('{0} kts', windspeed_segment)
        return windspeed_str

    def _parse_raw_string(self, raw_string: str) -> str:
        segments = str.split(raw_string, ' ')
        report_segments = []
        for segment in segments:
            if self._is_extreme_variable_wind_segment(segment):
                report_segments.append(self._get_extreme_variable_wind_report(segment))
            else:
                report_segments.append(self._get_normal_wind_report(segment))
        return str.join(' ', report_segments)


class VisibilitySegment(ParsableSegmentAbc):

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        segment = string_segments[5]
        return segment

    def _parse_raw_string(self, raw_string: str) -> str:
        prevailing_visibility = raw_string[0:-2]
        
        prevailing_visibility = str.format('{0} statute miles', prevailing_visibility)
        return prevailing_visibility


