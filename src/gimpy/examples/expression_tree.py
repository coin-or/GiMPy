from __future__ import print_function
try:
    from src.gimpy import BinaryTree
except ImportError:
    from coinor.gimpy import BinaryTree
    
T = BinaryTree()
T.add_root('*')
T.add_left_child('+', '*')
T.add_left_child('4', '+')
T.add_right_child('5', '+')
T.add_right_child('7', '*')
T.set_display_mode('matplotlib')
T.display()
T.printexp()
print()
T.postordereval()
print()
