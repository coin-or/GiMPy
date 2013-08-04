#!/usr/bin/env python

from distutils.core import setup

setup(name='GiMPy',
      version='1.0.0',
      description='Graph Methods in Python',
      long_description='GiMPy is yet another graph class in Python. The class includes implementations of a range of standard graph algorithms. The goal of the implementations is clarity and the package includes visualizations for most of the methods. It is intended for educational/research purposes. The implementations are as efficient as possible, but where tradeoffs have to be made, clarity and ability to visualize are emphasized above efficiency. For this reason, the package is pure Python. Visualization is done using Graphviz, which should be installed in order to do any visualization. Graphs can be displayed using either pygame (live), PIL (static), xdot (live), gexf (static display in browser), or dot2tex (set in LaTex).',
      author='Aykut Bulut, Ted Ralphs',
      author_email='{aykut,ted}@lehigh.edu',
      license='Eclipse Public License',
      url='http://projects.coin-or.org/CoinBazaar/wiki/Projects/GIMPy',
      packages=['gimpy','blimpy'],
      package_dir = {'': 'src'},
     )
