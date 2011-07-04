"""Python calls for the Mt Gox API."""

import itertools 
import time 
import json
import pycurl
import StringIO
import urllib
import decimal 
import datetime 
import os

pycurl.global_init(pycurl.GLOBAL_SSL)

SELL_TYPE = 1 
BUY_TYPE = 2 

from .utils import parse_json, listify

class DictToAttrMapper:
    MAPPER = {}
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            func = self.MAPPER.get(key, lambda x:x)
            if func is not None:
                setattr(self, key, func(value))

    def __cmp__(self, other):
        if isinstance(other, type(self)):
            return cmp(tuple(self.__me__()), tuple(other.__me__()))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return isinstance(other, type(self)) and not self.__cmp__(other)
    
    def __hash__(self):
        return hash(tuple(self.__me__()))

class DictToAttrMapperOnlyFields:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.FIELDS: continue 
            func = self.MAPPER.get(key, lambda x:x)
            if func is not None:
                setattr(self, key, func(value))


class Order(DictToAttrMapper):

    @classmethod
    def parse(cls, parse, message=None):
        by_order_type = {1:SellOrder,
                         2:BuyOrder}
        return by_order_type.get(int(parse['type'])).parse(parse, message)
        

    MAPPER = dict(amount=decimal.Decimal,
                  date=datetime.datetime.fromtimestamp,
                  status=int,
                  priority=int,
                  price=decimal.Decimal,
                  dark=bool,
                  type=None
                  )

    @classmethod 
    @listify
    def parse_many(cls, orders):
        message = orders.get('status')
        print orders
        orders = orders['orders']

        for order in orders:
            yield cls.parse(order, message)
        
class SubOrder(Order):

    @classmethod
    def parse(cls, order, message=None):
        if message:
            order['message'] = message
        return cls(**order)

class SellOrder(SubOrder):
    def __str__(self):
        return "<SellOrder amount=%s date=%s status=%s priority=%s price=%s dark=%s oid=%s>" % (
            self.amount, self.date, self.status, self.priority, self.price, self.dark, self.oid)

    order_type = SELL_TYPE

class BuyOrder(SubOrder):
    def __str__(self):
        return "<BuyOrder amount=%s date=%s status=%s priority=%s price=%s dark=%s, oid=%s>" % (
            self.amount, self.date, self.status, self.priority, self.price, self.dark, self.oid)
    order_type = BUY_TYPE

class Trade(DictToAttrMapperOnlyFields):
    FIELDS = set(['price', 'tid', 'amount', 'date'])
    MAPPER = dict(price=decimal.Decimal,
                  tid = long,
                  amount = decimal.Decimal,
                  date = datetime.datetime.fromtimestamp)
    
    def __str__(self):
        return "<Trade price=%s amount=%s date=%s tid=%s>" % (
            self.price, self.amount, self.date, self.tid)
    
class Funds(DictToAttrMapper):
    def __str__(self):
        return "<Funds usd=%s, btc=%s>" % (self.usds, self.btcs)

class Ticker(DictToAttrMapper):
    def __init__(self, **kwargs):
        DictToAttrMapper.__init__(self, **kwargs['ticker'])

    def __str__(self):
        return "<Ticker buy=%s, sell=%s, last=%s, vol=%s, high=%s, low=%s, avg=%s>" % self.__me__()
    
    def __me__(self):
        return (self.buy, self.sell, self.last, self.vol, self.high, self.low, self.avg)
        

class Bid():
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume 

    def __str__(self):
        return "<Bid price=%s, volume=%s>" % (self.price, self.volume)


USER_AGENT = ["UserAgent: PYGox Version 0.01"]

class UseLibCurl:

    def common_initialization(self, curl):
        curl.setopt(pycurl.HTTPHEADER, ["Accept: */*", "User-Agent: pygox/0.0.0"])
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        
    def _get(self, url):
        curl = pycurl.Curl()
        body = StringIO.StringIO()
        curl.setopt(pycurl.URL, url)
        self.common_initialization(curl)
        curl.setopt(pycurl.WRITEFUNCTION, body.write)
        curl.perform()
        return body.getvalue()

    def _post(self, url, **post):
        curl = pycurl.Curl()
        body = StringIO.StringIO()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.POST, 1)
        self.common_initialization(curl)
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(post))
        curl.setopt(pycurl.WRITEFUNCTION, body.write)        
        curl.perform()
        return body.getvalue()

class Connection(UseLibCurl):
    def __init__(self):
        pass

    def get(self, function):
        return parse_json(self._get("https://mtgox.com/code/data/%s.php" % (function,)))
        
    def getTicker(self):
        return Ticker(**self.get('ticker'))

    @listify
    def getTrades(self):
        for trade in self.get('getTrades'):
            yield Trade(**trade)

    @listify
    def getDepth(self):
        for bid in self.get('getDepth')['bids']:
            yield Bid(*bid)

class AuthenticationError(Exception):
    pass

class AuthenticatedConnection(Connection):
    def __init__(self, username=None, password=None):
        Connection.__init__(self)
        self.username = username or os.environ.get('MTGOX_USERNAME')
        self.password = password or os.environ.get('MTGOX_PASSWORD')

    def post(self, function, **params):
        params = dict(params)
        params['name'] = self.username
        params['pass'] = self.password
        data = self._post("https://mtgox.com/code/%s.php" % (function,),
                   **params)
        return parse_json(data)

    def getFunds(self):
        return Funds(**self.post('getFunds'))

    def sell(self, amount, price):
        return self.post('sellBTC', amount=amount, price=price)

    def buy(self, amount, price):
        return self.post('buyBTC', amount=amount, price=price)

    def cancelSell(self, oid):
        return self._cancelOrder(oid, SELL_TYPE)
        
    def cancelBuy(self, oid):
        return self._cancelOrder(oid, BUY_TYPE)

    def cancel(self, order):
        if hasattr(order, 'oid') and hasattr(order, 'order_type'):
            return self._cancelOrder(order.oid, order.order_type)
        if hasattr(order, 'oid'):
            oid = order.oid
        else:
            oid = order
        for order in self.getOrders():
            if order.oid == oid:
                return self.cancel(order)
        
    def _cancelOrder(self, oid, order_type):
        return self.post('cancelOrder', oid=oid, type=order_type)

    def getOrders(self):
        return Order.parse_many(self.post('getOrders'))

class RobotConnection(AuthenticatedConnection):
    DEFAULT_DELAY = 60
    def cancelAllOrders(self):
        orders = self.getOrders()
        while orders:
            for order in orders:
                self.cancel(order)
            orders = self.getOrders()

    def ticker(self, delay=DEFAULT_DELAY, history = None):
        if not history:
            history = {}
        old_ticker = None
        while True:
            new_ticker = self.getTicker()
            if new_ticker == old_ticker:
                yield None
            else:
                trades = self.getTrades()
                trades = sorted((trade for trade in trades if trade.tid not in history), key=lambda x:x.tid)
            
                for trade in trades:
                    yield trade
                    history[trade.tid] = trade 
            time.sleep(delay)
            old_ticker = new_ticker 
        
