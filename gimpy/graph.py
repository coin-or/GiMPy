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

from global_constants import *
from list import Stack
from list import Queue
from list import PriorityQueue
import subprocess # for call()
import StringIO   # for StringIO()
import copy       # for deepcopy()
import sys        # for exit()
import random     # for seed, random, randint
import tempfile   # for mkstemp()
import os         # for close()
import operator   # for itemgetter()

try:
    import pygame # for locals.QUIT, locals.KEYDOWN,display,image,event,init
except ImportError:
    PYGAME_INSTALLED = False
    print 'Pygame not installed'
else:
    PYGAME_INSTALLED = True
    print 'Found pygame installation'

try:
    import dot2tex # for dot2tex method
except ImportError:
    DOT2TEX_INSTALLED = False
    print 'dot2tex not installed'
else:
    DOT2TEX_INSTALLED = True
    print 'Found dot2tex'

try:
    from PIL import Image as PIL_Image
except ImportError:
    PIL_INSTALLED = False
    print 'Python Image Library not installed'
else:
    PIL_INSTALLED = True
    print 'Found Python Image Library'

try:
    import pygtk
    import gtk
    import xdot
except ImportError:
    XDOT_INSTALLED = False
    print 'Xdot not installed'
else:
    XDOT_INSTALLED = True
    print 'Found xdot installation'

try:
    import lxml # for etree
except ImportError:
    ETREE_INSTALLED = False
    print 'Etree could not be imported from lxml'
else:
    ETREE_INSTALLED = True
    print 'Found etree in lxml'

FlexList = list

class Node(object):
    '''
    '''
    def __init__(self, name, **attr):
        self.name = name
        self.attr = copy.deepcopy(DEFAULT_NODE_ATTRIBUTES)
        for a in attr:
            self.attr[a] = attr[a]

    def get_attr(self, attr):
        if attr in self.attr:
            return self.attr[attr]
        else:
            return None

    def set_attr(self, attr, value):
        self.attr[attr] = value

    def to_string(self):
        '''
        return string representation of node in dot language.
        '''
        node = list()
        node.append(str(self.name))
        node.append(' [')
        flag = False
        for a in self.attr:
            flag = True
            node.append(a)
            node.append('=')
            node.append(quote_if_necessary(str(self.attr[a])))
            node.append(', ')
        if flag is True:
            node = node[:-1]
        node.append(']')
        return ''.join(node)


