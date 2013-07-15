from gimpy import BinaryTree
import random

if __name__=='__main__':
    t = BinaryTree(display='pygame')
    t.add_root(0)
    t.add_left_child(1, 0, label='lc', color='red')
    t.add_right_child(2, 0, label='rc', color='red')
    t.add_right_child(3, 2, label='rrc', color='green')
    t.dfs()
    # check postordereval
    # check printexp


