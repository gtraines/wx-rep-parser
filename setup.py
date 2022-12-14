import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="wx-rep-parser",
    version="0.0.1",
    author="Graham Traines",
    author_email="THIS_IS_NOT_AN@email.com",
    description=("Aviation weather report parser"),
    license="BSD I guess",
    url="http://packages.python.org/update_later",
    packages=['wx_rep_parser', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)