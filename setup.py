#!/usr/bin/env python

from setuptools import setup
import setuptools

setup(name='coinor.gimpy',
      version='1.3.11',
      description='Graph Methods in Python',
      long_description='''GiMPy is yet another graph class in Python. It is part of the COIN-OR software repository (www.coin-or.org). The class includes implementations of a range of standard graph algorithms. The goal of the implementations is clarity and the package includes visualizations for most of the methods. It is intended for educational/research purposes. The implementations are as efficient as possible, but where tradeoffs have to be made, clarity and ability to visualize are emphasized above efficiency. For this reason, the package is pure Python (and thus will not be as fast as other graph classes with C extensions). Visualization is done using Graphviz, which should be installed in order to do any visualization. Graphs can be displayed using either pygame (live), PIL (static), xdot (live), gexf (static display in browser), or dot2tex (set in LaTex).

Documentation for the API is here:

https://coin-or.github.io/GiMPy
''',
      author='Aykut Bulut, Ted Ralphs',
      author_email='{aykut,ted}@lehigh.edu',
      license='Eclipse Public License',
      url='https://github.com/coin-or/GiMPy/',
      namespace_packages=['coinor'],
      packages=['coinor.gimpy','coinor.gimpy.examples','coinor'],
      package_dir = {'coinor': 'src'},
      install_requires=['coinor.blimpy>=1.2.0']
     )
