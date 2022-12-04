from abc import ABCMeta, abstractmethod

class ParsableSegmentAbc:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self._raw_string: str = ''

    def parse(self, raw_string: str) -> str:
        self._raw_string = raw_string
        return self._parse_raw_string(raw_string)

    @abstractmethod
    def _parse_raw_string(self, raw_string: str) -> str:
        pass