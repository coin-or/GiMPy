'''
Tree class built on top of Graph class.
'''

from graph import Graph, Node
from global_constants import *
from list import Stack, Queue
import operator

class Tree(Graph):
    def __init__(self, **attrs):
        attrs['type'] = DIRECTED_GRAPH
        if 'layout' not in attrs:
            attrs['layout'] = 'dot'
        Graph.__init__(self, **attrs)
        self.root = None

    def get_children(self, n):
        if isinstance(n, Node):
            return self.get_neighbors(n.name)
        else:
            return self.get_neighbors(n)

    def get_parent(self, n):
        if not isinstance(n, Node):
            n = self.get_node(n)
        return self.get_node(self.get_node_attr(n, 'parent'))

    def add_root(self, root, **attrs):
        attrs['level'] = 0
        self.root = self.add_node(root, **attrs)
        return self.root

    def add_child(self, n, parent, **attrs):
        if not isinstance(parent, Node):
            parent = self.get_node(parent)
        attrs['level'] = parent.get_attr('level') + 1
        attrs['parent'] = parent.name
        self.add_node(n, **attrs)
        self.add_edge(parent, n)
        return self.get_node(n)
    
    def dfs(self, root = None, display = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        self.traverse(root, display, Stack())

    def bfs(self, root = None, display = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        self.traverse(root, display, Queue())

    def traverse(self, root = None, display = None, q = Stack()):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        if isinstance(q, Queue):
            addToQ = q.enqueue
            removeFromQ = q.dequeue
        elif isinstance(q, Stack):
            addToQ = q.push
            removeFromQ = q.pop
        addToQ(root)
        while not q.isEmpty():
            current = removeFromQ()
            #print current
            if display:
                self.display(highlight = [current])
            for n in self.get_children(current):
                addToQ(n)


class BinaryTree(Tree):
    def __init__(self, **attrs):
        Tree.__init__(self, **attrs)

    def add_root(self, root, **attrs):
        Tree.add_root(self, root, **attrs)

    def add_right_child(self, n, parent, **attrs):
        if self.get_right_child(parent) is not None:
            raise Exception("Right child already exists for node " + parent)
        attrs['direction'] = 'R'
        self.set_node_attr(parent, 'Rchild', n)
        self.add_child(n, parent, **attrs)

    def add_left_child(self, n, parent, **attrs):
        if self.get_left_child(parent) is not None:
            raise Exception("Left child already exists for node " + parent)
        attrs['direction'] = 'L'
        self.set_node_attr(parent, 'Lchild', n)
        self.add_child(n, parent, **attrs)

    def get_right_child(self, n):
        return self.get_node_attr(n, 'Rchild')

    def get_left_child(self, n):
        return self.get_node_attr(n, 'Lchild')

    def del_node(self, n):
        parent = self.get_node_attr(n, 'parent')
        if self.get_node_attr(n, 'direction') == 'R':
            self.set_node_attr(parent, 'Rchild', None)
        else:
            self.set_node_attr(parent, 'Lchild', None)
        Graph.del_node(self, n)

    def print_nodes(self, order = 'in', priority = 'L', display = None,
                    root = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        if priority == 'L':
            first_child = self.get_left_child
            second_child = self.get_right_child
        else:
            first_child = self.get_right_child
            second_child = self.get_left_child
        if order == 'pre':
            print root
        if first_child(root) is not None:
            if display:
                self.display(highlight = [root])
            self.print_nodes(order, priority, display, first_child(root))
        if order == 'in':
            print root
        if second_child(root) is not None:
            if display:
                self.display(highlight = [root])
            self.print_nodes(order, priority, display, second_child(root))
        if order == 'post':
            print root
        if display:
            self.display(highlight = [root])

    def dfs(self, root = None, display = None, priority = 'L', order = 'in'):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        self.traverse(root, display, Stack(), priority, order)

    def bfs(self, root = None, display = None, priority = 'L', order = 'in'):
        if root == None:
            root = self.root
        if display == None:
            display = self.display_mode
        self.traverse(root, display, Queue(), priority, order)

    def traverse(self, root = None, display = None, q = Stack(),
                 priority = 'L',  order = 'in'):
        if root == None:
            root = self.root
        if display == None:
            display = self.display_mode
        if isinstance(q, Queue):
            addToQ = q.enqueue
            removeFromQ = q.dequeue
        elif isinstance(q, Stack):
            addToQ = q.push
            removeFromQ = q.pop
        if priority == 'L':
            first_child = self.get_left_child
            second_child = self.get_right_child
        else:
            first_child = self.get_right_child
            second_child = self.get_left_child
        addToQ(root)
        while not q.isEmpty():
            current = removeFromQ()
            if display:
                self.display(highlight = [current])
            n = first_child(current)
            if n is not None:
                addToQ(n)
            n = second_child(current)
            if n is not None:
                addToQ(n)

    def printexp(self, display = None, root = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        if self.get_left_child(root):
            print '(',
            if display:
                self.display(highlight = [root])
            self.printexp(display, self.get_left_child(root))
        print self.get_node_attr(root, 'label'),
        if display:
                self.display(highlight = [root])
        if self.get_right_child(root):
            self.printexp(display, self.get_right_child(root))
            print ')',
            if display:
                self.display(highlight = [root])

    def postordereval(self, display = None, root = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        opers = {'+':operator.add, '-':operator.sub, '*':operator.mul,
                 '/':operator.truediv}
        res1 = None
        res2 = None
        if self.get_left_child(root):
            if display:
                self.display(highlight = [root])
            res1 = self.postordereval(display, self.get_left_child(root))
        print self.get_node_attr(root, 'label'),
        if display:
                self.display(highlight = [root])
        if self.get_right_child(root):
            res2 = self.postordereval(display, self.get_right_child(root))
        if res1 and res2:
            print '=', opers[self.get_node_attr(root, 'label')](res1 , res2)
            if display:
                self.display(highlight = [root])
            print opers[self.get_node_attr(root, 'label')](res1 , res2),
            return opers[self.get_node_attr(root, 'label')](res1 , res2)
        else:
            return int(self.get_node_attr(root, 'label'))


if __name__ == '__main__':
    pass
