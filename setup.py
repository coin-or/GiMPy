#!/usr/bin/env python

from distutils.core import setup

setup(name='Distutils',
      version='1.0',
      description='Graph Methods in Python (GiMPy)',
      author='Aykut Bulut, Ted Ralphs',
      author_email='aykut@lehigh.edu',
      url='http://projects.coin-or.org/CoinBazaar/wiki/Projects/GIMPy',
      packages=['gimpy','blimpy'],
      package_dir = {'': 'src'},
     )
