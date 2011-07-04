import decimal 
import json
from .constants import * 

def parse_json(string):
    try:
        return json.loads(string, parse_float=decimal.Decimal)
    except ValueError:
        raise ValueError("Malformed JSON response: %s" % (string,))

class Underflow(Exception):
    def __init__(self, value, precision):
        Exception.__init__(self, ("Overspecified the precision of %s.  "
                                  "Limited to %s digits." % (value, precision)))
        self.value = value
        self.precision = precision 

def listify(gen):
    "Convert a generator into a function which returns a list"
    def patched(*args, **kwargs):
        return list(gen(*args, **kwargs))
    return patched


def parse_order(order):
    quantity, usd = map(decimal.Decimal, order.split('@'))
    
    if quantity.quantize(QUANT_PRECISION) != quantity:
        raise Underflow(quantity, 8)
    if usd.quantize(USD_PRECISION) != usd:
        raise Underflow(usd, 5)
    return quantity, usd
