from gimpy import Tree
import random

if __name__=='__main__':
    t = BinaryTree(display='pygame')
    t.add_root(0)
    for i in range(1,20):
        parent = random.randint(0,i-1)
        t.add_child(i, parent)
    t.bfs()

