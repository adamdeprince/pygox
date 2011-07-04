import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from pygox import VERSION 

setup(
    name = "pygox",
    version = VERSION,
    author = "Adam DePrince",
    author_email = "deprince@googlealumni.com",    
    description = "A API to MtGox",
    license = "GPLV3",
    keywords = "btc bitcoin mtgox",
    url = "http://adamdeprince.com/pygox",
    download_url = "http://adamdeprince.com/pygox/pygox-%(VERSION)s.tar.gz" % vars(),
    requires = ["pycurl"],
    packages=["pygox"],
    scripts=["commands/pygox_buy", "commands/pygox_sell", "commands/pygox_cancel_all_orders", "commands/pygox_spot"]
    # long_description=read('README'),
)
