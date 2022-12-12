import unittest
from abc import ABCMeta, abstractmethod

class MetarTestAbc(unittest.TestCase):

    __metaclass__ = ABCMeta

    metar_example_string_normal = 'METAR KGGG 161753Z AUTO 14021G26KT 3/4SM ' \
            + '+TSRA BR BKN008 OVC012CB 18/17 A2970 RMK PRESFR'

    metar_example_string_phx = 'KPHX 110051Z 24004KT 10SM CLR 16/05 A3004 RMK AO2 SLP168 T01560050'
    
    metar_example_string_extreme_variable_wind = 'METAR KGGG 161753Z AUTO VRB21G26KT 030V091  3/4SM ' \
            + '+TSRA BR BKN008 OVC012CB 18/17 A2970 RMK PRESFR'