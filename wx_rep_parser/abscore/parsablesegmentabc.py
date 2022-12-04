from abc import ABCMeta, abstractmethod


class ParsableSegmentAbc:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self._rawstring = ''
        
    @abstractmethod
    def parse(self, rawstring):
        pass