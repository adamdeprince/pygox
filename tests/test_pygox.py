#!/usr/bin/env python

import unittest
from pygox import *

SELL_ORDER="""{"status": "Your order has been queued for execution", "orders": [{"status": 2, "priority": "1309529776562400", "item": "BTC", "price": 20, "oid": "57ab542d-6386-49e1-b5e7-377af4658871", "dark": 0, "currency": "USD", "amount": 0.01, "date": 1309529776, "type": 1}]}"""

class TestSellOrder(unittest.TestCase):
    
    def setUp(self):
        self.so = SellOrder.parse_many(parse_json(SELL_ORDER))
        self.order = self.so[0]
        
    def test_order_isa_sell_order(self):
        self.assertTrue(isinstance(self.order, SellOrder))

    def test_amount(self):
        self.assertEquals(self.order.amount, decimal.Decimal('0.01'))

    def test_amount_type(self):
        self.assertTrue(isinstance(self.order.amount, decimal.Decimal))

    def test_currency(self):
        self.assertEquals(self.order.currency, 'USD')

    def test_date(self):
        self.assertEquals(self.order.date, datetime.datetime(2011, 7, 1, 10, 16, 16))

    def test_no_type(self):
        self.assertFalse(hasattr(self.order, 'type'))

    def test_parsed_file_has_one_orer(self):
        self.assertEquals(len(self.so), 1)

    def test_status_message(self):
        self.assertEquals(self.order.message, 'Your order has been queued for execution')

    def test_status(self):
        self.assertEquals(self.order.status, 2)

    def test_priority(self):
        self.assertEquals(self.order.priority, long(1309529776562400))
        
    def test_priortiy_is_correct_type(self):
        self.assertTrue(isinstance(self.order.priority, (int, long)))

    def test_item(self):
        self.assertEquals(self.order.item, 'BTC') 

    def test_price(self):
        self.assertEquals(self.order.price, decimal.Decimal('20'))

    def test_price_type(self):
        self.assertTrue(isinstance(self.order.price, decimal.Decimal))

    def test_oid(self):
        self.assertEquals(self.order.oid, '57ab542d-6386-49e1-b5e7-377af4658871')

    def test_dark(self):
        self.assertEquals(self.order.dark, False)

    def test_dark_type(self):
        self.assertTrue(isinstance(self.order.dark, bool))

    
    
if __name__ == "__main__":
    unittest.main()
