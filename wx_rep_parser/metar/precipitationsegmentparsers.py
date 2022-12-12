from abscore.parsablesegmentabc import ParsableSegmentAbc


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


class PrecipitationSegmentParser(ParsableSegmentAbc):
    
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

