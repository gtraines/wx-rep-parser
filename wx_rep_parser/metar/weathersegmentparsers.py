from abscore import ParsableSegmentAbc


class WeatherSegmentBase(ParsableSegmentAbc):
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


class WeatherQualifierSegment(WeatherSegmentBase):

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


class PrecipitationSegmentParser(WeatherSegmentBase):
    
    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        if self._has_precipitation_discriminator(string_segments):
            return self._get_precipitation_descriminator(string_segments)
        return ''
    
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
 