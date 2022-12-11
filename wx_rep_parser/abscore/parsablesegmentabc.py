from abc import ABCMeta, abstractmethod

class ParsableSegmentAbc:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self._raw_string: str = ''

    @abstractmethod
    def _get_string_from_segments(self, string_segments: list[str]) -> str:
        pass

    @abstractmethod
    def _parse_raw_string(self, raw_string: str) -> str:
        pass

    def parse(self, raw_string: str) -> str:
        self._raw_string = raw_string
        segments = str.split(raw_string, ' ')
        string_segment = self._get_string_from_segments(segments)
        return self._parse_raw_string(string_segment)


class StringParser:

    def __init__(self, args:list[str]) -> None:

        self._args = args

    def parse_args(self) -> str:

        return str.join(', ', self._args) 
        
