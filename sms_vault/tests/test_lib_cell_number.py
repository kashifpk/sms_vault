import unittest
from ..lib.cell_number import normalize


class TestCellNumber(unittest.TestCase):
    "Tests for lib.cell_number module"

    country_code = '92'
    network_code = '3'
    
    def test_normalize(self):
        "Test cell numbers normalization"
        
        self.assertEqual('+923451234567',
                         normalize('+923451234567', self.country_code, self.network_code))
        
        self.assertEqual('+923451234567',
                         normalize('03451234567', self.country_code, self.network_code))
    
        self.assertEqual('+923451234567',
                         normalize('00923451234567', self.country_code, self.network_code))
        
        self.assertEqual('+923451234567',
                         normalize('0345 1234567', self.country_code, self.network_code))
        
        self.assertEqual('+923451234567',
                         normalize('0345-1234567', self.country_code, self.network_code))
        
        self.assertEqual('+923451234567',
                         normalize('+92-345-1234567', self.country_code, self.network_code))