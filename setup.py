import os
from setuptools import setup
from pygox import VERSION 

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



setup(
    name = "pygox",
    version = VERSION,
    author = "Adam DePrince",
    author_email = "deprince@googlealumni.com",    
    description = "A API to MtGox",
    license = "GPLV3",
    keywords = "btc bitcoin mtgox",
    url = "http://adamdeprince.com/pygox",
    download_url = "http://adamdeprince.com/pygox/pygox-%s.tar.gz" % VERSION,
    requires = ["pycurl", "nose"],
    packages=["pygox"],
    test_suite="nose.collector",
    # long_description=read('README'),
)
