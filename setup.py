import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pygox",
    version = "0.0.0",
    author = "Adam DePrince",
    author_email = "deprince@googlealumni.com",    
    description = "A API to MtGox",
    license = "GPLV3",
    keywords = "btc bitcoin mtgox",
    url = "http://adamdeprince.com/pygox",
    download_url = "http://adamdeprince.com/pygox/pygox-0.0.0.tar.gz",
    requires = ["pycurl"],
    packages=["pygox"],
    # long_description=read('README'),
)
