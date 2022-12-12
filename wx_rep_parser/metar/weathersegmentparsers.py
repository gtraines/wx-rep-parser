from abscore import ParsableSegmentAbc


class WeatherQualifierSegment(ParsableSegmentAbc):
    _segment_starts_with = [
        '-',
        '+',
        'vc',
        'mi',
        'bc',
        'dr',
        'bl',
        'sh',
        'ts',
        'fz',
        'pr'
    ]

    def _get_string_from_segments(self, string_segments: list[str]) -> str:

        for segment in string_segments:
            if segment.lower().startswith(self._segment_starts_with):
                return segment
        return ''

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
 