'''
Created on Oct 15, 2012

@author: tkr2
'''
from __future__ import print_function

from coinor.gimpy import BinaryTree

if __name__ == '__main__':
    T = BinaryTree(display = 'pygame')
    T.add_root(0, label = '*')
    T.add_left_child(1, 0, label = '+')
    T.add_left_child(2, 1, label = '4')
    T.add_right_child(3, 1, label = '5')
    T.add_right_child(4, 0, label = '7')
    T.printexp(True)
    print()
    T.postordereval(True)
