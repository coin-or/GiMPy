'''
Created on Oct 15, 2012

@author: tkr2
'''
from coinor.gimpy import BinaryTree

if __name__ == '__main__':
#     T = BinaryTree(display = 'matplotlib')
#     T.add_root(0, label = '*')
#     T.add_left_child(1, 0, label = '+')
#     T.add_left_child(2, 1, label = '4')
#     T.add_right_child(3, 1, label = '5')
#     T.add_right_child(4, 0, label = '7')
#     T.printexp(True)
#     print()
#     T.postordereval(True)

    T = BinaryTree(display = 'matplotlib')
    T.add_root(0)
    T.add_left_child(1, 0)
    T.add_left_child(2, 1)
    T.add_right_child(3, 1)
    T.add_right_child(4, 0)
    T.add_right_child(5, 4)
    T.add_left_child(6, 4)
    T.add_right_child(7, 6)
    T.print_nodes(order = 'in')
#    T.dfs()
#    T.bfs()