class Graph(object):
    '''
    Graph class. Felxible enough to let any standart graph implementation,
    adjecency list, incidence list, adjecency matrix, incidence matrix, etc.
    Currently we only have adjacency list.
    '''
    def __init__(self, **attr):
        # graph attributes
        self.attr = copy.deepcopy(DEFAULT_GRAPH_ATTRIBUTES)
        # set attributes using constructor
        for a in attr:
            self.attr[a] = attr[a]
        # set name
        if 'name' in self.attr:
            self.name = self.attr['name']
        else:
            self.name = 'G'
        # edge attributes
        self.edge_attr = dict()
        # we treat type attribute and keep it in a separate class attribute
        if 'type' in self.attr:
            self.graph_type = self.attr['type']
        else:
            self.graph_type = UNDIRECTED_GRAPH
        # adjacency list of nodes, it is a dictionary of lists
        self.neighbors = {}
        # if the graph is undirected we do not need in_neighbor
        if self.graph_type is DIRECTED_GRAPH:
            self.in_neighbors = {}
        self.nodes = {}
        self.edge_connect_symbol = EDGE_CONNECT_SYMBOL[self.graph_type]
        self.out_neighbors = self.neighbors
        if 'display' in self.attr and self.attr['display']=='pygame':
            if PYGAME_INSTALLED:
                pygame.init()
            else:
                print "Pygame module not installed, graphical display disabled"
        elif 'display' not in self.attr:
            self.attr['display']='off'
        if 'layout' not in self.attr:
            self.attr['layout'] = 'dot'

    def __repr__(self):
        data = str()
        for n in self.nodes:
            data += str(n)
            data += ' -> '
            data += self.neighbors[n].__repr__()
            data += '\n'
        data = data[:-1]
        return data

    def add_node(self, name, **attr):
        if name in self.neighbors:
            raise MultipleNodeException
        self.neighbors[name] = FlexList()
        if self.graph_type is DIRECTED_GRAPH:
            self.in_neighbors[name] = FlexList()
        self.nodes[name] = Node(name, **attr)

    def del_node(self, name):
        if name not in self.neighbors:
            raise Exception('Node %s does not exist!' %str(name))
        del self.neighbors[name]
        del self.nodes[name]
        el = self.get_edge_list()
        for e in el:
            if e[0] is name or e[1] is name:
                del self.edge_attr[e]

    def add_edge(self, name1, name2, **attr):
        if (name1, name2) in self.edge_attr:
            raise MultipleEdgeException
        if self.graph_type is UNDIRECTED_GRAPH and (name2,name1) in self.edge_attr:
            raise MultipleEdgeException
        self.edge_attr[(name1,name2)] = copy.deepcopy(DEFAULT_EDGE_ATTRIBUTES)
        for a in attr:
            self.edge_attr[(name1,name2)][a] = attr[a]
        if name1 not in self.nodes:
            self.add_node(name1)
        if name2 not in self.nodes:
            self.add_node(name2)
        self.neighbors[name1].append(name2)
        if self.graph_type is UNDIRECTED_GRAPH:
            self.neighbors[name2].append(name1)
        else:
            self.in_neighbors[name2].append(name1)

    def del_edge(self, e):
        if self.graph_type is DIRECTED_GRAPH:
            try:
                del self.edge_attr[e]
            except KeyError:
                raise Exception('Edge %s does not exists!' %str(e))
            self.neighbors[e[0]].remove(e[1])
            self.in_neighbors[e[1]].remove(e[0])
        else:
            try:
                del self.edge_attr[e]
            except KeyError:
                try:
                    del self.edge_attr[(e[1],e[0])]
                except KeyError:
                    raise Exception('Edge %s does not exists!' %str(e))
            self.neighbors[e[0]].remove(e[1])
            self.neighbors[e[1]].remove(e[0])


    def get_node(self, name):
        '''
        Return none if node does not exist.
        '''
        if name in self.nodes:
            return self.nodes[name]
        else:
            return None

    def get_edge_cost(self, edge):
       '''
       Returns cost attr of edge, required for minimum_spanning_tree_kruskal().
       '''
       return self.get_edge_attr(edge[0], edge[1], 'cost')

    def check_edge(self, name1, name2):
        '''
        Return True if edge exists, false otherwise.
        '''
        if self.graph_type is DIRECTED_GRAPH:
            return (name1, name2) in self.edge_attr
        else:
            return ((name1, name2) in self.edge_attr or
                    (name2, name1) in self.edge_attr)

    def get_node_list(self):
        return self.neighbors.keys()

    def get_edge_list(self):
        return self.edge_attr.keys()

    def get_node_num(self):
        return len(self.neighbors)

    def get_edge_num(self):
        return len(self.edge_attr)

    def get_node_attr(self, name, attr):
        '''
        Returns attribute attr of node name.
        '''
        return self.get_node(name).get_attr(attr)

    def get_edge_attr(self, n, m, attr):
        '''
        Returns attribute attr of edge (n,m).
        '''
        if self.graph_type is DIRECTED_GRAPH:
            return self.edge_attr[(n,m)][attr]
        else:
            try:
                return self.edge_attr[(n,m)][attr]
            except KeyError:
                return self.edge_attr[(m,n)][attr]

    def set_node_attr(self, name, attr, value):
        '''
        Sets attr attribute of node named name to value.
        '''
        self.get_node(name).set_attr(attr, value)

    def set_edge_attr(self, n, m, attr, value):
        '''
        Sets attr attribute of edge (n,m) to value.
        '''
        if self.graph_type is DIRECTED_GRAPH:
            self.edge_attr[(n,m)][attr] = value
        else:
            try:
                self.edge_attr[(n,m)][attr] = value
            except KeyError:
                self.edge_attr[(m,n)][attr] = value

    def get_neighbors(self, name):
        return self.neighbors[name]

    def get_in_neighbors(self, name):
        return self.in_neighbors[name]

    def get_out_neighbors(self, name):
        return self.neighbors[name]

    def get_parent_graph(self):
        '''
        this method may be implemented, it is used by to_string()
        '''
        pass

    def edge_to_string(self, e):
        '''
        return string that represents edge e in dot language.
        '''
        edge = list()
        edge.append(str(e[0]))
        edge.append(self.edge_connect_symbol)
        edge.append(str(e[1]))
        # return if there is nothing in self.edge_attr[e]
        if len(self.edge_attr[e]) is 0:
            return ''.join(edge)
        edge.append('  [')
        for a in self.edge_attr[e]:
            edge.append(a)
            edge.append('=')
            edge.append(quote_if_necessary(str(self.edge_attr[e][a])))
            edge.append(', ')
        edge = edge[:-1]
        edge.append(']')
        return ''.join(edge)

    def to_string(self):
        """
        This method is based on pydot Graph class with the same name.
        Returns a string representation of the graph in dot language.
        It will return the graph and all its subelements in string form.
        """
        graph = list()
        graph.append('%s %s {\n' %(self.graph_type, self.name))
        for a in self.attr:
            if a not in GRAPH_ATTRIBUTES:
                continue
            val = self.attr[a]
            if val is not None:
                graph.append( '%s=%s' % (a, quote_if_necessary(val)) )
            else:
                graph.append(a)
            graph.append( ';\n' )
        # process nodes
        for n in self.neighbors:
            data = self.get_node(n).to_string()
            graph.append(data + ';\n')
        # process edges
        for e in self.edge_attr:
            data = self.edge_to_string(e)
            graph.append(data + ';\n')
        graph.append( '}\n' )
        return ''.join(graph)

    def label_components(self, display = None):
        '''
        This method labels the nodes of an undirected graph with component
        numbers so that each node has the same label as all nodes in the
        same component
        '''
        if self.graph_type == DIRECTED_GRAPH:
            raise Exception("label_components only works for ",
                            "undirected graphs")
        self.num_components = 0
        for n in self.get_node_list():
            self.get_node(n).set_attr('component', None)
        for n in self.get_node_list():
            if self.get_node(n).get_attr('component') == None:
                self.dfs(n, component = self.num_components)
                self.num_components += 1

    def label_strong_component(self, root, disc_count = 0, finish_count = 1,
                               component = None):
        '''
        This method labels the nodes of a directed graph with component
        numbers so that each node has the same label as all nodes in the
        same component
        '''
        if self.graph_type == UNDIRECTED_GRAPH:
            raise Exception("label_strong_componentsis only for ",
                            "directed graphs")
        if self.num_components != None:
            return
        self.num_components = 0
        for n in self.get_node_list():
            self.get_node(n).set_attr('component', None)
        for n in self.get_node_list():
            if self.get_node(n).get_attr('disc_time') == None:
                self.dfs(n, component = self.num_components)
        self.num_components = 0
        for n in self.get_node_list():
            self.set_node(n).set_attr('component', None)
        for n in self.get_node_list():
            if self.get_node(n).get_attr('component') == None:
                self.dfs(n, component = self.num_components, transpose = True)
                self.num_components += 1

    def dfs(self, root, disc_count = 0, finish_count = 1, component = None,
            transpose = False):
        neighbors = self.neighbors
        if self.graph_type == DIRECTED_GRAPH and transpose:
            neighbors = self.in_neighbors
        self.get_node(root).set_attr('component', component)
        disc_count += 1
        self.get_node(root).set_attr('disc_time', disc_count)
        if transpose:
            fTime = []
            for n in neighbors[root]:
                fTime.append((n,self.get_node(n).get_attr('finish_time')))
            neighbor_list = sorted(fTime, key=operator.itemgetter(1))
            neighbor_list = list(t[0] for t in neighbor_list)
            neighbor_list.reverse()
        else:
            neighbor_list = neighbors[root]
        for i in neighbor_list:
            if not transpose:
                if self.get_node(i).get_attr('disc_time') is None:
                    disc_count, finish_count = self.dfs(i, disc_count,
                                                        finish_count,
                                                        component, transpose)
            else:
                if self.get_node(i).get_attr('component') is None:
                    disc_count, finish_count = self.dfs(i, disc_count,
                                                        finish_count,
                                                        component, transpose)
        finish_count += 1
        self.get_node(root).set_attr('finish_time', finish_count)
        return disc_count, finish_count

    def bfs(self, root, display = None, component = None):
        self.search(root, display = display, component = component, q = Queue())

    def search(self, source, destination = None, display = None,
               component = None, q = Stack(),
               algo = 'DFS', reverse = False, **kargs):
        '''
        if destination is not specified:
           This method determines all nodes reachable from "source" ie. creates
           precedence tree and returns it (dictionary).
        if destionation is given:
           If there exists a path from "source" to "destination" it will return
           list of the nodes is this path. If there is no such path, it will
           return the precedence tree constructed from source (dictionary).
        Optionally, it marks all nodes reachable from "source" with a component
        number. The variable "q" determines the order in which the nodes are searched.
        '''
        if display == None:
            display = self.attr['display']
        else:
            self.set_display_mode(display)
        if algo == 'DFS':
            q = Stack()
        elif algo == 'BFS' or algo == "UnweightedSPT":
            q = Queue()
        elif algo == 'Dijkstra':
            q = PriorityQueue()
            for n in self.neighbors:
                self.get_node(n).set_attr('label', '-')
            self.display()
        elif algo == 'Prim':
            q = PriorityQueue()
            for n in self.neighbors:
                self.get_node(n).set_attr('label', '-')
            self.display()
        neighbors = self.neighbors
        if self.graph_type == DIRECTED_GRAPH and reverse:
            neighbors = self.in_neighbors
        for i in self.get_node_list():
            self.get_node(i).set_attr('color', 'black')
            for j in neighbors[i]:
                if reverse:
                    self.set_edge_attr(j, i, 'color', 'black')
                else:
                    self.set_edge_attr(i, j, 'color', 'black')
        pred = {}
        self.process_edge_search(None, source, pred, q, component, algo,
                                 **kargs)
        found = True
        if source != destination:
            found = False
        while not q.isEmpty() and not found:
            current = q.peek()
            self.process_node_search(current, q, **kargs)
            self.get_node(current).set_attr('color', 'blue')
            if current != source:
                if reverse:
                    self.set_edge_attr(current, pred[current], 'color', 'green')
                else:
                    self.set_edge_attr(pred[current], current, 'color', 'green')
            if current == destination:
                found = True
                break
            self.display()
            for n in neighbors[current]:
                if self.get_node(n).get_attr('color') != 'green':
                    if reverse:
                        self.set_edge_attr(n, current, 'color', 'yellow')
                    else:
                        self.set_edge_attr(current, n, 'color', 'yellow')
                    self.display()
                    self.process_edge_search(current, n, pred, q, component,
                                             algo, **kargs)
                    if reverse:
                        self.set_edge_attr(n, current, 'color', 'black')
                    else:
                        self.set_edge_attr(current, n, 'color', 'black')
            q.remove(current)
            self.get_node(current).set_attr('color', 'green')
            self.display()
        if found:
            path = [destination]
            current = destination
            while current != source:
                path.insert(0, pred[current])
                current = pred[current]
            #calculate distance lines
            #distance = 0
            #for i in range(len(path)-1):
            #    distance += self.edge_attr[(path[i],path[i+1])]['cost']
            #return distance
            #end of calculate distance lines
            return path
        return pred

    def process_node_search(self, node, q, **kwargs):
        if isinstance(q, PriorityQueue):
            self.get_node(node).set_attr('priority', q.get_priority(node))

    def process_edge_dijkstra(self, current, neighbor, pred, q, component):
        if current is None:
            self.get_node(neighbor).set_attr('color', 'red')
            self.get_node(neighbor).set_attr('label', 0)
            q.push(neighbor, 0)
            self.display()
            self.get_node(neighbor).set_attr('color', 'black')
            return
        new_estimate = (q.get_priority(current) +
                        self.get_edge_attr(current, neighbor, 'cost'))
        if neighbor not in pred or new_estimate < q.get_priority(neighbor):
            pred[neighbor] = current
            self.get_node(neighbor).set_attr('color', 'red')
            self.get_node(neighbor).set_attr('label', new_estimate)
            q.push(neighbor, new_estimate)
            self.display()
            self.get_node(neighbor).set_attr('color', 'black')

    def process_edge_prim(self, current, neighbor, pred, q, component):
        if current is None:
            self.get_node(neighbor).set_attr('color', 'red')
            self.get_node(neighbor).set_attr('label', 0)
            q.push(neighbor, 0)
            self.display()
            self.get_node(neighbor).set_attr('color', 'black')
            return
        new_estimate = self.get_edge_attr(current, neighbor, 'cost')
        if not neighbor in pred or new_estimate < q.get_priority(neighbor):
            pred[neighbor] = current
            self.get_node(neighbor).set_attr('color', 'red')
            self.get_node(neighbor).set_attr('label', new_estimate)
            q.push(neighbor, new_estimate)
            self.display()
            self.get_node(neighbor).set_attr('color', 'black')

    def process_edge_search(self, current, neighbor, pred, q, component, algo,
                            **kargs):
        if algo == 'Dijkstra':
            return self.process_edge_dijkstra(current, neighbor, pred, q,
                                              component)
        if algo == 'Prim':
            return self.process_edge_prim(current, neighbor, pred, q,
                                          component)
        if algo == 'UnweightedSPT':
            if current == None:
                self.get_node(neighbor).set_attr('distance', 0)
            else:
                self.get_node(neighbor).set_attr('distance',
                                   self.get_node(current).get_attr('distance') + 1)
        if current == None:
            q.push(neighbor)
            return
        if not neighbor in pred:
            pred[neighbor] = current
            self.get_node(neighbor).set_attr('color', 'red')
            self.display()
            if component != None:
                self.get_node(neighbor).set_attr('component', component)
                self.get_node(neighbor).set_attr('label', component)
            self.get_node(neighbor).set_attr('color', 'black')
            self.display()
            q.push(neighbor)

    def minimum_spanning_tree_prim(self, source, display = None,
                                   q = PriorityQueue()):
        '''
        This method determines a minimum spanning tree of all nodes reachable
        from "source" using Prim's Algorithm
        '''
        if display == None:
            display = self.attr['display']
        else:
            self.set_display_mode(display)
        if isinstance(q, PriorityQueue):
            addToQ = q.push
            removeFromQ = q.pop
            peek = q.peek
            isEmpty = q.isEmpty
        neighbors = self.get_neighbors
        pred = {}
        addToQ(source)
        done = False
        while not isEmpty() and not done:
            current = removeFromQ()
            self.set_node_attr(current, 'color', 'blue')
            if current != source:
                self.set_edge_attr(pred[current], current, 'color', 'green')
            self.display()
            for n in neighbors(current):
                if self.get_node_attr(n, 'color') != 'green':
                    self.set_edge_attr(current, n, 'color', 'yellow')
                    self.display()
                    new_estimate = self.get_edge_attr(current, n, 'cost')
                    if not n in pred or new_estimate < peek(n)[0]:
                        pred[n] = current
                        self.set_node_attr(n, 'color', 'red')
                        self.set_node_attr(n, 'label', new_estimate)
                        addToQ(n, new_estimate)
                        self.display()
                        self.set_node_attr(n, 'color', 'black')
                    self.set_edge_attr(current, n, 'color', 'black')
            self.set_node_attr(current, 'color', 'green')
            self.display()
        return pred

    def minimum_spanning_tree_kruskal(self, display = None, components = None):
        '''
        This method determines a minimum spanning tree using Kruskal's Algorithm
        '''
        if display == None:
            display = self.attr['display']
        else:
            self.set_display_mode(display)
        if components is None:
            components = DisjointSet(display = display, layout = 'dot',
                                     optimize = True)
        sorted_edge_list = sorted(self.get_edge_list(), key=self.get_edge_cost)
        edges = []
        for n in self.get_node_list():
            components.add([n])
        components.display()
        for e in sorted_edge_list:
            if len(edges) == len(self.get_node_list()) - 1:
                break
            self.set_edge_attr(e[0], e[1], 'color', 'yellow')
            self.display()
            if components.union(e[0], e[1]):
                self.set_edge_attr(e[0], e[1], 'color', 'green')
                self.display()
                edges.append(e)
            else:
                self.set_edge_attr(e[0], e[1], 'color', 'black')
                self.display()
            components.display()
        return edges

    def max_flow_preflowpush(self, source, sink, algo = 'FIFO', display = None):
        '''
        API: max_flow(self, source, sink, display=None)
        Finds maximum flow from source to sink by a depth-first search based
        augmenting path algorithm.

        pre: Assumes a directed graph in which each arc has a 'capacity'
        attribute and for which there does does not exist both arcs (i, j) and
        (j, i) for any pair of nodes i and j.
        inputs:
            source: source node, integer or string
            sink: sink node, integer or string
            display:

        post: The 'flow' attribute of each arc gives a maximum flow.
        '''
        if display == None:
            display = self.attr['display']
        else:
            self.set_display_mode(display)
        nl = self.get_node_list()
        # set excess of all nodes to 0
        for n in nl:
            self.set_node_attr(n, 'excess', 0)
        # set flow of all edges to 0
        for e in self.edge_attr:
           self.edge_attr[e]['flow'] = 0
           self.edge_attr[e]['label'] = str(self.edge_attr[e]['capacity'])+'/0'
        self.display()
        self.set_display_mode('off')
        self.search(sink, algo = 'UnweightedSPT', reverse = True)
        self.set_display_mode(display)
        disconnect = False
        for n in nl:
            if self.get_node_attr(n, 'distance') is None:
                disconnect = True
                self.set_node_attr(n, 'distance',
                                   2*len(nl) + 1)
        if disconnect:
            print 'Warning: graph contains nodes not connected to the sink...'
        if algo == 'FIFO':
            q = Queue()
        elif algo == 'SAP':
            q = Stack()
        elif algo == 'HighestLabel':
            q = PriorityQueue()
        for n in self.get_neighbors(source):
            capacity = self.get_edge_attr(source, n, 'capacity')
            self.set_edge_attr(source, n, 'flow', capacity)
            self.set_node_attr(n, 'excess', capacity)
            excess = self.get_node_attr(source, 'excess')
            self.set_node_attr(source, 'excess', excess - capacity)
            if algo == 'FIFO' or algo == 'SAP':
                q.push(n)
            elif algo == 'HighestLabel':
                q.push(n, -1)
        self.set_node_attr(source, 'distance', len(nl))
        self.show_flow()
        while not q.isEmpty():
            relabel = True
            current = q.peek()
            neighbors = (self.get_neighbors(current) +
                         self.get_in_neighbors(current))
            for n in neighbors:
                pushed = self.process_edge_flow(source, sink, current, n, algo,
                                                q)
                if pushed:
                    self.show_flow()
                    if algo == 'FIFO':
                        '''With FIFO, we need to add the neighbors to the queue
                        before the current is added back in or the nodes will
                        be out of order
                        '''
                        if q.peek(n) is None and n != source and n != sink:
                            q.push(n)
                        '''Keep pushing while there is excess'''
                        if self.get_node_attr(current, 'excess') > 0:
                            continue
                    '''If we were able to push, then there we should not
                    relabel
                    '''
                    relabel = False
                    break
            q.remove(current)
            if current != sink:
                if relabel:
                    self.relabel(current)
                    self.show_flow()
                if self.get_node_attr(current, 'excess') > 0:
                    if algo == 'FIFO' or algo == 'SAP':
                        q.push(current)
                    elif algo == 'HighestLabel':
                        q.push(current, -self.get_node_attr(current,
                                                            'distance'))
            if pushed and q.peek(n) is None and n != source:
                if algo == 'SAP':
                    q.push(n)
                elif algo == 'HighestLabel':
                    q.push(n, -self.get_node_attr(n, 'distance'))
        return

    def process_edge_flow(self, source, sink, i, j, algo, q):
        if (self.get_node_attr(i, 'distance') !=
            self.get_node_attr(j, 'distance') + 1):
            return False
        if (i, j) in self.edge_attr:
            edge = (i, j)
            capacity = self.get_edge_attr(i, j, 'capacity')
            mult = 1
        else:
            edge = (j, i)
            capacity = 0
            mult = -1
        flow = mult*self.edge_attr[edge]['flow']
        residual_capacity = capacity - flow
        if residual_capacity == 0:
            return False
        excess_i = self.get_node_attr(i, 'excess')
        excess_j = self.get_node_attr(j, 'excess')
        push_amount = min(excess_i, residual_capacity)
        self.edge_attr[edge]['flow'] = mult*(flow + push_amount)
        self.set_node_attr(i, 'excess', excess_i - push_amount)
        self.set_node_attr(j, 'excess', excess_j + push_amount)
        return True

    def relabel(self, i):
        min_distance = 2*len(self.get_node_list()) + 1
        for j in self.get_neighbors(i):
            if (self.get_node_attr(j, 'distance') < min_distance and
                (self.get_edge_attr(i, j, 'flow') <
                 self.get_edge_attr(i, j, 'capacity'))):
                min_distance = self.get_node_attr(j, 'distance')
        for j in self.get_in_neighbors(i):
            if (self.get_node_attr(j, 'distance') < min_distance and
                self.get_edge_attr(j, i, 'flow') > 0):
                min_distance = self.get_node_attr(j, 'distance')
        self.set_node_attr(i, 'distance', min_distance + 1)

    def show_flow(self):
        for n in self.get_node_list():
            excess = self.get_node_attr(n, 'excess')
            distance = self.get_node_attr(n, 'distance')
            self.set_node_attr(n, 'label', str(excess)+'/'+str(distance))
            for neighbor in self.get_neighbors(n):
                capacity = self.get_edge_attr(n, neighbor, 'capacity')
                flow = self.get_edge_attr(n, neighbor, 'flow')
                self.set_edge_attr(n, neighbor, 'label',
                                   str(capacity)+'/'+str(flow))
                if capacity == flow:
                    self.set_edge_attr(n, neighbor, 'color', 'red')
                elif flow > 0:
                    self.set_edge_attr(n, neighbor, 'color', 'green')
                else:
                    self.set_edge_attr(n, neighbor, 'color', 'black')
        self.display()

    def create_residual_graph(self):
        '''
        API:
            create_residual_graph(self)
        Description:
            Creates and returns residual graph, which is a Graph instance
            itself.
        Pre:
            (1) Arcs should have 'flow', 'capacity' and 'cost' attribute
            TODO(aykut): this can be generalized by skipping 'cost' when it is
            not relevant.
            (2) Graph should be a directed graph
        Return:
            returns residual graph, which is a Graph instance.
        '''
        if self.graph_type is UNDIRECTED_GRAPH:
            raise Exception('residual graph is defined for directed graphs.')
        residual_g = Graph(type = DIRECTED_GRAPH)
        for e in self.get_edge_list():
            capacity_e = self.get_edge_attr(e[0], e[1], 'capacity')
            flow_e = self.get_edge_attr(e[0], e[1], 'flow')
            cost_e = self.get_edge_attr(e[0], e[1], 'cost')
            if flow_e > 0:
                residual_g.add_edge(e[1], e[0], cost=-1*cost_e,
                                    capacity=flow_e)
            if capacity_e - flow_e > 0:
                residual_g.add_edge(e[0], e[1], cost=cost_e,
                                    capacity=capacity_e-flow_e)
        return residual_g

    def cycle_canceling(self, display):
        '''
        API:
            cycle_canceling(self)
        Description:
            Solves minimum cost feasible flow problem using cycle canceling
            algorithm. Returns True when an optimal solution is found, returns
            False otherwise. 'flow' attribute values of arcs should be
            considered as junk when returned False.
        Pre:
            (1) Arcs should have 'capacity' and 'cost' attribute.
            (2) Nodes should have 'demand' attribute, this value should be
            positive if the node is a supply node, negative if it is demand
            node and 0 if it is transhipment node.
            (3) graph should not have node 's' and 't'.
        Post:
            Changes 'flow' attributes of arcs.
        Return:
            Returns True when an optimal solution is found, returns False
            otherwise.
        '''
        # find a feasible solution to flow problem
        if not self.find_feasible_flow():
            return False
        # create residual graph
        residual_g = self.create_residual_graph()
        # identify a negative cycle in residual graph
        ncycle = residual_g.get_negative_cycle()
        # loop while residual graph has a negative cycle
        while ncycle is not None:
            # find capacity of cycle
            cap = residual_g.find_cycle_capacity(ncycle)
            # augment capacity amount along the cycle
            self.augment_cycle(cap, ncycle)
            # create residual graph
            residual_g = self.create_residual_graph()
            # identify next negative cycle
            ncycle = residual_g.get_negative_cycle()
        return True

    def find_feasible_flow(self):
        '''
        API:
            find_feasible_flow(self)
        Description:
            Solves feasible flow problem, stores solution in 'flow' attribute
            or arcs. This method is used to get an initial feasible flow for
            simplex and cycle canceling algorithms. Uses max_flow() method.
            Other max flow methods can also be used. Returns True if a feasible
            flow is found, returns False, if the problem is infeasible. When
            the problem is infeasible 'flow' attributes of arcs should be
            considered as junk.
        Pre:
            (1) 'capacity' attribute of arcs
            (2) 'demand' attribute of nodes
        Post:
            Keeps solution in 'flow' attribute of arcs.
        Return:
            Returns True if a feasible flow is found, returns False, if the
            problem is infeasible
        '''
        # establish a feasible flow in the network, to do this add nodes s and
        # t and solve a max flow problem.
        nl = self.get_node_list()
        for i in nl:
            b_i = self.get_node(i).get_attr('demand')
            if b_i > 0:
                # i is a supply node, add (s,i) arc
                self.add_edge('s', i, capacity=b_i)
            elif b_i < 0:
                # i is a demand node, add (i,t) arc
                self.add_edge(i, 't', capacity=-1*b_i)
        # solve max flow on this modified graph
        self.max_flow('s', 't')
        # check if all demand is satisfied, i.e. the min cost problem is
        # feasible or not
        for i in self.neighbors['s']:
            flow = self.get_edge_attr('s', i, 'flow')
            capacity = self.get_edge_attr('s', i, 'capacity')
            if flow != capacity:
                self.del_node('s')
                self.del_node('t')
                return False
        # remove node 's' and node 't'
        self.del_node('s')
        self.del_node('t')
        return True

    def get_layout(self):
        return self.attr['layout']

    def set_layout(self, value):
        self.attr['layout']=value

    def write(self, basename, layout, format='png'):
        f = file(basename, "w+b")
        if format == 'dot':
            f.write(self.to_string())
        else:
            f.write(self.create(layout, format))
        f.close()

    def create(self, layout, format, **args):
        '''
        TODO(aykut)
        Returns postscript representation of self.
        layout specifies the executable to be used.
        im = StringIO.StringIO(self.create(self.get_layout(), format))
        return image representing string in specified format. Do this by
        calling graphviz executable. (piping)
        We don not have support for shape files.
        '''
        #p = subprocess.Popen([layout, '-T'+format],
        #                     stdin=subprocess.PIPE,
        #                     stdout=subprocess.PIPE,
        #                     stderr=subprocess.PIPE)
        tmp_fd, tmp_name = tempfile.mkstemp()
        tmp_file = os.fdopen(tmp_fd, 'w')
        tmp_file.write(self.to_string())
        # ne need for os.close(tmp_fd), since we have tmp_file.close(tmp_file)
        tmp_file.close()
        tmp_dir = os.path.dirname(tmp_name)
        p = subprocess.Popen([layout, '-T'+format, tmp_name],
                             cwd=tmp_dir,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout_output, stderr_output = p.communicate()
        if p.returncode != 0 :
            raise Exception('Graphviz executable terminated with status: %d. stderr follows: %s' % (
                    p.returncode, stderr_output))
        elif stderr_output:
            print stderr_output
        return stdout_output

    def display(self, highlight = None, basename = 'graph', format = 'png',
                pause = True):
        '''
        TODO(aykut):
        current display modes: off, file, pygame, PIL, xdot, svg
        current layout modes: layouts provided by graphviz, dot2tex, bak
        current formats: formats provided by graphviz (ps pdf png )
        problems:
            layout bak is not supported.
            display mode svg is not supported.

        '''
        if self.attr['display'] == 'off':
            return
        if highlight != None:
            for n in highlight:
                if not isinstance(n, Node):
                    m = self.get_node(n)
                m.set_attr('color', 'red')
        if self.attr['display'] == 'file':
            if self.get_layout() == 'dot2tex':
                if DOT2TEX_INSTALLED:
                    if format != 'pdf' or format != 'ps':
                        print "Dot2tex only supports pdf and ps formats, falling back to pdf"
                        format = 'pdf'
                    #self.set_layout('dot')
                    tex = dot2tex.dot2tex(self.to_string(), autosize=True, texmode = 'math', template = DOT2TEX_TEMPLATE)
                    f = open(basename+'.tex', 'w')
                    f.write(tex)
                    f.close()
                    subprocess.call(['latex', basename])
                    if format == 'ps':
                        subprocess.call(['dvips', basename])
                    elif format == 'pdf':
                        subprocess.call(['pdflatex', basename])
                    #self.set_layout('dot2tex')
                else:
                    print "Dot2tex not installed, falling back to graphviz"
                    self.set_layout('dot')
                    self.write(basename+'.'+format, self.get_layout(), format)
            elif self.get_layout() == 'bak':
                im = StringIO.StringIO(self.GenerateTreeImage())
            else:
                self.write(basename+'.'+format, self.get_layout(), format)
            return
        elif self.attr['display'] == 'pygame':
            im = StringIO.StringIO(self.create(self.get_layout(), format))
            picture = pygame.image.load(im, format)
            screen = pygame.display.set_mode(picture.get_size())
            screen.blit(picture, picture.get_rect())
            pygame.display.flip()
            while pause:
                e = pygame.event.poll()
                if e.type == pygame.KEYDOWN:
                    break
                if e.type == pygame.QUIT:
                    sys.exit()
        elif self.attr['display'] == 'PIL':
            im = StringIO.StringIO(self.create(self.get_layout(), format))
            if PIL_INSTALLED:
                im2 = PIL_Image.open(im)
                im2.show()
            else:
                print 'Error: PIL not installed. Display disabled.'
                self.attr['display'] = 'off'
        elif self.attr['display'] == 'xdot':
            if XDOT_INSTALLED:
                window = xdot.DotWindow()
                window.set_dotcode(self.to_string())
                window.connect('destroy', gtk.main_quit())
                gtk.main()
            else:
                print 'Error: xdot not installed. Display disabled.'
                self.attr['display'] = 'off'
        elif self.attr['display'] == 'svg':
            if not ETREE_INSTALLED:
                print 'Error: etree not installed (display mode: svg). Display disabled.'
                self.attr['display'] = 'off'
        else:
            print "Unknown display mode: ",
            print self.attr['display']
        if highlight != None:
            for n in highlight:
                if not isinstance(n, Node):
                    m = self.get_node(n)
                m.set_attr('color', 'black')

    def set_display_mode(self, value):
        self.attr['display'] = value

    def max_flow(self, source, sink, display=None):
        '''
        API: max_flow(self, source, sink, display=None)
        Finds maximum flow from source to sink by a depth-first search based
        augmenting path algorithm.

        pre: Assumes a directed graph in which each arc has a 'capacity'
        attribute and for which there does does not exist both arcs (i, j)
        and (j, i) for any pair of nodes i and j.
        inputs:
            source: source node, integer or string
            sink: sink node, integer or string
            display:

        post: The 'flow" attribute of each arc gives a maximum flow.
        '''
        nl = self.get_node_list()
        # set flow of all edges to 0
        for e in self.edge_attr:
            self.edge_attr[e]['flow'] = 0
            capacity = self.edge_attr[e]['capacity']
            self.edge_attr[e]['label'] = str(capacity)+'/0'
        while True:
            # find an augmenting path from source to sink using DFS
            dfs_stack = []
            dfs_stack.append(source)
            pred = {source:None}
            explored = [source]
            for n in nl:
                self.get_node(n).set_attr('color', 'black')
            for e in self.edge_attr:
                if self.edge_attr[e]['flow'] == 0:
                    self.edge_attr[e]['color'] = 'black'
                elif self.edge_attr[e]['flow']==self.edge_attr[e]['capacity']:
                    self.edge_attr[e]['color'] = 'red'
                else:
                    self.edge_attr[e]['color'] = 'green'
            self.display()
            while dfs_stack:
                current = dfs_stack.pop()
                if current == sink:
                    break
                out_neighbor = self.neighbors[current]
                in_neighbor = self.in_neighbors[current]
                neighbor = out_neighbor+in_neighbor
                for m in neighbor:
                    if m in explored:
                        continue
                    self.get_node(m).set_attr('color', 'yellow')
                    if m in out_neighbor:
                        self.set_edge_attr(current, m, 'color', 'yellow')
                        available_capacity = (
                            self.get_edge_attr(current, m, 'capacity')-
                            self.get_edge_attr(current, m, 'flow'))
                    else:
                        self.set_edge_attr(m, current, 'color', 'yellow')
                        available_capacity=self.get_edge_attr(m, current, 'flow')
                    self.display()
                    if available_capacity > 0:
                        self.get_node(m).set_attr('color', 'blue')
                        if m in out_neighbor:
                            self.set_edge_attr(current, m, 'color', 'blue')
                        else:
                            self.set_edge_attr(m, current, 'color', 'blue')
                        explored.append(m)
                        pred[m] = current
                        dfs_stack.append(m)
                    else:
                        self.get_node(m).set_attr('color', 'black')
                        if m in out_neighbor:
                            if (self.get_edge_attr(current, m, 'flow') ==
                                self.get_edge_attr(current, m, 'capacity')):
                                self.set_edge_attr(current, m, 'color', 'red')
                            elif self.get_edge_attr(current, m, 'flow') == 0:
                                self.set_edge_attr(current, m, 'color', 'black')
                            else:
                                self.set_edge_attr(current, m, 'color', 'green')
                        else:
                            if (self.get_edge_attr(m, current, 'flow') ==
                                self.get_edge_attr(m, current, 'capacity')):
                                self.set_edge_attr(m, current, 'color', 'red')
                            elif self.get_edge_attr(m, current, 'flow') == 0:
                                self.set_edge_attr(m, current, 'color', 'black')
                            else:
                                self.set_edge_attr(m, current, 'color', 'green')
                    self.display()
            # if no path with positive capacity from source sink exists, stop
            if sink not in pred:
                break
            # find capacity of the path
            current = sink
            min_capacity = 'infinite'
            while True:
                m = pred[current]
                if (m,current) in self.edge_attr:
                    arc_capacity = self.edge_attr[(m, current)]['capacity']
                    flow = self.edge_attr[(m, current)]['flow']
                    potential = arc_capacity-flow
                    if min_capacity == 'infinite':
                        min_capacity = potential
                    elif min_capacity > potential:
                        min_capacity = potential
                else:
                    potential = self.edge_attr[(current, m)]['flow']
                    if min_capacity == 'infinite':
                        min_capacity = potential
                    elif min_capacity > potential:
                        min_capacity = potential
                if m == source:
                    break
                current = m
            # update flows on the path
            current = sink
            while True:
                m = pred[current]
                if (m, current) in self.edge_attr:
                    flow = self.edge_attr[(m, current)]['flow']
                    capacity = self.edge_attr[(m, current)]['capacity']
                    new_flow = flow+min_capacity
                    self.edge_attr[(m, current)]['flow'] = new_flow
                    self.edge_attr[(m, current)]['label'] = \
                        str(capacity)+'/'+str(new_flow)
                    if new_flow==capacity:
                        self.edge_attr[(m, current)]['color'] = 'red'
                    else:
                        self.edge_attr[(m, current)]['color'] = 'green'
                    self.display()
                else:
                    flow = self.edge_attr[(current, m)]['flow']
                    capacity = self.edge_attr[(current, m)]['capacity']
                    new_flow = flow-min_capacity
                    self.edge_attr[(current, m)]['flow'] = new_flow
                    if new_flow==0:
                        self.edge_attr[(current, m)]['color'] = 'red'
                    else:
                        self.edge_attr[(current, m)]['color'] = 'green'
                    self.display()
                if m == source:
                    break
                current = m

    def get_negative_cycle(self):
        '''
        API:
            get_negative_cycle(self)
        Description:
            Finds and returns negative cost cycle using 'cost' attribute of
            arcs. Return value is a list of nodes representing cycle it is in
            the following form; n_1-n_2-...-n_k, when the cycle has k nodes.
        Pre:
            Arcs should have 'cost' attribute.
        Return:
            Returns a list of nodes in the cycle if a negative cycle exists,
            returns None otherwise.
        '''
        nl = self.get_node_list()
        i = nl[0]
        r_value = self.fifo_label_correcting(i)
        if r_value[0] is False:
            return r_value[1]
        else:
            return None

    def find_cycle_capacity(self, cycle):
        '''
        API:
            find_cycle_capacity(self, cycle):
        Description:
            Finds capacity of the cycle input.
        Pre:
            (1) Arcs should have 'capacity' attribute.
        Inputs:
            cycle: a list representing a cycle
        Return:
            Returns an integer number representing capacity of cycle.
        '''
        index = 0
        k = len(cycle)
        capacity = self.get_edge_attr(cycle[k-1], cycle[0], 'capacity')
        while index<(k-1):
            i = cycle[index]
            j = cycle[index+1]
            capacity_ij = self.get_edge_attr(i, j, 'capacity')
            if capacity > capacity_ij:
                capacity = capacity_ij
            index += 1
        return capacity

    def fifo_label_correcting(self, source):
        '''
        API:
            fifo_label_correcting(self, source)
        Description:
            finds shortest path from source to every other node. Returns
            predecessor dictionary. If graph has a negative cycle, detects it
            and returns to it.
        Pre:
            (1) 'cost' attribute of arcs. It will be used to compute shortest
            path.
        Input:
            source: source node
        Post:
            Modifies 'distance' attribute of nodes.
        Return:
            If there is no negative cycle returns to (True, pred), otherwise
            returns to (False, cycle) where pred is the predecessor dictionary
            and cycle is a list of nodes that represents cycle. It is in
            [n_1, n_2, ..., n_k] form where the cycle has k nodes.
        '''
        pred = {}
        self.get_node(source).set_attr('distance', 0)
        pred[source] = None
        for n in self.neighbors:
            if n!=source:
                self.get_node(n).set_attr('distance', 'inf')
        q = [source]
        while q:
            i = q[0]
            q = q[1:]
            for j in self.neighbors[i]:
                distance_j = self.get_node(j).get_attr('distance')
                distance_i = self.get_node(i).get_attr('distance')
                c_ij = self.get_edge_attr(i, j, 'cost')
                if distance_j > distance_i + c_ij:
                    self.get_node(j).set_attr('distance', distance_i+c_ij)
                    if j in pred:
                        pred[j] = i
                        cycle = self.label_correcting_check_cycle(j, pred)
                        if cycle is not None:
                            return (False, cycle)
                    else:
                        pred[j] = i
                    if j not in q:
                        q.append(j)
        return (True, pred)

    def label_correcting_check_cycle(self, j, pred):
        '''
        API:
            label_correcting_check_cycle(self, j, pred)
        Description:
            Checks if predecessor dictionary has a cycle, j represents the node
            that predecessor is recently updated.
        Pre:
            (1) predecessor of source node should be None.
        Input:
            j: node that predecessor is recently updated.
            pred: predecessor dictionary
        Return:
            If there exists a cycle, returns the list that represents the
            cycle, otherwise it returns to None.
        '''
        labelled = {}
        for n in self.neighbors:
            labelled[n] = None
        current = j
        while current != None:
            if labelled[current]==j:
                cycle = self.label_correcting_get_cycle(j, pred)
                return cycle
            labelled[current] = j
            current = pred[current]
        return None

    def label_correcting_get_cycle(self, j, pred):
        '''
        API:
            label_correcting_get_cycle(self, labelled, pred)
        Description:
            In label correcting check cycle it is decided pred has a cycle and
            nodes in the cycle are labelled. We will create a list of nodes
            in the cycle using labelled and pred inputs.
        Pre:
            This method should be called from label_correcting_check_cycle(),
            unless you are sure about what you are doing.
        Inputs:
            j: node that predecessor is recently updated. We know that it is
            in the cycle
            pred: predecessor dictionary that contains a cycle
        Post:
            Returns a list of nodes that represents cycle. It is in
            [n_1, n_2, ..., n_k] form where the cycle has k nodes.
        '''
        cycle = []
        cycle.append(j)
        current = pred[j]
        while current!=j:
            cycle.append(current)
            current = pred[current]
        cycle.reverse()
        return cycle

    def augment_cycle(self, amount, cycle):
        '''
        API:
            augment_cycle(self, amount, cycle):
        Description:
            Augments 'amount' unit of flow along cycle.
        Pre:
            Arcs should have 'flow' attribute.
        Inputs:
            amount: an integer representing the amount to augment
            cycle: a list representing a cycle
        Post:
            Changes 'flow' attributes of arcs.
        '''
        index = 0
        k = len(cycle)
        while index<(k-1):
            i = cycle[index]
            j = cycle[index+1]
            if (i,j) in self.edge_attr:
                flow_ij = self.edge_attr[(i,j)]['flow']
                self.edge_attr[(i,j)]['flow'] = flow_ij+amount
            else:
                flow_ji = self.edge_attr[(j,i)]['flow']
                self.edge_attr[(j,i)]['flow'] = flow_ji-amount
            index += 1
        i = cycle[k-1]
        j = cycle[0]
        if (i,j) in self.edge_attr:
            flow_ij = self.edge_attr[(i,j)]['flow']
            self.edge_attr[(i,j)]['flow'] = flow_ij+amount
        else:
            flow_ji = self.edge_attr[(j,i)]['flow']
            self.edge_attr[(j,i)]['flow'] = flow_ji-amount

    def network_simplex(self, display, pivot, root):
        '''
        API:
            network_simplex(self, display, pivot)
        Description:
            Solves minimum cost feasible flow problem using network simplex
            algorithm. It is recommended to use min_cost_flow(algo='simplex')
            instead of using network_simplex() directly. Returns True when an
            optimal solution is found, returns False otherwise. 'flow' attribute
            values of arcs should be considered as junk when returned False.
        Pre:
            (1) check Pre section of min_cost_flow()
        Inputs:
            pivot: specifies pivot rule. Check min_cost_flow()
            display: 'off' for no display, 'pygame' for live update of
            spanning tree.
        Post:
            (1) Changes 'flow' attribute of edges.
        Return:
            Returns True when an optimal solution is found, returns
            False otherwise.
        '''
        # ==== determine an initial tree structure (T,L,U)
        # find a feasible flow
        if not self.find_feasible_flow():
            return False
        t = self.simplex_find_tree()
        self.set_display_mode(display)
        # mark spanning tree arcs
        self.simplex_mark_st_arcs(t)
        # display initial spanning tree
        t.simplex_redraw(display, root)
        t.set_display_mode(display)
        #t.display()
        self.display()
        # set predecessor, depth and thread indexes
        t.simplex_search(root, 1)
        # compute potentials
        self.simplex_compute_potentials(t, root)
        # while some nontree arc violates optimality conditions
        while not self.simplex_optimal(t):
            self.display()
            # select an entering arc (k,l)
            (k,l) = self.simplex_select_entering_arc(t, pivot)
            self.simplex_mark_entering_arc(k, l)
            self.display()
            # determine leaving arc
            ((p,q), capacity, cycle)=self.simplex_determine_leaving_arc(t,k,l)
            # mark leaving arc
            self.simplex_mark_leaving_arc(p, q)
            self.display()
            self.simplex_remove_arc(t, p, q, capacity, cycle)
            # display after arc removed
            self.display()
            self.simplex_mark_st_arcs(t)
            self.display()
            # set predecessor, depth and thread indexes
            t.simplex_redraw(display, root)
            #t.display()
            t.simplex_search(root, 1)
            # compute potentials
            self.simplex_compute_potentials(t, root)
        return True

    def simplex_mark_leaving_arc(self, p, q):
        '''
        API:
            simplex_mark_leving_arc(self, p, q)
        Description:
            Marks leaving arc.
        Inputs:
            p: tail of the leaving arc
            q: head of the leaving arc
        Post:
            Changes color attribute of leaving arc.
        '''
        self.set_edge_attr(p, q, 'color', 'red')

    def simplex_determine_leaving_arc(self, t, k, l):
        '''
        API:
            simplex_determine_leaving_arc(self, t, k, l)
        Description:
            Determines and returns the leaving arc.
        Inputs:
            t: current spanning tree solution.
            k: tail of the entering arc.
            l: head of the entering arc.
        Return:
            Returns the tuple that represents leaving arc, capacity of the
            cycle and cycle.
        '''
        # k,l are the first two elements of the cycle
        cycle = self.simplex_identify_cycle(t, k, l)
        flow_kl = self.get_edge_attr(k, l, 'flow')
        capacity_kl = self.get_edge_attr(k, l, 'capacity')
        min_capacity = capacity_kl
        # check if k,l is in U or L
        if flow_kl==capacity_kl:
            # l,k will be the last two elements
            cycle.reverse()
        n = len(cycle)
        index = 0
        # determine last blocking arc
        t.add_edge(k, l)
        tel = t.get_edge_list()
        while index < (n-1):
            if (cycle[index], cycle[index+1]) in tel:
                flow = self.edge_attr[(cycle[index], cycle[index+1])]['flow']
                capacity = \
                    self.edge_attr[(cycle[index],cycle[index+1])]['capacity']
                if min_capacity >= (capacity-flow):
                    candidate = (cycle[index], cycle[index+1])
                    min_capacity = capacity-flow
            else:
                flow = self.edge_attr[(cycle[index+1], cycle[index])]['flow']
                if min_capacity >= flow:
                    candidate = (cycle[index+1], cycle[index])
                    min_capacity = flow
            index += 1
        # check arc (cycle[n-1], cycle[0])
        if (cycle[n-1], cycle[0]) in tel:
            flow = self.edge_attr[(cycle[n-1], cycle[0])]['flow']
            capacity = self.edge_attr[(cycle[n-1], cycle[0])]['capacity']
            if min_capacity >= (capacity-flow):
                candidate = (cycle[n-1], cycle[0])
                min_capacity = capacity-flow
        else:
            flow = self.edge_attr[(cycle[0], cycle[n-1])]['flow']
            if min_capacity >= flow:
                candidate = (cycle[0], cycle[n-1])
                min_capacity = flow
        return (candidate, min_capacity, cycle)

    def simplex_mark_entering_arc(self, k, l):
        '''
        API:
            simplex_mark_entering_arc(self, k, l)
        Description:
            Marks entering arc (k,l)
        Input:
            k: tail of the entering arc
            l: head of the entering arc
        Post:
            (1) color attribute of the arc (k,l)
        '''
        self.set_edge_attr(k, l, 'color', 'green')

    def simplex_mark_st_arcs(self, t):
        '''
        API:
            simplex_mark_st_arcs(self, t)
        Description:
            Marks spanning tree arcs.
            Case 1, Blue: Arcs that are at lower bound and in tree.
            Case 2, Red: Arcs that are at upper bound and in tree.
            Case 3, Green: Arcs that are between bounds are green.
            Case 4, Brown: Non-tree arcs at lower bound.
            Case 5, Violet: Non-tree arcs at upper bound.
        Input:
            t: t is the current spanning tree
        Post:
            (1) color attribute of edges.
        '''
        tel = t.edge_attr.keys()
        for e in self.get_edge_list():
            flow_e = self.edge_attr[e]['flow']
            capacity_e = self.edge_attr[e]['capacity']
            if e in tel:
                if flow_e == 0:
                    self.edge_attr[e]['color'] = 'blue'
                elif flow_e == capacity_e:
                    self.edge_attr[e]['color'] = 'blue'
                else:
                    self.edge_attr[e]['color'] = 'blue'
            else:
                if flow_e == 0:
                    self.edge_attr[e]['color'] = 'black'
                elif flow_e == capacity_e:
                    self.edge_attr[e]['color'] = 'black'
                else:
                    msg = "Arc is not in ST but has flow between bounds."
                    raise Exception(msg)

    def print_flow(self):
        '''
        API:
            print_flow(self)
        Description:
            Prints all positive flows to stdout. This method can be used for
            debugging purposes.
        '''
        print 'printing current edge, flow, capacity'
        for e in self.edge_attr:
            if self.edge_attr[e]['flow']!=0:
                print e, str(self.edge_attr[e]['flow']).ljust(4),
                print str(self.edge_attr[e]['capacity']).ljust(4)

    def simplex_redraw(self, display, root):
        '''
        API:
            simplex_redraw(self, display, root)
        Description:
            Returns a new graph instance that is same as self but adds nodes
            and arcs in a way that the resulting tree will be displayed
            properly.
        Inputs:
            display: display mode
            root: root node in tree.
        Return:
            Returns a graph same as self.
        '''
        nl = self.get_node_list()
        el = self.get_edge_list()
        new = Graph(type=DIRECTED_GRAPH, layout='dot', display=display)
        pred_i = self.get_node(root).get_attr('pred')
        thread_i = self.get_node(root).get_attr('thread')
        depth_i = self.get_node(root).get_attr('depth')
        new.add_node(root, pred=pred_i, thread=thread_i, depth=depth_i)
        q = [root]
        visited = [root]
        while q:
            name = q.pop()
            visited.append(name)
            neighbors = self.neighbors[name] + self.in_neighbors[name]
            for n in neighbors:
                if n not in new.get_node_list():
                    pred_i = self.get_node(n).get_attr('pred')
                    thread_i = self.get_node(n).get_attr('thread')
                    depth_i = self.get_node(n).get_attr('depth')
                    new.add_node(n, pred=pred_i, thread=thread_i, depth=depth_i)
                if (name,n) in el:
                    if (name,n) not in new.edge_attr:
                        new.add_edge(name,n)
                else:
                    if (n,name) not in new.edge_attr:
                        new.add_edge(n,name)
                if n not in visited:
                    q.append(n)
        for e in el:
            flow = self.edge_attr[e]['flow']
            capacity = self.edge_attr[e]['capacity']
            cost = self.edge_attr[e]['cost']
            new.edge_attr[e]['flow'] = flow
            new.edge_attr[e]['capacity'] = capacity
            new.edge_attr[e]['cost'] = cost
            new.edge_attr[e]['label'] =  "%d/%d/%d" %(flow,capacity,cost)
        return new

    def simplex_remove_arc(self, t, p, q, min_capacity, cycle):
        '''
        API:
            simplex_remove_arc(self, p, q, min_capacity, cycle)
        Description:
            Removes arc (p,q), updates t, updates flows, where (k,l) is
            the entering arc.
        Inputs:
            t: tree solution to be updated.
            p: tail of the leaving arc.
            q: head of the leaving arc.
            min_capacity: capacity of the cycle.
            cycle: cycle obtained when entering arc considered.
        Post:
            (1) updates t.
            (2) updates 'flow' attributes.
        '''
        # augment min_capacity along cycle
        n = len(cycle)
        tel = t.edge_attr.keys()
        index = 0
        while index < (n-1):
            if (cycle[index], cycle[index+1]) in tel:
                flow_e = self.edge_attr[(cycle[index], cycle[index+1])]['flow']
                self.edge_attr[(cycle[index], cycle[index+1])]['flow'] =\
                    flow_e+min_capacity
            else:
                flow_e = self.edge_attr[(cycle[index+1], cycle[index])]['flow']
                self.edge_attr[(cycle[index+1], cycle[index])]['flow'] =\
                    flow_e-min_capacity
            index += 1
        # augment arc cycle[n-1], cycle[0]
        if (cycle[n-1], cycle[0]) in tel:
            flow_e = self.edge_attr[(cycle[n-1], cycle[0])]['flow']
            self.edge_attr[(cycle[n-1], cycle[0])]['flow'] =\
                flow_e+min_capacity
        else:
            flow_e = self.edge_attr[(cycle[0], cycle[n-1])]['flow']
            self.edge_attr[(cycle[0], cycle[n-1])]['flow'] =\
                flow_e-min_capacity
        # remove leaving arc
        t.del_edge((p, q))
        # set label of removed arc
        flow_pq = self.get_edge_attr(p, q, 'flow')
        capacity_pq = self.get_edge_attr(p, q, 'capacity')
        cost_pq = self.get_edge_attr(p, q, 'cost')
        self.set_edge_attr(p, q, 'label',
                           "%d/%d/%d" %(flow_pq,capacity_pq,cost_pq))
        for e in t.edge_attr:
            flow = self.edge_attr[e]['flow']
            capacity = self.edge_attr[e]['capacity']
            cost = self.edge_attr[e]['cost']
            t.edge_attr[e]['flow'] = flow
            t.edge_attr[e]['capacity'] = capacity
            t.edge_attr[e]['cost'] = cost
            t.edge_attr[e]['label'] = "%d/%d/%d" %(flow,capacity,cost)
            self.edge_attr[e]['label'] = "%d/%d/%d" %(flow,capacity,cost)

    def simplex_select_entering_arc(self, t, pivot):
        '''
        API:
            simplex_select_entering_arc(self, t, pivot)
        Description:
            Decides and returns entering arc using pivot rule.
        Input:
            t: current spanning tree solution
            pivot: May be one of the following; 'first_eligible' or 'dantzig'.
            'dantzig' is the default value.
        Return:
            Returns entering arc tuple (k,l)
        '''
        if pivot=='dantzig':
            # pick the maximum violation
            candidate = {}
            for e in self.edge_attr:
                if e in t.edge_attr:
                    continue
                flow_ij = self.edge_attr[e]['flow']
                potential_i = self.get_node(e[0]).get_attr('potential')
                potential_j = self.get_node(e[1]).get_attr('potential')
                capacity_ij = self.edge_attr[e]['capacity']
                c_ij = self.edge_attr[e]['cost']
                cpi_ij = c_ij - potential_i + potential_j
                if flow_ij==0:
                    if cpi_ij < 0:
                        candidate[e] = cpi_ij
                elif flow_ij==capacity_ij:
                    if cpi_ij > 0:
                        candidate[e] = cpi_ij
            for e in candidate:
                max_c = e
                max_v = abs(candidate[e])
                break
            for e in candidate:
                if max_v < abs(candidate[e]):
                    max_c = e
                    max_v = abs(candidate[e])
        elif pivot=='first_eligible':
            # pick the first eligible
            for e in self.edge_attr:
                if e in t.edge_attr:
                    continue
                flow_ij = self.edge_attr[e]['flow']
                potential_i = self.get_node(e[0]).get_attr('potential')
                potential_j = self.get_node(e[1]).get_attr('potential')
                capacity_ij = self.edge_attr[e]['capacity']
                c_ij = self.edge_attr[e]['cost']
                cpi_ij = c_ij - potential_i + potential_j
                if flow_ij==0:
                    if cpi_ij < 0:
                        max_c = e
                        max_v = abs(cpi_ij)
                elif flow_ij==capacity_ij:
                    if cpi_ij > 0:
                        max_c = e
                        max_v = cpi_ij
        else:
            raise Exception("Unknown pivot rule.")
        return max_c

    def simplex_optimal(self, t):
        '''
        API:
            simplex_optimal(self, t)
        Description:
            Checks if the current solution is optimal, if yes returns True,
            False otherwise.
        Pre:
            'flow' attributes represents a solution.
        Input:
            t: Graph instance tat reperesents spanning tree solution.
        Return:
            Returns True if the current solution is optimal (optimality
            conditions are satisfied), else returns False
        '''
        for e in self.edge_attr:
            if e in t.edge_attr:
                continue
            flow_ij = self.edge_attr[e]['flow']
            potential_i = self.get_node(e[0]).get_attr('potential')
            potential_j = self.get_node(e[1]).get_attr('potential')
            capacity_ij = self.edge_attr[e]['capacity']
            c_ij = self.edge_attr[e]['cost']
            cpi_ij = c_ij - potential_i + potential_j
            if flow_ij==0:
                if cpi_ij < 0:
                    return False
            elif flow_ij==capacity_ij:
                if cpi_ij > 0:
                    return False
        return True

    def simplex_find_tree(self):
        '''
        API:
            simplex_find_tree(self)
        Description:
            Assumes a feasible flow solution stored in 'flow' attribute's of
            arcs and converts this solution to a feasible spanning tree
            solution.
        TODO(aykut): The solution we find is not strongly feasible. Fix this.
        Pre:
            (1) 'flow' attributes represents a feasible flow solution.
        Post:
            (1) 'flow' attributes may change when eliminating cycles.
        Return:
            Return a Graph instance that is a spanning tree solution.
        '''
        # find a cycle
        solution_g = self.get_simplex_solution_graph()
        cycle = solution_g.simplex_find_cycle()
        while cycle is not None:
            # find amount to augment and direction
            amount = self.simplex_augment_cycle(cycle)
            # augment along the cycle
            self.augment_cycle(amount, cycle)
            # find a new cycle
            solution_g = self.get_simplex_solution_graph()
            cycle = solution_g.simplex_find_cycle()
        # check if the solution is connected
        while self.simplex_connect(solution_g):
            pass
        # add attributes
        for e in self.edge_attr:
            flow = self.edge_attr[e]['flow']
            capacity = self.edge_attr[e]['capacity']
            cost = self.edge_attr[e]['cost']
            self.edge_attr[e]['label'] = "%d/%d/%d" %(flow,capacity,cost)
            if e in solution_g.edge_attr:
                solution_g.edge_attr[e]['flow'] = flow
                solution_g.edge_attr[e]['capacity'] = capacity
                solution_g.edge_attr[e]['cost'] = cost
                solution_g.edge_attr[e]['label'] = "%d/%d/%d" %(flow,capacity,cost)
        return solution_g

    def simplex_connect(self, solution_g):
        '''
        API:
            simplex_connect(self, solution_g)
        Description:
            At this point we assume that the solution does not have a cycle.
            We check if all the nodes are connected, if not we add an arc to
            solution_g that does not create a cycle and return True. Otherwise
            we do nothing and return False.
        Pre:
            (1) We assume there is no cycle in the solution.
        Input:
            solution_g: current spanning tree solution instance.
        Post:
            (1) solution_g is updated. An arc that does not create a cycle is
            added.
            (2) 'component' attribute of nodes are changed.
        Return:
            Returns True if an arc is added, returns False otherwise.
        '''
        nl = solution_g.get_node_list()
        current = nl[0]
        pred = solution_g.simplex_search(current, current)
        separated = pred.keys()
        for n in nl:
            if solution_g.get_node(n).get_attr('component') != current:
                # find an arc from n to seperated
                for m in separated:
                    if (n,m) in self.edge_attr:
                        solution_g.add_edge(n,m)
                        return True
                    elif (m,n) in self.edge_attr:
                        solution_g.add_edge(m,n)
                        return True
        return False

    def simplex_search(self, source, component_nr):
        '''
        API:
            simplex_search(self, source, component_nr)
        Description:
            Searches graph starting from source. Its difference from usual
            search is we can also go backwards along an arc. When the graph
            is a spanning tree it computes predecessor, thread and depth
            indexes and stores them as node attributes. These values should be
            considered as junk when the graph is not a spanning tree.
        Input:
            source: source node
            component_nr: component number
        Post:
            (1) Sets the component number of all reachable nodes to component.
            Changes 'component' attribute of nodes.
            (2) Sets 'pred', 'thread' and 'depth' attributes of nodes. These
            values are junk if the graph is not a tree.
        Return:
            Returns predecessor dictionary.
        TODO(aykut): usual search is bugged, it does not set component number
        for source. If you fix that update this method (since it sets component
        number of source after search).
        '''
        q = [source]
        pred = {source:None}
        depth = {source:0}
        sequence = []
        for n in self.neighbors:
            self.get_node(n).set_attr('component', None)
        while q:
            current = q.pop()
            self.get_node(current).set_attr('component', component_nr)
            sequence.append(current)
            neighbors = self.in_neighbors[current] + self.neighbors[current]
            for n in neighbors:
                if n in pred:
                    continue
                self.get_node(n).set_attr('component', component_nr)
                pred[n] = current
                depth[n] = depth[current]+1
                q.append(n)
        for i in range(len(sequence)-1):
            self.get_node(sequence[i]).set_attr('thread', int(sequence[i+1]))
        self.get_node(sequence[-1]).set_attr('thread', int(sequence[0]))
        for n in pred:
            self.get_node(n).set_attr('pred', pred[n])
            self.get_node(n).set_attr('depth', depth[n])
        return pred

    def simplex_augment_cycle(self, cycle):
        '''
        API:
            simplex_augment_cycle(self, cycle)
        Description:
            Augments along the cycle to break it.
        Pre:
            'flow', 'capacity' attributes on arcs.
        Input:
            cycle: list representing a cycle in the solution
        Post:
            'flow' attribute will be modified.
        '''
        # find amount to augment
        index = 0
        k = len(cycle)
        el = self.edge_attr.keys()
        # check arc (cycle[k-1], cycle[0])
        if (cycle[k-1], cycle[0]) in el:
            min_capacity = self.edge_attr[(cycle[k-1], cycle[0])]['capacity']-\
                              self.edge_attr[(cycle[k-1], cycle[0])]['flow']
        else:
            min_capacity = self.edge_attr[(cycle[0], cycle[k-1])]['flow']
        # check rest of the arcs in the cycle
        while index<(k-1):
            i = cycle[index]
            j = cycle[index+1]
            if (i,j) in el:
                capacity_ij = self.edge_attr[(i,j)]['capacity'] -\
                              self.edge_attr[(i,j)]['flow']
            else:
                capacity_ij = self.edge_attr[(j,i)]['flow']
            if min_capacity > capacity_ij:
                min_capacity = capacity_ij
            index += 1
        return min_capacity

    def simplex_find_cycle(self):
        '''
        API:
            simplex_find_cycle(self)
        Description:
            Returns a cycle (list of nodes) if the graph has one, returns None
            otherwise. Uses DFS. During DFS checks existence of arcs to lower
            depth regions. Note that direction of the arcs are not important.
        Return:
            Returns list of nodes that represents cycle. Returns None if the
            graph does not have any cycle.
        '''
        # make a dfs, if you identify an arc to a lower depth node we have a
        # cycle
        nl = self.get_node_list()
        q = [nl[0]]
        visited = []
        depth = {nl[0]:0}
        pred = {nl[0]:None}
        for n in nl:
            self.get_node(n).set_attr('component', None)
        component_nr = int(nl[0])
        self.get_node(nl[0]).set_attr('component', component_nr)
        while True:
            while q:
                current = q.pop()
                visited.append(current)
                neighbors = self.in_neighbors[current] +\
                    self.neighbors[current]
                for n in neighbors:
                    if n==pred[current]:
                        continue
                    self.get_node(n).set_attr('component', component_nr)
                    if n in depth:
                        # we have a cycle
                        cycle1 = []
                        cycle2 = []
                        temp = n
                        while temp is not None:
                            cycle1.append(temp)
                            temp = pred[temp]
                        temp = current
                        while temp is not None:
                            cycle2.append(temp)
                            temp = pred[temp]
                        cycle1.pop()
                        cycle1.reverse()
                        cycle2.extend(cycle1)
                        return cycle2
                    else:
                        pred[n] = current
                        depth[n] = depth[current] + 1
                    if n not in visited:
                        q.append(n)
            flag = False
            for n in nl:
                if self.get_node(n).get_attr('component') is None:
                    q.append(n)
                    depth = {n:0}
                    pred = {n:None}
                    visited = []
                    component_nr = int(n)
                    self.get_node(n).set_attr('component', component_nr)
                    flag = True
                    break
            if not flag:
                break
        return None

    def get_simplex_solution_graph(self):
        '''
        API:
            get_simplex_solution_graph(self):
        Description:
            Assumes a feasible flow solution stored in 'flow' attribute's of
            arcs. Returns the graph with arcs that have flow between 0 and
            capacity.
        Pre:
            (1) 'flow' attribute represents a feasible flow solution. See
            Pre section of min_cost_flow() for details.
        Return:
            Graph instance that only has the arcs that have flow strictly
            between 0 and capacity.
        '''
        simplex_g = Graph(type=DIRECTED_GRAPH)
        for i in self.neighbors:
            simplex_g.add_node(i)
        for e in self.edge_attr:
            flow_e = self.edge_attr[e]['flow']
            capacity_e = self.edge_attr[e]['capacity']
            if flow_e>0 and flow_e<capacity_e:
                simplex_g.add_edge(e[0], e[1])
        return simplex_g

    def simplex_compute_potentials(self, t, root):
        '''
        API:
            simplex_compute_potentials(self, root)
        Description:
            Computes node potentials for a minimum cost flow problem and stores
            them as node attribute 'potential'. Based on pseudocode given in
            Network Flows by Ahuja et al.
        Pre:
            (1) Assumes a directed graph in which each arc has a 'cost'
            attribute.
            (2) Uses 'thread' and 'pred' attributes of nodes.
        Inputs:
            t: Current spanning tree solution, its type is Graph.
            root: root node of the tree.
        Post:
            Keeps the node potentials as 'potential' attribute.
        '''
        self.get_node(root).set_attr('potential', 0)
        j = t.get_node(root).get_attr('thread')
        while j is not root:
            i = t.get_node(j).get_attr('pred')
            potential_i = self.get_node(i).get_attr('potential')
            if (i,j) in self.edge_attr:
                c_ij = self.edge_attr[(i,j)]['cost']
                self.get_node(j).set_attr('potential', potential_i-c_ij)
            if (j,i) in self.edge_attr:
                c_ji = self.edge_attr[(j,i)]['cost']
                self.get_node(j).set_attr('potential', potential_i+c_ji)
            j = t.get_node(j).get_attr('thread')

    def simplex_identify_cycle(self, t, k, l):
        '''
        API:
            identify_cycle(self, t, k, l)
        Description:
            Identifies and returns to the pivot cycle, which is a list of
            nodes.
        Pre:
            (1) t is spanning tree solution, (k,l) is the entering arc.
        Inputs:
            t: current spanning tree solution
            k: tail of the entering arc
            l: head of the entering arc
        Returns:
            List of nodes in the cycle.
        '''
        i = k
        j = l
        cycle = []
        li = [k]
        lj = [j]
        while i is not j:
            depth_i = t.get_node(i).get_attr('depth')
            depth_j = t.get_node(j).get_attr('depth')
            if depth_i > depth_j:
                i = t.get_node(i).get_attr('pred')
                li.append(i)
            elif depth_i < depth_j:
                j = t.get_node(j).get_attr('pred')
                lj.append(j)
            else:
                i = t.get_node(i).get_attr('pred')
                li.append(i)
                j = t.get_node(j).get_attr('pred')
                lj.append(j)
        cycle.extend(lj)
        li.pop()
        li.reverse()
        cycle.extend(li)
        # l is beginning k is end
        return cycle

    def min_cost_flow(self, display = 'off', **args):
        '''
        API:
            min_cost_flow(self, **args)
        Description:
            Solves minimum cost flow problem using node/edge attributes with
            the algorithm specified.
        Pre:
            (1) Assumes a directed graph in which each arc has 'capacity' and
            'cost' attributes.
            (2) Nodes should have 'demand' attribute. This value should be
            positive for supply and negative for demand, and 0 for transhipment
            nodes.
            (3) The graph should be connected.
            (4) Assumes (i,j) and (j,i) does not exist together. Needed when
            solving max flow. (max flow problem is solved to get a feasible
            flow).
        Inputs:
            display: 'off' for no display, 'pygame' for live update of tree
            args: may have the following
                display: display method, if not given current mode (the one
                    specified by __init__ or set_display) will be used.
                algo: determines algorithm to use, can be one of the following
                    'simplex': network simplex algorithm
                    'cycle_canceling': cycle canceling algorithm
                    'simplex' is used if not given.
                    see Network Flows by Ahuja et al. for details of algorithms.
                pivot: valid if algo is 'simlex', determines pivoting rule for
                    simplex, may be one of the following; 'first_eligible',
                    'dantzig' or 'scaled'.
                    'dantzig' is used if not given.
                    see Network Flows by Ahuja et al. for pivot rules.
                root: valid if algo is 'simlex', specifies the root node for
                    simplex algorithm. It is name of the one of the nodes. It
                    will be chosen randomly if not provided.
        Post:
            The 'flow' attribute of each arc gives the optimal flows.
            'distance' attribute of the nodes are also changed during max flow
            solution process.
        Examples:
            g.min_cost_flow():
                solves minimum cost feasible flow problem using simplex
                algorithm with dantzig pivoting rule.
                See pre section for details.
            g.min_cost_flow(algo='cycle_canceling'):
                solves minimum cost feasible flow problem using cycle canceling
                agorithm.
            g.min_cost_flow(algo='simplex', pivot='scaled'):
                solves minimum cost feasible flow problem using network simplex
                agorithm with scaled pivot rule.
        '''
        if 'algo' in args:
            algorithm = args['algo']
        else:
            algorithm = 'simplex'
        if algorithm is 'simplex':
            if 'root' in args:
                root = args['root']
            else:
                for k in self.neighbors:
                    root = k
                    break
            if 'pivot' in args:
                if not self.network_simplex(display, args['pivot'], root):
                    print 'problem is infeasible'
            else:
                if not self.network_simplex(display, 'dantzig', root):
                    print 'problem is infeasible'
        elif algorithm is 'cycle_canceling':
            if not self.cycle_canceling(display):
                print 'problem is infeasible'
        else:
            print args['algo'], 'is not a defined algorithm. Exiting.'
            return

    def random(self, numnodes = 10, degree_range = None, length_range = None,
               density = None, edge_format = None, node_format = None,
               Euclidean = False, seedInput = 0):
        random.seed(seedInput)
        if edge_format == None:
            edge_format = {'fontsize':10,
                           'fontcolor':'blue'}
        if node_format == None:
            node_format = {'height':0.5,
                           'width':0.5,
                           'fixedsize':'true',
                           'fontsize':10,
                           'fontcolor':'red',
                           'shape':'circle',
                           }
        if Euclidean == False:
            for m in range(numnodes):
                self.add_node(m, **node_format)
            if degree_range is not None:
                for m in range(numnodes):
                    for i in range(random.randint(degree_range[0], degree_range[1])):
                        n = random.randint(1, numnodes)
                        if (m,n) not in self.edge_attr and (n,m) not in self.edge_attr and m != n:
                            if length_range is not None:
                                length = random.randint(length_range[0],
                                                 length_range[1])
                                self.add_edge(m, n, cost = length,
                                              label = str(length),
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            elif density != None:
                for m in range(numnodes):
                    if self.graph_type == DIRECTED_GRAPH:
                        numnodes2 = numnodes
                    else:
                        numnodes2 = m
                    for n in range(numnodes2):
                        if random.random() < density and m != n:
                            if length_range is not None:
                                length = random.randint(length_range[0],
                                                 length_range[1])
                                self.add_edge(m, n, cost = length,
                                              label = str(length),
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            else:
                print "Must set either degree range or density"
        else:
            for m in range(numnodes):
                ''' Assigns random coordinates (between 1 and 20) to the nodes
                '''
                self.add_node(m, locationx = random.randint(1, 20),
                              locationy = random.randint(1, 20), **node_format)
            if degree_range is not None:
                for m in range(numnodes):
                    for i in range(random.randint(degree_range[0], degree_range[1])):
                        n = random.randint(1, numnodes)
                        if (m,n) not in self.edge_attr and (n,m) not in self.edge_attr and m != n:
                            if length_range is None:
                                ''' calculates the euclidean norm and round it
                                to an integer '''
                                length = round((((self.get_node(n).get_attr('locationx') -
                                                  self.get_node(m).get_attr('locationx')) ** 2 +
                                                 (self.get_node(n).get_attr('locationy') -
                                                  self.get_node(m).get_attr('locationy')) ** 2) ** 0.5), 0)
                                self.add_edge(m, n, cost = int(length), label = str(int(length)),
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            elif density != None:
                for m in range(numnodes):
                    if self.graph_type == DIRECTED_GRAPH:
                        numnodes2 = numnodes
                    else:
                        numnodes2 = m
                    for n in range(numnodes2):
                        if random.random() < density:
                            if length_range is None:
                                ''' calculates the euclidean norm and round it
                                to an integer '''
                                length = round((((self.get_node(n).get_attr('locationx') -
                                                  self.get_node(m).get_attr('locationx')) ** 2 +
                                                 (self.get_node(n).get_attr('locationy') -
                                                  self.get_node(m).get_attr('locationy')) ** 2) ** 0.5), 0)
                                self.add_edge(m, n, cost = int(length), label = str(int(length)),
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            else:
                print "Must set either degree range or density"

    def page_rank(self, damping_factor=0.85, max_iterations=100,
                  min_delta=0.00001):
        """
        Compute and return the PageRank in a directed graph.

        This function was originally taken from here and modified for this
        graph class:
        http://code.google.com/p/python-graph/source/browse/trunk/core/pygraph/algorithms/pagerank.py

        @type  graph: digraph
        @param graph: Digraph.

        @type  damping_factor: number
        @param damping_factor: PageRank dumping factor.

        @type  max_iterations: number
        @param max_iterations: Maximum number of iterations.

        @type  min_delta: number
        @param min_delta: Smallest variation required to have a new iteration.

        @rtype:  Dict
        @return: Dict containing all the nodes PageRank.
        """
        nodes = self.get_node_list()
        graph_size = len(nodes)
        if graph_size == 0:
            return {}
        #value for nodes without inbound links
        min_value = (1.0-damping_factor)/graph_size
        # itialize the page rank dict with 1/N for all nodes
        pagerank = dict.fromkeys(nodes, 1.0/graph_size)
        for i in range(max_iterations):
            diff = 0 #total difference compared to last iteraction
            # computes each node PageRank based on inbound links
            for node in nodes:
                rank = min_value
                for referring_page in self.get_in_neighbors(node):
                    rank += (damping_factor * pagerank[referring_page] /
                             len(self.get_neighbors(referring_page)))
                diff += abs(pagerank[node] - rank)
                pagerank[node] = rank
            #stop if PageRank has converged
            if diff < min_delta:
                break
        return pagerank


class DisjointSet(Graph):
    def __init__(self, optimize = True, **attrs):
        attrs['type'] = DIRECTED_GRAPH
        Graph.__init__(self, **attrs)
        self.sizes = {}
        self.optimize = optimize

    def add(self, aList):
        self.add_node(aList[0])
        for i in range(1, len(aList)):
            self.add_edge(aList[i], aList[0])
        self.sizes[aList[0]] = len(aList)

    def union(self, i, j):
        roots = (self.find(i), self.find(j))
        if roots[0] == roots[1]:
            return False
        if self.sizes[roots[0]] <= self.sizes[roots[1]] or not self.optimize:
            self.add_edge(roots[0], roots[1])
            self.sizes[roots[1]] += self.sizes[roots[0]]
            return True
        else:
            self.add_edge(roots[1], roots[0])
            self.sizes[roots[0]] += self.sizes[roots[1]]
            return True

    def find(self, i):
        current = i
        edge_list = []
        while len(self.get_neighbors(current)) != 0:
            successor = self.get_neighbors(current)[0]
            edge_list.append((current, successor))
            current = successor
        if self.optimize:
            for e in edge_list:
                if e[1] != current:
                    self.del_edge((e[0], e[1]))
                    self.add_edge(e[0], current)
        return current


if __name__ == '__main__':
    G = Graph(type = DIRECTED_GRAPH, splines = 'true')
#    G.random(numnodes = 7, density = 0.7, length_range = (1, 10), seedInput = 5)
    G.random(numnodes = 7, density = 0.7, Euclidean = True, seedInput = 5)
#    G.random(numnodes = 10, density = 0.5, seedInput = 5)

#    G.set_display_mode('file')
#    print G.to_string()
#    G.display(basename='try.png', format='png')

#    G.search(0, display = 'pygame', algo = 'Prims')
    G.minimum_spanning_tree_kruskal(display = 'pygame')
    #G.search(0, display = 'pygame')
