import decimal 
import json
from .constants import * 
import sys 

class MtGoxException(Exception):
    pass
                      

def parse_json(string):
    try:
        value = json.loads(string, parse_float=decimal.Decimal)
        if 'error' in value:
            raise MtGoxException(value['error'])
        return value 
    except ValueError:
        raise ValueError("Malformed JSON response: %s" % (string,))

def listify(gen):
    "Convert a generator into a function which returns a list"
    def patched(*args, **kwargs):
        return list(gen(*args, **kwargs))
    return patched

class ParseOrderException(Exception):
    def __init__(self, msg, value):
        Exception.__init__(self, msg)
        self.value = value

class Underflow(ParseOrderException):
    def __init__(self, value, precision):
        Exception.__init__(self, ("Overspecified the precision of %s.  "
                                  "Limited to %s digits." % (value, precision)),
                           value)
        self.precision = precision 

class MalformedOrder(ParseOrderException):
    def __init__(self, value):
        Exception.__init__(self, "Malformed value %r expecting of form [0-9]+(\.[0-9]+){0,1}@[0-9]+(\.[0-9]+){0,1}" % (value,), value)

def parse_order(order):
    try:
        quantity, usd = map(decimal.Decimal, order.split('@'))
    except decimal.InvalidOperation:
        raise MalformedOrder(order)
    
    
    if quantity.quantize(QUANT_PRECISION) != quantity:
        raise Underflow(quantity, 8)
    if usd.quantize(USD_PRECISION) != usd:
        raise Underflow(usd, 5)
    return quantity, usd

def simple_command_line_main(args, verb, function, 
                             to_print=lambda x='':sys.stderr.write(x + "\n")):

    why = ""
    try:
        args = map(parse_order, args)
    except ParseOrderException, ex:
        args = []
        why = str(ex)
    if not args:
        if why:
            to_print(why)
        to_print("Usage: %(verb)s 1@2 1.1@2.2" % vars())
        to_print()
        to_print("Creates two orders to %(verb)s 1 bit coin at 2 USD and 1.1 bit coins at $2.20USD" % vars())
        return 1
        
    for arg in args:
        function(*arg)
    return 0
