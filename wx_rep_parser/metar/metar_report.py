from datetime import datetime
from dateutil import tz
from wx_rep_parser.abscore import ParsableSegmentAbc


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


class PrecipitationDiscriminatorSegmentParser(ParsableSegmentAbc):

    def _has_precipitation_discriminator(self, string_segments: list[str]) -> bool:
        for entry in string_segments:
            if entry.lower() == 'a01' or entry.lower() == 'a02':
                return True
        return False

    def _get_precipitation_descriminator(self, string_segments: list[str]) -> str:
        for entry in string_segments:
            if entry.lower() == 'a01' or entry.lower() == 'a02':
                return entry
        return ''

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        if self._has_precipitation_discriminator(string_segments):
            return self._get_precipitation_descriminator(string_segments)
        return ''

    def _parse_raw_string(self, raw_string: str) -> str:
        if raw_string.lower() == 'a01':
            return 'prescription discriminator included'
        if raw_string.lower() == 'a02':
            return 'no precipitation discriminator'
        return ''


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


class WeatherQualifierSegment(ParsableSegmentAbc):

    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        segment = string_segments[6]
        return segment

    def _get_intensity_or_proximity(self, raw_string: str) -> str:
        if raw_string[0:1] == '-':
            return 'light'
        if raw_string[0:1] == '+':
            return 'heavy'
        if raw_string[0:2].lower() == 'vc':
            return 'in the vicinity'
        return 'moderate'

    def _get_segment_with_intensity_or_proximity_trimmed(self, raw_string: str) -> str:
        intensity_string = raw_string[0:1]
        if intensity_string == '-' \
            or intensity_string == '+':
            return raw_string[1:]
        if raw_string[0:2].lower() == 'vc':
            return raw_string[2:]
        return raw_string

    def _get_descriptor(self, raw_string: str) -> str:

        trimmed_segment = self._get_segment_with_intensity_or_proximity_trimmed(raw_string)
        
        if len(trimmed_segment) >= 2:
            descriptor_segment = trimmed_segment[0:2].lower()
            if descriptor_segment == 'mi':
                return 'shallow'
            if descriptor_segment == 'bc':
                return 'patches'
            if descriptor_segment == 'dr':
                return 'low drifting'
            if descriptor_segment == 'bl':
                return 'blowing'
            if descriptor_segment == 'sh':
                return 'showers'
            if descriptor_segment == 'ts':
                return 'thunderstorm'
            if descriptor_segment == 'fz':
                return 'freezing'
            if descriptor_segment == 'pr':
                return 'partial'
            
        return ''
        
    def _parse_raw_string(self, raw_string: str) -> str:
        intensity_or_proximity = self._get_intensity_or_proximity(raw_string)
        descriptor = self._get_descriptor(raw_string)       
        if (intensity_or_proximity != ''):
            return str.format('{0} {1}', intensity_or_proximity, descriptor)
        
        return descriptor


class PrecipitationSegment(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        if raw_string is not None and len(raw_string) >= 2:
            precipitation_segment = raw_string[-2:].lower()

            if precipitation_segment == 'dz':
                return 'drizzle'
            if precipitation_segment == 'ra':
                return 'rain'
            if precipitation_segment == 'sn':
                return 'snow'
            if precipitation_segment == 'sg':
                return 'snow grains'
            if precipitation_segment == 'ic':
                return 'ice crystals'
            if precipitation_segment == 'pl':
                return 'ice pellets'
            if precipitation_segment == 'gr':
                return 'hail'
            if precipitation_segment == 'gs':
                return 'small hail or snow pellets'
            if precipitation_segment == 'up':
                return 'unknown precipitation'
        return '' 


class ObscurationSegment(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        obscuration_segment = raw_string.lower()
        if obscuration_segment == 'br':
            return 'mist'
        if obscuration_segment == 'fg':
            return 'fog'
        if obscuration_segment == 'fu':
            return 'smoke'
        if obscuration_segment == 'du':
            return 'dust'
        if obscuration_segment == 'sa':
            return 'sand'
        if obscuration_segment == 'ha':
            return 'haze'
        if obscuration_segment == 'py':
            return 'spray'
        if obscuration_segment == 'va':
            return 'volcanic ash'
        return ''


class OtherPhenomenaSegment(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        other_phenomena = raw_string.lower()

        if other_phenomena == 'po':
            return 'Dust/sand whirls'
        if other_phenomena == 'sq':
            return 'Squalls'
        if other_phenomena == 'fc':
            return 'Funnel cloud'
        if other_phenomena == '+fc':
            return 'Tornado or waterspout'
        if other_phenomena == 'ss':
            return 'Sandstorm'
        if other_phenomena == 'ds':
            return 'Dust storm'

        return ''

class WeatherPhenomenon(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        
        return


class WeatherSegment(ParsableSegmentAbc):

    def _parse_raw_string(self, raw_string: str) -> str:
        
        return ''
    

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