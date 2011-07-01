import unittest

class TestSellOrder(unittest.TestCase):
    SELL_ORDER="{u'status': u'Your order has been queued for execution', u'orders': [{u'status': 2, u'priority': u'1309529776562400', u'i
tem': u'BTC', u'price': 20, u'oid': u'57ab542d-6386-49e1-b5e7-377af4658871', u'dark': 0, u'currency': u'USD', u'amount': 
Decimal('0.01'), u'date': 1309529776, u'type': 1}]}"
    
    def setUp(self):
        self.so = SellOrder.parse(parse_order(SELL_ORDER))
        self.order = self.so[0]

    def test_amount(self):
        self.assertEquals(self.so.amount, decimal.Decimal('0.01'))

    def test_amount_type(self):
        self.assertTrue(isinstance(self.so.amount, decimal.Decimal))

    def test_currency(self):
        self.assertTrue(self.so.currency, 'USD')

    def test_date(

    def test_parsed_file_has_one_orer(self):
        self.assertEquals(len(self.so), 1)

    def test_status_message(self):
        self.assertEquals(self.so.message, 'Your order has been queued for execution')

    def test_status(self):
        self.assertEquals(self.so.status, 2)

    def test_priority(self):
        self.assertEquals(self.so.priority, long(1309529776562400))
        
    def test_priortiy_is_correct_type(self):
        self.assertTrue(isinstance(self.so.priority, (int, long)))

    def test_item(self):
        self.assertEquals(self.so.item, 'BTC') 

    def test_price(self):
        self.assertEquals(self.so.price, decimal.Decimal('20'))

    def test_price_type(self):
        self.assertTrue(isinstantce(self.so.price, decimal.Decimal))

    def test_oid(self):
        self.assertEquals(self.so.oid, '57ab542d-6386-49e1-b5e7-377af4658871')

    def test_dark(self):
        self.assertEquals(self.dark, False)

    def test_dark_type(self):
        self.assertTrue(isinstance(self.dark, bool))

    
    
