from pygox import * 
import unittest
import json
import decimal


class TestParseJSON(unittest.TestCase):
    def test_floats_are_decimals(self):
        self.assertEquals(type(parse_json(json.dumps(0.5))), decimal.Decimal)

class TestListify(unittest.TestCase):
    @listify
    def func(self):
        yield 1
        yield 2

    def test_listify_generates_correct_results(self):
        self.assertEquals(self.func(), [1, 2])

    def test_listify_returns_list(self):
        self.assertEquals(type(self.func()), list)
        
class TestOrderParsing(unittest.TestCase):
    def test_order(self):
        self.assertEquals(parse_order("1.2@2.3"), (decimal.Decimal("1.2"), decimal.Decimal("2.3")))

    def test_order_types(self):
        self.assertEquals(map(type, parse_order("1.2@2.3")), [decimal.Decimal] * 2)
        
    def test_underflows_on_quanitity(self):
        self.assertRaises(Underflow, lambda :parse_order("1.00000000000000001@2.3",))

    def test_underflows_on_price(self):
        self.assertRaises(Underflow, lambda :parse_order("1.001@2.300000000001",))
    
    
if __name__ == "__main__":
    unittest.main()
