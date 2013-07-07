'''
Tree class built on top of Graph class.

TODO(aykut):
-> root argument in DFS, BFS and traverse. Is it a Node instance or string?
-> Is self.root a Node() or string?
'''

from graph import Graph, Node
from global_constants import *
from blimpy import Stack, Queue
import operator

class Tree(Graph):
    '''
    Tree class. It inherits from Graph class. Provides DFS, BFS and traverse
    methods.
    '''
    def __init__(self, **attrs):
        '''
        API: __init__(self, **attrs)
        Description:
            Constructor. Sets attrbutes of class using argument.
        Input:
            attrs: Attributes in keyword arguments format.
        '''
        attrs['type'] = DIRECTED_GRAPH
        if 'layout' not in attrs:
            attrs['layout'] = 'dot'
        Graph.__init__(self, **attrs)
        self.root = None

    def get_children(self, n):
        '''
        API: get_children(self, n)
        Description:
            Returns list of children of node n.
        Pre:
            Node with name n should exist.
        Input:
            n: Node name.
        Return:
            Returns list of names of children nodes of n.
        '''
        return self.get_neighbors(n)

    def get_parent(self, n):
        '''
        API: get_parent(self, n)
        Description:
            Returns parent node name if n's parent exists, returns
            None otherwise.
        Pre:
            Node with name n should exist.
        Input:
            n: Node name.
        Return:
            Returns parent name of n if its parent exists, returns None
            otherwise.
        '''
        n = self.get_node(n)
        return n.get_attr('parent')

    def add_root(self, root, **attrs):
        '''
        API: add_root(self, root, **attrs)
        Description:
            Adds root node to the tree with name root and returns root Node
            instance.
        Input:
            root: Root node name.
            attrs: Root node attributes.
        Post:
            Changes self.root.
        Return:
            Returns root Node instance.
        '''
        attrs['level'] = 0
        self.root = self.add_node(root, **attrs)
        return self.root

    def add_child(self, n, parent, **attrs):
        '''
        API: add_child(self, n, parent, **attrs)
        Description:
            Adds child n to node parent and return Node n.
        Pre:
            Node with name parent should exist.
        Input:
            n: Child node name.
            parent: Parent node name.
            attrs: Attributes of node being added.
        Post:
            Updates Graph related graph data attributes.
        Return:
            Returns n Node instance.
        '''
        attrs['level'] = self.get_node(parent).get_attr('level') + 1
        attrs['parent'] = parent
        self.add_node(n, **attrs)
        self.add_edge(parent, n)
        return self.get_node(n)

    def dfs(self, root = None, display = None):
        '''
        API: dfs(self, root = None, display = None)
        Description:
            Searches tree starting from node named root using depth-first
            strategy if root argument is provided. Starts search from root node
            of the tree otherwise.
        Pre:
            Node indicated by root argument should exist.
        Input:
            root: Starting node name.
            display: Display argument.
        '''
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        self.traverse(root, display, Stack())

    def bfs(self, root = None, display = None):
        '''
        API: bfs(self, root = None, display = None)
        Description:
            Searches tree starting from node named root using breadth-first
            strategy if root argument is provided. Starts search from root node
            of the tree otherwise.
        Pre:
            Node indicated by root argument should exist.
        Input:
            root: Starting node name.
            display: Display argument.
        '''
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        self.traverse(root, display, Queue())

    def traverse(self, root = None, display = None, q = Stack()):
        '''
        API: traverse(self, root = None, display = None, q = Stack())
        Description:
            Traverses tree starting from node named root. Used strategy (BFS,
            DFS) is controlled by argument q. It is a DFS if q is Queue(), BFS
            if q is Stack(). Starts search from root argument if it is given.
            Starts from root node of the tree otherwise.
        Pre:
            Node indicated by root argument should exist.
        Input:
            root: Starting node name.
            display: Display argument.
            q: Queue data structure instance. It is either a Stack() or
            Queue().
        '''
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
    '''
    Binary tree class. Inherits Tree class. Provides methods for adding
    left/right childs and binary tree specific DFS and BFS methods.
    '''
    def __init__(self, **attrs):
        '''
        API: __init__(self, **attrs)
        Description:
            Class constructor.
        Input:
            attrs: Tree attributes in keyword arguments format. See Graph and
            Tree class for details.
        '''
        Tree.__init__(self, **attrs)

    def add_root(self, root, **attrs):
        '''
        API: __init__(self, **attrs)
        Description:
            Class constructor.
        Input:
            attrs: Tree attributes in keyword arguments format. See Graph and
            Tree class for details.
        '''
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
        if isinstance(n, Node):
            return n.get_attr('Rchild')
        return self.get_node_attr(n, 'Rchild')

    def get_left_child(self, n):
        if isinstance(n, Node):
            return n.get_attr('Lchild')
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
            display = self.attr['display']
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
