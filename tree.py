'''
A new Graph class implementation. The aim for this implementation is
1. To reflect implementation methods in leterature as much as possible
2. Removing superflous stuff that comes with pydot
3. To have a more object oriented design

This implementation can be considered as a comprimise between pydot graph
class and an efficient graph data structure.

One deviation from standart Graph implementations is to keep in neighbors in
an other adjacency list. We do this for efficiency resons considering
traversing residual graphs.

We have a class for Graph and a class for Node. Edges are not represented as
objects. They are kept in a dictionary which also keeps their attributes.

Node objects should be used to get an attribute of a Node. We do not have a
get_node_attr() method in Graph class.

It is user's responsibility to name nodes properly (according to dot standarts), Graph class will not check that.

Some portion of code is written using Pydot source code.

There are two attribute sets for Graph and node classes.
1. attributes to keep data (attr), ie for edges cost, capacity etc.
These two attribute sets should not e considered
They may have commons. It is users responsibility to keep coherency of attributes.

For edges we only have edge_attr. User should be aware of this.

Edges are not objects in this implementation and if a user wants to change an edge attribute she should do it directly on edge_attr.

For constructor attr arguments:
They will all be in self.attr

Default is an undirected graph.

We will not raise exception when the user tries to get in_neighbors of an undirected graph. She should be aware of this.

Graph type should be given by g = Graph(type=DIRECTED_GRAPH)



an example graph dot file

digraph G {
layout=dot;
splines=true;
0 [color=black, demand=-5, label=0];
1 [color=black, demand=10, label=1];
0 -> 1  [color=black, flow=0, cost=38, capacity=11, label="0/11/38"];
2 [color=black, demand=-8, label=2];
0 -> 2  [color=black, flow=0, cost=38, capacity=10, label="0/10/38"];
1 -> 2  [color=blue, flow=8, cost=35, capacity=15, label="8/15/35"];
3 [color=black, demand=-5, label=3];
1 -> 3  [color=blue, flow=10, cost=34, capacity=11, label="10/11/34"];
5 [color=black, demand=0, label=5];
2 -> 5  [color=black, flow=0, cost=43, capacity=13, label="0/13/43"];
3 -> 5  [color=blue, flow=5, cost=44, capacity=16, label="5/16/44"];
4 [color=black, demand=8, label=4];
4 -> 1  [color=blue, flow=8, cost=31, capacity=15, label="8/15/31"];
5 -> 0  [color=blue, flow=5, cost=42, capacity=19, label="5/19/42"];
}


TODO(aykut):
-> when we look for an attr and it does not exist we return None for Node class
get_attr() method. Should we change this?

'''

class Tree(Graph):
    def __init__(self, **attrs):
        attrs['type'] = DIRECTED_GRAPH
        if 'layout' not in attrs:
            attrs['layout'] = 'dot'
        Graph.__init__(self, **attrs)
        self.root = None

    def get_children(self, n):
        return self.get_neighbors(n)

    def get_parent(self, n):
        return self.get_node_attr(n, 'parent')

    def add_root(self, root, **attrs):
        attrs['level'] = 0
        self.add_node(root, **attrs)
        self.root = root

    def add_child(self, n, parent, **attrs):
        attrs['level'] = self.get_node_attr(parent, 'level') + 1
        attrs['parent'] = parent
        self.add_node(n, **attrs)
        self.add_edge(parent, n)

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
