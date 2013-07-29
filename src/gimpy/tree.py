'''
Tree class built on top of Graph class.
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
        API: add_root(self, root, **attrs)
        Description:
            Adds root node to the binary tree.
        Input:
            root: Name of the root node.
            attrs: Attributes of the root node.
        Post:
            Changes self.root attribute.
        '''
        Tree.add_root(self, root, **attrs)

    def add_right_child(self, n, parent, **attrs):
        '''
        API: add_right_child(self, n, parent, **attrs)
        Description:
            Adds right child n to node parent.
        Pre:
            Right child of parent should not exist.
        Input:
            n: Node name.
            parent: Parent node name.
            attrs: Attributes of node n.
        '''
        if self.get_right_child(parent) is not None:
            msg = "Right child already exists for node " + str(parent)
            raise Exception(msg)
        attrs['direction'] = 'R'
        self.set_node_attr(parent, 'Rchild', n)
        self.add_child(n, parent, **attrs)

    def add_left_child(self, n, parent, **attrs):
        '''
        API: add_left_child(self, n, parent, **attrs)
        Description:
            Adds left child n to node parent.
        Pre:
            Left child of parent should not exist.
        Input:
            n: Node name.
            parent: Parent node name.
            attrs: Attributes of node n.
        '''
        if self.get_left_child(parent) is not None:
            msg = "Right child already exists for node " + str(parent)
            raise Exception(msg)
        attrs['direction'] = 'L'
        self.set_node_attr(parent, 'Lchild', n)
        self.add_child(n, parent, **attrs)

    def get_right_child(self, n):
        '''
        API: get_right_child(self, n)
        Description:
            Returns right child of node n. n can be Node() instance or string
            (name of node).
        Pre:
            Node n should be present in the tree.
        Input:
            n: Node name or Node() instance.
        Return:
            Returns name of the right child of n.
        '''
        if isinstance(n, Node):
            return n.get_attr('Rchild')
        return self.get_node_attr(n, 'Rchild')

    def get_left_child(self, n):
        '''
        API: get_left_child(self, n)
        Description:
            Returns left child of node n. n can be Node() instance or string
            (name of node).
        Pre:
            Node n should be present in the tree.
        Input:
            n: Node name or Node() instance.
        Return:
            Returns name of the left child of n.
        '''
        if isinstance(n, Node):
            return n.get_attr('Lchild')
        return self.get_node_attr(n, 'Lchild')

    def del_node(self, n):
        '''
        API: del_node(self, n)
        Description:
            Removes node n from tree.
        Pre:
            Node n should be present in the tree.
        Input:
            n: Node name.
        '''
        parent = self.get_node_attr(n, 'parent')
        if self.get_node_attr(n, 'direction') == 'R':
            self.set_node_attr(parent, 'Rchild', None)
        else:
            self.set_node_attr(parent, 'Lchild', None)
        Graph.del_node(self, n)

    def print_nodes(self, order = 'in', priority = 'L', display = None,
                    root = None):
        '''
        API: print_nodes(self, order = 'in', priority = 'L', display = None,
                    root = None)
        Description:
            A recursive function that prints nodes to stdout starting from
            root.
        Input:
            order: Order of printing. Acceptable arguments are 'pre', 'in',
            'post'.
            priority: Priority of printing, acceptable arguments are 'L' and
            'R'.
            display: Display mode.
            root: Starting node.
        '''
        old_display = None
        if root == None:
            root = self.root.name
        if display == None:
            display = self.attr['display']
        else:
            old_display = self.attr['display']
            self.attr['display'] = display
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
        if old_display:
            self.attr['display'] = old_display

    def dfs(self, root = None, display = None, priority = 'L'):
        '''
        API: dfs(self, root=None, display=None, priority='L', order='in')
        Description:
            Searches tree starting from node named root using depth-first
            strategy if root argument is provided. Starts search from root node
            of the tree otherwise.
        Input:
            root: Starting node.
            display: Display mode.
            priority: Priority used when exploring children of the node.
            Acceptable arguments are 'L' and 'R'.
        '''
        if root == None:
            root = self.root
        self.traverse(root, display, Stack(), priority)

    def bfs(self, root = None, display = None, priority = 'L'):
        '''
        API: bfs(self, root=None, display=None, priority='L', order='in')
        Description:
            Searches tree starting from node named root using breadth-first
            strategy if root argument is provided. Starts search from root node
            of the tree otherwise.
        Input:
            root: Starting node.
            display: Display mode.
            priority: Priority used when exploring children of the node.
            Acceptable arguments are 'L' and 'R'.
        '''
        if root == None:
            root = self.root
        self.traverse(root, display, Queue(), priority)

    def traverse(self, root = None, display = None, q = Stack(),
                 priority = 'L'):
        '''
        API: traverse(self, root=None, display=None, q=Stack(), priority='L',
                      order='in')
        Description:
            Traverses tree starting from node named root if root argument is
            provided. Starts search from root node of the tree otherwise. Search
            strategy is determined by q data structure. It is DFS if q is
            Stack() and BFS if Queue().
        Input:
            root: Starting node.
            display: Display mode.
            q: Queue data structure, either Queue() or Stack().
            priority: Priority used when exploring children of the node.
            Acceptable arguments are 'L' and 'R'.
            order: Ineffective, will be removed.
        '''
        old_display = None
        if root == None:
            root = self.root
        if display == None:
            display = self.attr['display']
        else:
            old_display = self.attr['display']
            self.attr['display'] = display
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
        if old_display:
            self.attr['display'] = old_display

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
        if isinstance(root, Node):
            print root.get_attr('label')
        else:
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
        if isinstance(root, Node):
            print root.get_attr('label')
        else:
            print self.get_node_attr(root, 'label'),
        if display:
                self.display(highlight = [root])
        if self.get_right_child(root):
            res2 = self.postordereval(display, self.get_right_child(root))
        if res1 and res2:
            if isinstance(root, Node):
                val = root.get_attr('label')
            else:
                val = self.get_node_attr(root, 'label')
            print '=', opers[val](res1 , res2)
            if display:
                self.display(highlight = [root])
            print opers[val](res1 , res2),
            return opers[val](res1 , res2)
        else:
            return int(self.get_node_attr(root, 'label'))


if __name__ == '__main__':
    pass
