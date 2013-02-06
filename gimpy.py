'''
This module implements a Graph class based on the class provided by Pydot.
You must have installed Pydot and Graphviz. Optionally, if you have
PIL, xdot, or Pygame installed, these can also be used for display
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'aykut@lehigh.edu'
__url__        = None
__title__      = 'GiMPy (Graph Methods in Python)'

import sys
from pydot import Dot, Node, Edge
from pydot import Subgraph as Dotsubgraph
from pydot import Cluster as Dotcluster
from pydot import quote_if_necessary
from random import random, randint, seed
from Queues import Queue
from Stack import Stack
from LinkedList import LinkedList
import operator
from StringIO import StringIO
from Queues import PriorityQueue
from operator import itemgetter
from string import atoi

try:
    from PIL import Image
except ImportError:
    PIL_installed = False
    print 'Python Image Library not installed'
else:
    PIL_installed = True
    print 'Found Python Image Library'

try:
    import gtk
    import xdot
except ImportError:
    xdot_installed = False
    print 'Xdot not installed'
else:
    xdot_installed = True
    print 'Found xdot installation'

try:
    from pygame.locals import QUIT, KEYDOWN
    from pygame import display, image, event, init
except ImportError:
    pygame_installed = False
    print 'Pygame not installed'
else:
    pygame_installed = True
    print 'Found pygame installation'

try:
    from lxml import etree
except ImportError:
    etree_installed = False
    print 'Etree could not be imported from lxml'
else:
    etree_installed = True
    print 'Found etree in lxml'

try:
    from gexf import Gexf
except ImportError:
    gexf_installed = False
    print 'Gexf not installed'
else:
    gexf_installed = True
    print 'Found gexf installation'

class Graph(Dot):
    
    def __init__(self, display = 'off', dot_data = None, 
                 dot_file = None, **attrs):
        if 'layout' not in attrs:
            attrs['layout'] = 'fdp'
        if 'graph_type' not in attrs:
            attrs['graph_type'] = 'graph'
        #self.obj_dict['type'] = attrs['graph_type']
        Dot.__init__(self, **attrs)
        self.display_mode = display
        self.graph_type = attrs['graph_type']
        self.num_components = None
        if self.graph_type == 'digraph':
            self.in_neighbor_lists = {}
            self.out_neighbor_lists = {}
        else:
            self.neighbor_lists = {}
        if display == 'pygame':
            if pygame_installed:
                init()
            else:
                print "Pygame module not installed, graphical display disabled"
    
    def add_node(self, name, **attrs):
        if 'label' not in attrs:
            attrs['label'] = str(name)
        Dot.add_node(self, Node(name, **attrs))
        if self.graph_type == 'digraph':
            if name in self.in_neighbor_lists:
                raise Exception, "Node with that name already exists"
            self.in_neighbor_lists[str(name)] = LinkedList()
            self.out_neighbor_lists[str(name)] = LinkedList()
        else:
            if str(name) in self.neighbor_lists:
                raise Exception, "Node with that name already exists"
            self.neighbor_lists[str(name)] = LinkedList()
        self.num_components = None
       
    def del_node(self, name):
        if self.graph_type == 'digraph':
            try:
                for neighbor in self.out_neighbor_lists[str(name)]:
                    self.del_edge(name, neighbor)
                for neighbor in self.in_neighbor_lists[str(name)]:
                    self.del_edge(neighbor, name)
                del self.out_neighbor_lists[str(name)]
                del self.in_neighbor_lists[str(name)]
            except KeyError:
                return False
        if self.graph_type == 'graph':
            try:
                for n in self.neighborlists[str(name)]:
                    del self.neighborlists[n][str(name)]
                del self.neighborlists[str(name)]
            except KeyError:
                return False
        Dot.del_node(self, quote_if_necessary(str(name)))

    def get_node(self, name):
        if isinstance(name, Node):
            return name
        nodes = Dot.get_node(self, quote_if_necessary(str(name)))
        if len(nodes) == 1:
            return nodes[0]
        elif len(nodes) == 0:
            return None
        else:
            raise Exception("Multiple instances of node", name, 
                            "present in Tree")

    def get_node_list(self):
        return self.obj_dict['nodes'].keys()

    def get_node_attr(self, n, attr):
        if isinstance(n, Node):
            return n.get(attr)
        else:
            return self.get_node(n).get(attr)

    def set_node_attr(self, n, attr, val):
        if isinstance(n, Node):
            return n.set(attr, val)
        else:
            return self.get_node(str(n)).set(attr, val)

    def set_component_number(self, n, component):
        self.set_node_attr(n, 'component', component)

    def add_edge(self, m, n, **attrs):
        if self.get_node(m) == None:
            self.add_node(m)
        if self.get_node(n) == None:
            self.add_node(n)
        Dot.add_edge(self, Edge(self.get_node(m), self.get_node(n), **attrs))
        if self.graph_type == 'digraph':
            self.out_neighbor_lists[str(m)].append(str(n))
            self.in_neighbor_lists[str(n)].append(str(m))
        else:
            self.neighbor_lists[str(m)].append(str(n))
            self.neighbor_lists[str(n)].append(str(m))
        self.num_components = None
        
    def del_edge(self, m, n):
        if self.graph_type == 'digraph':
            try:
                del self.get_out_neighbors(str(m))[str(n)]
                del self.get_in_neighbors(str(n))[str(m)]
            except KeyError:
                return False
        if self.graph_type == 'graph':
            try:
                del self.get_neighbors(str(m))[str(n)]
                del self.get_neighbors(str(n))[str(m)]
            except KeyError:
                return False
        Dot.del_edge(self, quote_if_necessary(str(m)), 
                     quote_if_necessary(str(n)))

    def get_edge(self, m, n):
        edges = Dot.get_edge(self, quote_if_necessary(str(m)), 
                             quote_if_necessary(str(n)))
        if len(edges) == 1:
            return edges[0]
        elif len(edges) == 0:
            return None
        else:
            raise Exception("Multiple instances of edge (", m, n, 
                            ") present in Tree")
        
    def get_edge_list(self):
        return self.obj_dict['edges'].keys()

    def get_edge_attr(self, m, n, attr):
        return self.get_edge(m, n).get(attr)
    
    def set_edge_attr(self, m, n, attr, val):
        return self.get_edge(m, n).set(attr, val)

    def get_neighbors(self, n):
        if self.graph_type == 'digraph':
            raise Exception, "get_neighbors method called for digraph" 
        return self.neighbor_lists[str(n)]

    def get_out_neighbors(self, n):
        if self.graph_type != 'digraph':
            raise Exception("get_out_neighbors method called ",
                            "for undirected graph")
        try:
            return self.out_neighbor_lists[str(n)]
        except KeyError:
            pass

    def get_in_neighbors(self, n):
        if self.graph_type != 'digraph':
            raise Exception("get_in_neighbors method called for ",
                            "undirected graph")
        return self.in_neighbor_lists[str(n)]

    def label_components(self, display = None):
        '''
        This method labels the nodes of an undirected graph with component 
        numbers so that each node has the same label as all nodes in the 
        same component
        '''
        if self.graph_type == 'digraph':
            raise Exception("label_components only works for ",
                            "undirected graphs")
        if self.num_components != None:
            return 
        self.num_components = 0
        for n in self.get_node_list():
            self.set_component_number(n, None)
        for n in self.get_node_list():
            if self.get_node_attr(n, 'component') == None:
                #self.dfs(n, display, self.num_components)
                self.dfs(n, component = self.num_components)
                self.num_components += 1 
            
    def get_finishing_time(self, n):
        return self.get_node_attr(n, 'finish_time')
    
    def label_strong_component(self, root, disc_count = 0, finish_count = 1, 
                               component = None):
        if self.graph_type == 'graph':
            raise Exception("label_strong_componentsis only for ",
                            "directed graphs")
        if self.num_components != None:
            return 
        self.num_components = 0
        for n in self.get_node_list():
            self.set_component_number(n, None)
        for n in self.get_node_list():
            if self.get_node_attr(n, 'disc_time') == None:
                self.dfs(n, component = self.num_components)

        self.num_components = 0
        for n in self.get_node_list():
            self.set_component_number(n, None)
        for n in self.get_node_list():
            if self.get_node_attr(n, 'component') == None:
                self.dfs(n, component = self.num_components, transpose = True)
                self.num_components += 1

    def dfs(self, root, disc_count = 0, finish_count = 1, component = None,
            transpose = False):
        if self.graph_type == 'digraph':
            if not transpose:
                neighbors = self.get_out_neighbors
            else:
                neighbors = self.get_in_neighbors
        else:
            neighbors = self.get_neighbors
        self.set_node_attr(root, 'component', component)
        disc_count += 1
        self.set_node_attr(root, 'disc_time', disc_count)
        if transpose:
            fTime = []
            for n in neighbors(root):
                fTime.append((n,self.get_finishing_time(n)))
            neighbor_list = sorted(fTime, key=itemgetter(1))
            neighbor_list = list(t[0] for t in neighbor_list)
            neighbor_list.reverse()
        else:
            neighbor_list = neighbors(root)
        for i in neighbor_list:
            if not transpose:
                if self.get_node_attr(i, 'disc_time') is None:
                    disc_count, finish_count = self.dfs(i, disc_count, 
                                                        finish_count, 
                                                        component, transpose)
            else:
                if self.get_node_attr(i, 'component') is None:
                    disc_count, finish_count = self.dfs(i, disc_count, 
                                                        finish_count, 
                                                        component, transpose)
        finish_count += 1
        self.set_node_attr(root, 'finish_time', finish_count)
        return disc_count, finish_count

    def bfs(self, root, display = None, component = None):
        self.search(root, display = display, component = component, q = Queue())
        
    def path(self, source, destination, display = None):
        return self.search(source, destination, display = display)

    def shortest_unweighted_path(self, source, destination, display = None):
        return self.search(source, destination, display = display, q = Queue(), 
                           algo = 'BFS')

    def shortest_weighted_path(self, source, destination = None, 
                               display = None, algo = 'Dijkstra'):
        '''
        This method determines the shortest paths to all nodes reachable from 
        "source" if "destination" is not given. Otherwise, it determines a 
        shortest path from "source" to "destination". The variable "q" must 
        be an instance of a priority queue. 
        '''
        nl = self.get_node_list()
        neighbors = self.get_out_neighbors

        for i in nl:
            self.set_node_attr(i, 'color', 'black')
            self.set_node_attr(i, 'distance', 'inf')
            for j in neighbors(i):
                self.set_edge_attr(i, j, 'color', 'black')
        
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)

        if algo == 'Dijkstra':
            q = PriorityQueue()
        elif algo == 'FIFO':
            q = Queue()
        else:
            print 'Unknown algorithm'
            return
        
        pred = {source:source}
        q.push(str(source))
        self.set_node_attr(source, 'distance', 0)
        done = False
        while not q.isEmpty() and not done:
            current = q.pop()
            current_estimate = self.get_node_attr(current, 'distance')
            self.set_node_attr(current, 'color', 'blue')
            if current == str(destination):
                done = True
                break
            self.display()
            for n in neighbors(current):
                if (self.get_node_attr(n, 'color') != 'green' and 
                    n != pred[current]):
                    self.set_edge_attr(current, n, 'color', 'yellow')
                    self.display()
                    new_estimate = (current_estimate + 
                                    self.get_edge_attr(current, n, 'cost'))
                    if (self.get_node_attr(n, 'distance') == 'inf' or 
                        new_estimate < self.get_node_attr(n, 'distance')):
                        if n in pred and n != pred[n]:
                            self.set_edge_attr(pred[n], n, 'color', 'black')
                        pred[n] = current
                        self.set_edge_attr(current, n, 'color', 'green')
                        self.set_node_attr(n, 'color', 'red')
                        self.set_node_attr(n, 'label', new_estimate)
                        self.set_node_attr(n, 'distance', new_estimate)
                        if algo == 'Dijkstra':
                            q.push(n, new_estimate)
                        elif algo == 'FIFO':
                            q.push(n)
                        self.display()
                        self.set_node_attr(n, 'color', 'black')
                    else:
                        self.set_edge_attr(current, n, 'color', 'black')
            if algo == 'Dijkstra':
                self.set_node_attr(current, 'color', 'green')
            else:
                cycle = self.check_for_cycle(source, pred)
                if cycle is not None:
                    print 'Negative cycle detected'
                    return cycle, None 
                self.set_node_attr(current, 'color', 'black')
            self.display()
                    
        if done:
            path = [str(destination)]
            current = str(destination)        
            while current != str(source):
                path.insert(0, pred[current])
                current = pred[current]
            return path, q.get_priority(current)
        
        return pred
    
    def check_for_cycle(self, source, tree):
        labels = {}
        found = False
        for start in self.get_node_list():
            if start not in labels and start in tree and tree[start] != start:
                labels[start] = start
                pred = tree[start]
                while True:
                    if pred not in labels:
                        labels[pred] = start
                        if pred != tree[pred]:
                            pred = tree[pred]
                        else:
                            break
                    else:
                        if labels[pred] == start:
                            found = True
                        break
            if found:
                start = pred
                cycle = [start]
                pred = tree[start]
                while pred != start:
                    cycle.append(pred)
                    pred = tree[pred]
                return cycle
        return None
    
    def minimum_spanning_tree_prim(self, source, display = None, 
                                   q = PriorityQueue()):
        '''
        This method determines a minimum spanning tree of all nodes reachable 
        from "source" using Prim's Algorithm
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
        if isinstance(q, PriorityQueue):
            addToQ = q.push
            removeFromQ = q.pop
            peek = q.peek
            isEmpty = q.isEmpty
        if self.graph_type == 'digraph':
            neighbors = self.get_out_neighbors
        else:
            neighbors = self.get_neighbors

        pred = {}
        addToQ(str(source))
        done = False
        while not isEmpty() and not done:
            current = removeFromQ()
            self.set_node_attr(current, 'color', 'blue')
            if current != str(source):
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

    def get_edge_cost(self, edge):
        return self.get_edge_attr(edge[0], edge[1], 'cost')

    def minimum_spanning_tree_kruskal(self, display = None, components = None):
        '''
        This method determines a minimum spanning tree of all nodes reachable 
        from "source" using Kruskal's Algorithm
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
        
        if components is None:
            components = DisjointSet(display = 'pygame', layout = 'dot', 
                                     optimize = False)
            
        sorted_edge_list = sorted(self.obj_dict['edges'].keys(), 
                                  key = self.get_edge_cost)
        
        edges = []
        for n in self.get_node_list():
            components.add([n])
        components.display()   
        for e in sorted_edge_list:
            print e
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
            
    def search(self, source, destination = None, display = None, 
               component = None, q = Stack(),
               algo = 'DFS', reverse = False, **kargs):
        '''
        This method determines all nodes reachable from "source" if 
        "destination" is not given. Otherwise, it determines whether there is 
        a path from "source" to "destination". Optionally, it marks all nodes 
        reachable from "source" with a component number. The variable "q" 
        determines the order in which the nodes are searched. 
        
        post: The return value should be a list of nodes on the path from 
        "source" to "destination" if one is found. Otherwise, "None" is 
        returned
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
            
        if algo == 'DFS':
            q = Stack()
        elif algo == 'BFS' or algo == "UnweightedSPT":
            q = Queue()
        elif algo == 'Dijkstra':
            q = PriorityQueue()
            for n in self.get_node_list():
                self.set_node_attr(n, 'label', '-')
            self.display()
        elif algo == 'Prim':
            q = PriorityQueue()
            for n in self.get_node_list():
                self.set_node_attr(n, 'label', '-')
            self.display()

        if self.graph_type == 'digraph':
            if reverse:
                neighbors = self.get_in_neighbors
            else:
                neighbors = self.get_out_neighbors
        else:
            neighbors = self.get_neighbors

        nl = self.get_node_list()
        for i in nl:
            self.set_node_attr(i, 'color', 'black')
            for j in neighbors(i):
                if reverse:
                    self.set_edge_attr(j, i, 'color', 'black')
                else:
                    self.set_edge_attr(i, j, 'color', 'black')

        pred = {}
        self.process_edge_search(None, source, pred, q, component, algo, 
                                 **kargs)
        found = True
        if str(source) != str(destination):
            found = False
        while not q.isEmpty() and not found:
            current = q.peek()
            self.process_node_search(current, q)
            self.set_node_attr(current, 'color', 'blue')
            if current != str(source):
                if reverse:
                    self.set_edge_attr(current, pred[current], 'color', 'green')
                else:
                    self.set_edge_attr(pred[current], current, 'color', 'green')
            if current == str(destination):
                found = True
                break
            self.display()
            for n in neighbors(current):
                if self.get_node_attr(n, 'color') != 'green':
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
            self.set_node_attr(current, 'color', 'green')
            self.display()
                    
        if found:
            path = [str(destination)]
            current = str(destination)        
            while current != str(source):
                path.insert(0, pred[current])
                current = pred[current]
            
            #calculate distance lines
            #distance = 0
            #for i in range(len(path)-1):
            #    distance += self.get_edge_attr(path[i],path[i+1],'cost')
            #return distance
            #end of calculate distance lines

            return path

        return pred

    def process_node_search(self, node, q):
        if isinstance(q, PriorityQueue):
            self.set_node_attr(node, 'priority', q.get_priority(node))

    def process_edge_dijkstra(self, current, neighbor, pred, q, component):

        if current is None:
            self.set_node_attr(neighbor, 'color', 'red')
            self.set_node_attr(neighbor, 'label', 0)
            q.push(str(neighbor), 0)
            self.display()
            self.set_node_attr(neighbor, 'color', 'black')
            return
       
        new_estimate = (q.get_priority(str(current)) + 
                        self.get_edge_attr(current, neighbor, 'cost'))
        if neighbor not in pred or new_estimate < q.get_priority(str(neighbor)):
            pred[neighbor] = current
            self.set_node_attr(neighbor, 'color', 'red')
            self.set_node_attr(neighbor, 'label', new_estimate)
            q.push(str(neighbor), new_estimate)
            self.display()
            self.set_node_attr(neighbor, 'color', 'black')

    def process_edge_prim(self, current, neighbor, pred, q, component):

        if current is None:
            self.set_node_attr(neighbor, 'color', 'red')
            self.set_node_attr(neighbor, 'label', 0)
            q.push(str(neighbor), 0)
            self.display()
            self.set_node_attr(neighbor, 'color', 'black')
            return
        
        new_estimate = self.get_edge_attr(current, neighbor, 'cost')
        if not neighbor in pred or new_estimate < q.get_priority(str(neighbor)):
            pred[neighbor] = current
            self.set_node_attr(neighbor, 'color', 'red')
            self.set_node_attr(neighbor, 'label', new_estimate)
            q.push(str(neighbor), new_estimate)
            self.display()
            self.set_node_attr(neighbor, 'color', 'black')

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
                self.set_node_attr(neighbor, 'distance', 0)
            else:                
                self.set_node_attr(neighbor, 'distance',
                                   self.get_node_attr(current, 'distance') + 1)

        if current == None:
            q.push(str(neighbor))
            return
        
        if not neighbor in pred:
            pred[neighbor] = current
            self.set_node_attr(neighbor, 'color', 'red')
            self.display()
            if component != None:
                self.set_component_number(neighbor, component)
                self.set_node_attr(neighbor, 'label', component)
            self.set_node_attr(neighbor, 'color', 'black')
            self.display()
            q.push(str(neighbor))

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
        if display=='pygame':
            self.set_display_mode('pygame')
        if isinstance(source, int):
            source = str(source)
        if isinstance(sink, int):
            sink = str(sink)
        nl = self.get_node_list()
        # set flow of all edges to 0
        for e in self.get_edge_list():
            self.set_edge_attr(e[0], e[1], 'flow', 0)
            capacity = self.get_edge_attr(e[0], e[1], 'capacity')
            self.set_edge_attr(e[0], e[1], 'label', str(capacity)+'/0')
        self.display()
        while True:
            # find an augmenting path from source to sink using DFS
            dfs_stack = []
            dfs_stack.append(source)
            pred = {source:None}
            explored = [source]
            for n in self.get_node_list():
                self.set_node_attr(n, 'color', 'black')
            for e in self.get_edge_list():
                if self.get_edge_attr(e[0], e[1], 'flow') == 0:
                    self.set_edge_attr(e[0], e[1], 'color', 'black')
                elif (self.get_edge_attr(e[0], e[1], 'flow') == 
                      self.get_edge_attr(e[0], e[1], 'capacity')):
                    self.set_edge_attr(e[0], e[1], 'color', 'red')
                else:
                    self.set_edge_attr(e[0], e[1], 'color', 'green')
            self.display()
            while dfs_stack:
                current = dfs_stack.pop()
                if current == sink:
                    break
                out_neighbor = self.get_out_neighbors(current)
                in_neighbor = self.get_in_neighbors(current)
                neighbor = out_neighbor+in_neighbor
                for m in neighbor:
                    if m in explored:
                        continue
                    self.set_node_attr(m, 'color', 'yellow')
                    if m in out_neighbor:
                        self.set_edge_attr(current, m , 'color', 'yellow')
                        available_capacity = (self.get_edge_attr(current, m, 
                                                                 'capacity')-
                                              self.get_edge_attr(current, m, 
                                                                 'flow'))
                    else:
                        self.set_edge_attr(m, current , 'color', 'yellow')
                        available_capacity = self.get_edge_attr(m, current, 
                                                                'flow')
                    self.display()
                    if available_capacity > 0:
                        self.set_node_attr(m, 'color', 'blue')
                        if m in out_neighbor:
                            self.set_edge_attr(current, m, 'color', 'blue')
                        else:
                            self.set_edge_attr(m, current, 'color', 'blue')
                        explored.append(m)
                        pred[m] = current
                        dfs_stack.append(m)
                    else:
                        self.set_node_attr(m, 'color', 'black')
                        if m in out_neighbor:
                            if (self.get_edge_attr(current, m, 'flow') == 
                                self.get_edge_attr(current,m,'capacity')):
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
                                self.set_edge_attr(m, current,'color', 'black')
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
                if self.get_edge(m, current)!=None:
                    arc_capacity = self.get_edge_attr(m, current, 'capacity')
                    flow = self.get_edge_attr(m, current, 'flow')
                    potential = arc_capacity-flow
                    if min_capacity == 'infinite':
                        min_capacity = potential
                    elif min_capacity > potential:
                        min_capacity = potential
                else:
                    potential = self.get_edge_attr(current, m, 'flow')
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
                if self.get_edge(m, current)!=None:
                    flow = self.get_edge_attr(m, current, 'flow')
                    capacity = self.get_edge_attr(m, current, 'capacity')
                    new_flow = flow+min_capacity
                    self.set_edge_attr(m, current, 'flow', new_flow)
                    self.set_edge_attr(m, current, 'label', 
                                       str(capacity)+'/'+str(new_flow))
                    if new_flow==capacity:
                        self.set_edge_attr(m, current, 'color', 'red')
                    else:
                        self.set_edge_attr(m, current, 'color', 'green')
                    self.display()
                else:
                    flow = self.get_edge_attr(current, m, 'flow')
                    capacity = self.get_edge_attr(current, m, 'capacity')
                    new_flow = flow-min_capacity
                    self.set_edge_attr(current, m, 'flow', new_flow)
                    if new_flow==0:
                        self.set_edge_attr(current, m, 'color', 'red')
                    else:
                        self.set_edge_attr(current, m, 'color', 'green')
                    self.display()
                if m == source:
                    break
                current = m

    def max_flow_augment(self, source, sink, display = None, algo = 'SAP'):
        '''
        API: max_flow(self, source, sink, display=None)
        Finds maximum flow from source to sink by a general graph search based 
        augmenting path algorithm. 
        
        pre: Assumes a directed graph in which each arc has a 'capacity' 
        attribute and for which there does does not exist both arcs (i, j) 
        and (j, i) for any pair of nodes i and j.
        inputs:
            source: source node, integer or string
            sink: sink node, integer or string
            display: 
            algo: determines what graph search method to use
                  'SAP' is the shortest augmenting path
                  'DFS' is depth-first search
                  'MaxCap' is the maximum capacity path
       
        post: The 'flow' attribute of each arc gives a maximum flow.
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
        if isinstance(source, int):
            source = str(source)
        if isinstance(sink, int):
            sink = str(sink)
        nl = self.get_node_list()
        # set flow of all edges to 0
        for n in nl:
            for m in self.get_out_neighbors(n):
                if self.get_edge(n, m) != None:
                    self.set_edge_attr(n, m, 'flow', 0)
                    capacity = self.get_edge_attr(n, m, 'capacity')
                    self.set_edge_attr(n, m, 'label', str(capacity)+'/0')
        self.display()
            
        while True:
            self.set_display_mode('off')
            path = self.find_augmenting_path(source, sink, algo = algo)
            self.set_display_mode(display)
            if path is not None:
                self.augment_flow(source, sink, path)
            else:
                return

    def find_augmenting_path(self, source, sink, display = None, q = Stack(),
               algo = 'SAP', **kargs):
        '''
        This method finds an augmenting path in the residual graph from 
        "source" to "sink" using a generalized graph search method. 
        
        post: The return value should be a list of nodes on the path from 
        "source" to "sink" if one is found. Otherwise, "None" is returned.
        '''

        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
            
        if algo == 'DFS':
            q = Stack()
            q.push(str(source))
        elif algo == 'SAP':
            q = Queue()
            q.push(str(source))
        elif algo == 'MaxCap':
            q = PriorityQueue()
            q.push(str(source), 0)

        for i in self.get_node_list():
            self.set_node_attr(i, 'color', 'black')
            if display != 'off':
                for j in self.get_out_neighbors(i):
                    self.set_edge_attr(i, j, 'color', 'black')

        pred = {}
        found = True
        if str(source) != str(sink):
            found = False
        while not q.isEmpty() and not found:
            current = q.peek()
            if algo == 'MaxCap':
                if current != source:
                    current_capacity = -q.get_priority(current)
            if display != 'off':
                self.set_node_attr(current, 'color', 'blue')
            if current != str(source) and display != 'off':
                self.set_edge_attr(pred[current], current, 'color', 'green')
            self.display()
            if current == str(sink):
                found = True
                break
            neighbors = (self.get_out_neighbors(current) + 
                         self.get_in_neighbors(current))
            for n in neighbors:
                if n == source:
                    continue
                if self.get_edge(current, n) is not None:
                    edge = (current, n)
                    mult = 1
                    capacity = self.get_edge_attr(current, n, 'capacity')
                else:
                    edge = (n, current)
                    mult = -1
                    capacity = 0
                flow = mult * self.get_edge_attr(edge[0], edge[1], 'flow')
                residual_capacity = capacity - flow 
                if residual_capacity > 0:
                    if algo == 'DFS' or algo == 'SAP':
                        if not n in pred:
                            pred[n] = current
                            q.push(str(n))
                    elif algo == 'MaxCap':
                        if current != source:
                            if self.get_node_attr(n, 'color') != 'green':
                                capacity_n = q.get_priority(n)
                                if (capacity_n is None or 
                                    (min(residual_capacity, current_capacity) 
                                     > -capacity_n)):
                                    q.push(str(n), max(-residual_capacity, 
                                                        -current_capacity))
                                    pred[n] = current
                        else:
                            q.push(str(n), -residual_capacity)
                            pred[n] = current
                    if display != 'off':
                        self.set_edge_attr(edge[0], edge[1], 'color', 'yellow')
                        self.display()
                        self.set_node_attr(n, 'color', 'red')
                        self.display()
                        self.set_node_attr(n, 'color', 'black')
                        self.display()
                        self.set_edge_attr(edge[0], edge[1], 'color', 'black')
            q.remove(current)
            self.set_node_attr(current, 'color', 'green')
            if display != 'off':
                self.display()
                    
        if found:
            path = [str(sink)]
            current = str(sink)        
            while current != str(source):
                path.insert(0, pred[current])
                current = pred[current]
        else:
            path = None

        return path

    def augment_flow(self, source, sink, path): 
        min_capacity = None
        current = path[0]
        for m in path[1:]:
            if self.get_edge(current, m) is not None:
                residual_capacity = (self.get_edge_attr(current,m,'capacity') -
                    self.get_edge_attr(current, m, 'flow')) 
            else:                            
                residual_capacity = self.get_edge_attr(m, current, 'flow')
            if min_capacity is None:
                min_capacity = residual_capacity
            elif min_capacity > residual_capacity:
                min_capacity = residual_capacity
            current = m
            # update flows on the path
        current = path[0]
        for m in path[1:]:
            if self.get_edge(current, m) is not None:
                edge = (current, m)
                mult = 1
            else:
                edge = (m, current)
                mult = -1
            flow = self.get_edge_attr(edge[0], edge[1], 'flow')
            capacity = self.get_edge_attr(edge[0], edge[1], 'capacity')
            new_flow = flow + mult * min_capacity
            self.set_edge_attr(edge[0], edge[1], 'flow', new_flow)
            self.set_edge_attr(edge[0], edge[1], 'label', 
                               str(capacity)+'/'+str(new_flow))
            self.set_edge_attr(edge[0], edge[1], 'color', 'yellow')
            self.display()
            if new_flow == capacity:
                self.set_edge_attr(edge[0], edge[1], 'color', 'red')
            elif new_flow == 0:
                self.set_edge_attr(edge[0], edge[1], 'color', 'black')
            else:
                self.set_edge_attr(edge[0], edge[1], 'color', 'green')
            current = m
        return

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
            display = self.display_mode
        else:
            self.set_display_mode(display)
        if isinstance(source, int):
            source = str(source)
        if isinstance(sink, int):
            sink = str(sink)
        nl = self.get_node_list()
        # set flow of all edges to 0
        for n in nl:
            self.set_node_attr(n, 'excess', 0)
            for m in self.get_out_neighbors(n):
                if self.get_edge(n, m) != None:
                    self.set_edge_attr(n, m, 'flow', 0)
                    capacity = self.get_edge_attr(n, m, 'capacity')
                    self.set_edge_attr(n, m, 'label', str(capacity)+'/0')
        self.display()

        self.set_display_mode('off')
        self.search(sink, algo = 'UnweightedSPT', reverse = True)
        self.set_display_mode(display)
        
        disconnect = False
        for n in nl:
            if self.get_node_attr(n, 'distance') is None:
                disconnect = True
                self.set_node_attr(n, 'distance',
                                   2*len(self.get_node_list()) + 1)
        if disconnect:
            print 'Warning: graph contains nodes not connected to the sink...'

        if algo == 'FIFO':
            q = Queue()
        elif algo == 'SAP':
            q = Stack()
        elif algo == 'HighestLabel':
            q = PriorityQueue()
        for n in self.get_out_neighbors(source):
            capacity = self.get_edge_attr(source, n, 'capacity')
            self.set_edge_attr(source, n, 'flow', capacity)
            self.set_node_attr(n, 'excess', capacity)
            excess = self.get_node_attr(source, 'excess')
            self.set_node_attr(source, 'excess', excess - capacity)
            if algo == 'FIFO' or algo == 'SAP':
                q.push(n)
            elif algo == 'HighestLabel':
                q.push(n, -1)
        self.set_node_attr(source, 'distance', len(self.get_node_list()))
        self.show_flow()

        while not q.isEmpty():
            # debug stuff
            print "node_id excess distance"
            nl = self.get_node_list()
            nl.sort()
            for n in nl:
                print n.ljust(6), \
                    str(self.get_node_attr(n,'excess')).ljust(6), \
                    self.get_node_attr(n,'distance')

            # end of debug stuff
            relabel = True
            current = q.peek()
            neighbors = (self.get_out_neighbors(current) + 
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
        if self.get_edge(i, j) is not None:
            edge = (i, j)
            capacity = self.get_edge_attr(i, j, 'capacity')
            mult = 1
        else:
            edge = (j, i)
            capacity = 0
            mult = -1
        flow = mult*self.get_edge_attr(edge[0], edge[1], 'flow')
        residual_capacity = capacity - flow
        if residual_capacity == 0:
            return False
        excess_i = self.get_node_attr(i, 'excess')
        excess_j = self.get_node_attr(j, 'excess')
        push_amount = min(excess_i, residual_capacity)
        self.set_edge_attr(edge[0], edge[1], 'flow',  mult*(flow + push_amount))
        self.set_node_attr(i, 'excess', excess_i - push_amount)
        self.set_node_attr(j, 'excess', excess_j + push_amount)
        return True

    def relabel(self, i):
        min_distance = 2*len(self.get_node_list()) + 1
        for j in self.get_out_neighbors(i):
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
            for neighbor in self.get_out_neighbors(n):
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

    def random(self, numnodes = 10, degree_range = None, length_range = None,
               density = None, edge_format = None, node_format = None, 
               Euclidean = False, seedInput = None):
        if seedInput is not None:
            seed(seedInput)
        seed(seedInput)
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
                    for i in range(randint(degree_range[0], degree_range[1])):
                        n = randint(1, numnodes)
                        if not self.get_edge(m, n) and m != n:
                            if length_range is not None:
                                length = randint(length_range[0], 
                                                 length_range[1])
                                self.add_edge(m, n, cost = length, 
                                              label = str(length), 
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            if density != None:
                for m in range(numnodes):
                    if self.graph_type == 'digraph':
                        numnodes2 = numnodes
                    else:
                        numnodes2 = m
                    for n in range(numnodes2):
                        if random() < density and m != n:
                            if length_range is not None:
                                length = randint(length_range[0], 
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
                self.add_node(m, locationx = randint(1, 20), 
                              locationy = randint(1, 20), **node_format)
            if degree_range is not None:
                for m in range(numnodes):
                    for i in range(randint(degree_range[0], degree_range[1])):
                        n = randint(1, numnodes)
                        if not self.get_edge(m, n) and m != n:
                            if length_range is None:
                                ''' calculates the euclidean norm and round it 
                                to three decimal places '''
                                length = round((((self.get_node_attr(n, 'locationx') - self.get_node_attr(m, 'locationx')) ** 2 + (self.get_node_attr(n, 'locationy') - self.get_node_attr(m, 'locationy')) ** 2) ** 0.5), 3) 
                                self.add_edge(m, n, cost = length, 
                                             label = str(length), 
                                              **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            if density != None:
                for m in range(numnodes):
                    if self.type == 'digraph':
                        numnodes2 = numnodes
                    else:
                        numnodes2 = m
                    for n in range(numnodes2):
                        if random() < density:
                            if length_range is None:
                                ''' calculates the euclidean norm and round it 
                                to three decimal places '''
                                length = round((((self.get_node_attr(n, 'locationx') - self.get_node_attr(m, 'locationx')) ** 2 + (self.get_node_attr(n, 'locationy') - self.get_node_attr(m, 'locationy')) ** 2) ** 0.5), 3) 
                                self.add_edge(m, n, cost = length, 
                                             label = str(length), 
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
                             len(self.get_out_neighbors(referring_page)))
                
                diff += abs(pagerank[node] - rank)
                pagerank[node] = rank
        
            #stop if PageRank has converged
            if diff < min_delta:
                break
    
            return pagerank            
    def get_degree(self):
        dd = {}
        if self.graph_type == 'graph':
            for n in self.get_node_list():
                dd[n] = len(self.get_neighbors(n))
        elif self.graph_type == 'digraph':
            for n in self.get_node_list():
                dd[n] = (len(self.get_in_neighbors(n)) + 
                         len(self.get_out_neighbors(n)))
        return dd 

    def get_diameter(self):
        dist = 0
        for n in self.get_node_list():
            for m in self.get_node_list():
                ndist = self.shortest_unweighted_path(n, m)
                if isinstance(ndist, dict):
                    continue
                ndist = len(ndist)-1
                if ndist > dist:
                    dist = ndist
        return dist

    def set_display_mode(self, display):
        if display == 'pygame':
            if pygame_installed:
                if self.display_mode == 'off':
                    init()
                self.display_mode = display
            else:
                print "Pygame module not found, graphical display disabled"
        else:
            self.display_mode = display
        
    def display(self, highlight = None, filename = 'graph.png', format = 'png',
                pause = True):
        if self.display_mode == 'off':
            return
        if highlight != None:
            for n in highlight:
                if not isinstance(n, Node):
                    m = self.get_node(n)
                m.set('color', 'red')    
        if self.display_mode == 'file':
            self.write(filename, self.get_layout(), format)
            return
        elif self.get_layout() != 'bak':
            im = StringIO(self.create(self.get_layout(), format))
        else:
            im = StringIO(self.GenerateTreeImage())
        if highlight != None:
            for n in highlight:
                if not isinstance(n, Node):
                    m = self.get_node(n)
                m.set('color', 'black')
        if self.display_mode == 'pygame':
            picture = image.load(im, format)
            screen = display.set_mode(picture.get_size())
            screen.blit(picture, picture.get_rect())
            display.flip()
            while pause:
                e = event.poll()
                if e.type == KEYDOWN:
                    break
                if e.type == QUIT:
                    sys.exit()
        elif self.display_mode == 'PIL':
            if PIL_installed:
                im2 = Image.open(im)
                im2.show()
            else:
                print 'Error: PIL not installed. Display disabled.'
                self.display_mode = 'off'
        elif self.display_mode == 'xdot':
            if xdot_installed:
                window = xdot.DotWindow()
                window.set_dotcode(self.to_string())
                window.show()
                gtk.main()
            else:
                print 'Error: xdot not installed. Display disabled.'
                self.display_mode = 'off'
        else:
            print "Unknown display mode: ",
            print self.display_mode
        
    def exit_window(self):
        if self.display_mode != 'pygame':
            return
        while True:
            e = event.wait()
            if e.type == QUIT:
                break

    def add_subgraph(self, S):
        Dot.add_subgraph(self, S)

    def network_simplex(self, display, pivot):
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
        t.simplex_redraw(display)
        t.set_display_mode(display)
        #t.display()
        self.display()
        # set predecessor, depth and thread indexes
        t.simplex_search('1', 1)
        # compute potentials
        self.simplex_compute_potentials(t)
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
            t.simplex_redraw(display)
            #t.display()
            t.simplex_search('1', 1)
            # compute potentials
            self.simplex_compute_potentials(t)
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
                flow = self.get_edge_attr(cycle[index], cycle[index+1], 'flow')
                capacity = self.get_edge_attr(cycle[index], cycle[index+1],
                                           'capacity')
                if min_capacity >= (capacity-flow):
                    candidate = (cycle[index], cycle[index+1])
                    min_capacity = capacity-flow
            else:
                flow = self.get_edge_attr(cycle[index+1], cycle[index], 'flow')
                if min_capacity >= flow:
                    candidate = (cycle[index+1], cycle[index])
                    min_capacity = flow
            index += 1
        # check arc (cycle[n-1], cycle[0])
        if (cycle[n-1], cycle[0]) in tel:
            flow = self.get_edge_attr(cycle[n-1], cycle[0], 'flow')
            capacity = self.get_edge_attr(cycle[n-1], cycle[0],
                                       'capacity')
            if min_capacity >= (capacity-flow):
                candidate = (cycle[n-1], cycle[0])
                min_capacity = capacity-flow
        else:
            flow = self.get_edge_attr(cycle[0], cycle[n-1], 'flow')
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
        tel = t.get_edge_list()
        for e in self.get_edge_list():
            flow_e = self.get_edge_attr(e[0], e[1], 'flow')
            capacity_e = self.get_edge_attr(e[0], e[1], 'capacity')
            if e in tel:
                if flow_e == 0:
                    self.set_edge_attr(e[0], e[1], 'color', 'blue')
                elif flow_e == capacity_e:
                    self.set_edge_attr(e[0], e[1], 'color', 'blue')
                else:
                    self.set_edge_attr(e[0], e[1], 'color', 'blue')
            else:
                if flow_e == 0:
                    self.set_edge_attr(e[0], e[1], 'color', 'black')
                elif flow_e == capacity_e:
                    self.set_edge_attr(e[0], e[1], 'color', 'black')
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
        for e in self.get_edge_list():
            if self.get_edge_attr(e[0],e[1],'flow')!=0:
                print e, str(self.get_edge_attr(e[0],e[1],'flow')).ljust(4),
                print str(self.get_edge_attr(e[0],e[1],'capacity')).ljust(4)

    def simplex_redraw(self, display):
        '''
        API:
            simplex_redraw(self, display)
        Description:
            Returns a new graph instance that is same as self but adds nodes
            and arcs in a way that the resulting tree will be displayed
            properly.
        Pre:
            (1) Assumes a node with name 1 exists.
        Inputs:
            display: display mode
        Return:
            Returns a graph same as self.
        '''
        nl = self.get_node_list()
        el = self.get_edge_list()
        new = self.__class__(graph_type='digraph', layout='dot',
                             display=display)
        pred_i = self.get_node_attr('1', 'pred')
        thread_i = self.get_node_attr('1', 'thread')
        depth_i = self.get_node_attr('1', 'depth')
        new.add_node('1', pred=pred_i, thread=thread_i, depth=depth_i)
        q = ['1']
        visited = ['1']
        while q:
            name = q.pop()
            visited.append(name)
            neighbors = self.get_in_neighbors(name) +\
                        self.get_out_neighbors(name)
            for n in neighbors:
                if n not in new.get_node_list():
                    pred_i = self.get_node_attr(n, 'pred')
                    thread_i = self.get_node_attr(n, 'thread')
                    depth_i = self.get_node_attr(n, 'depth')
                    new.add_node(n, pred=pred_i, thread=thread_i, depth=depth_i)
                if (name,n) in el:
                    if new.get_edge(name,n) is None:
                        new.add_edge(name,n)
                else:
                    if new.get_edge(n,name) is None:
                        new.add_edge(n,name)
                if n not in visited:
                    q.append(n)
        for e in el:
            flow = self.get_edge_attr(e[0], e[1], 'flow')
            capacity = self.get_edge_attr(e[0], e[1], 'capacity')
            cost = self.get_edge_attr(e[0], e[1], 'cost')
            new.set_edge_attr(e[0], e[1], 'flow', flow)
            new.set_edge_attr(e[0], e[1], 'capacity', capacity)
            new.set_edge_attr(e[0], e[1], 'cost', cost)
            new.set_edge_attr(e[0], e[1], 'label',
                                     "%d/%d/%d" %(flow,capacity,cost))
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
        tel = t.get_edge_list()
        index = 0
        while index < (n-1):
            if (cycle[index], cycle[index+1]) in tel:
                flow_e = self.get_edge_attr(cycle[index], cycle[index+1],
                                            'flow')
                self.set_edge_attr(cycle[index], cycle[index+1], 'flow',
                                   flow_e+min_capacity)
            else:
                flow_e = self.get_edge_attr(cycle[index+1], cycle[index],
                                            'flow')
                self.set_edge_attr(cycle[index+1], cycle[index], 'flow',
                                   flow_e-min_capacity)
            index += 1
        # augment arc cycle[n-1], cycle[0]
        if (cycle[n-1], cycle[0]) in tel:
            flow_e = self.get_edge_attr(cycle[n-1], cycle[0], 'flow')
            self.set_edge_attr(cycle[n-1], cycle[0], 'flow',
                               flow_e+min_capacity)
        else:
            flow_e = self.get_edge_attr(cycle[0], cycle[n-1], 'flow')
            self.set_edge_attr(cycle[0], cycle[n-1], 'flow',
                               flow_e-min_capacity)
        # remove leaving arc
        t.del_edge(p, q)
        # set label of removed arc
        flow_pq = self.get_edge_attr(p, q, 'flow')
        capacity_pq = self.get_edge_attr(p, q, 'capacity')
        cost_pq = self.get_edge_attr(p, q, 'cost')
        self.set_edge_attr(p, q, 'label',
                                     "%d/%d/%d" %(flow_pq,capacity_pq,cost_pq))
        for e in t.get_edge_list():
            flow = self.get_edge_attr(e[0], e[1], 'flow')
            capacity = self.get_edge_attr(e[0], e[1], 'capacity')
            cost = self.get_edge_attr(e[0], e[1], 'cost')
            t.set_edge_attr(e[0], e[1], 'flow', flow)
            t.set_edge_attr(e[0], e[1], 'capacity', capacity)
            t.set_edge_attr(e[0], e[1], 'cost', cost)
            t.set_edge_attr(e[0], e[1], 'label',
                                     "%d/%d/%d" %(flow,capacity,cost))
            self.set_edge_attr(e[0], e[1], 'label',
                                     "%d/%d/%d" %(flow,capacity,cost))


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
            for e in self.get_edge_list():
                if e in t.get_edge_list():
                    continue
                flow_ij = self.get_edge_attr(e[0], e[1], 'flow')
                potential_i = self.get_node_attr(e[0], 'potential')
                potential_j = self.get_node_attr(e[1], 'potential')
                capacity_ij = self.get_edge_attr(e[0], e[1], 'capacity')
                c_ij = self.get_edge_attr(e[0], e[1], 'cost')
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
            for e in self.get_edge_list():
                if e in t.get_edge_list():
                    continue
                flow_ij = self.get_edge_attr(e[0], e[1], 'flow')
                potential_i = self.get_node_attr(e[0], 'potential')
                potential_j = self.get_node_attr(e[1], 'potential')
                capacity_ij = self.get_edge_attr(e[0], e[1], 'capacity')
                c_ij = self.get_edge_attr(e[0], e[1], 'cost')
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
        for e in self.get_edge_list():
            if e in t.get_edge_list():
                continue
            flow_ij = self.get_edge_attr(e[0], e[1], 'flow')
            potential_i = self.get_node_attr(e[0], 'potential')
            potential_j = self.get_node_attr(e[1], 'potential')
            capacity_ij = self.get_edge_attr(e[0], e[1], 'capacity')
            c_ij = self.get_edge_attr(e[0], e[1], 'cost')
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
        for e in self.get_edge_list():
            flow = self.get_edge_attr(e[0], e[1], 'flow')
            capacity = self.get_edge_attr(e[0], e[1], 'capacity')
            cost = self.get_edge_attr(e[0], e[1], 'cost')
            self.set_edge_attr(e[0], e[1], 'label',
                                     "%d/%d/%d" %(flow,capacity,cost))
            if e in solution_g.get_edge_list():
                solution_g.set_edge_attr(e[0], e[1], 'flow', flow)
                solution_g.set_edge_attr(e[0], e[1], 'capacity', capacity)
                solution_g.set_edge_attr(e[0], e[1], 'cost', cost)
                solution_g.set_edge_attr(e[0], e[1], 'label',
                                         "%d/%d/%d" %(flow,capacity,cost))
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
            if solution_g.get_node_attr(n, 'component') != current:
                # find an arc from n to seperated
                for m in separated:
                    if self.get_edge(n,m) is not None:
                        solution_g.add_edge(n,m)
                        return True
                    elif self.get_edge(m,n) is not None:
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
        for n in self.get_node_list():
            self.set_node_attr(n, 'component', None)
        while q:
            current = q.pop()
            self.set_node_attr(current, 'component', component_nr)
            sequence.append(current)
            neighbors = self.get_in_neighbors(current)+\
                        self.get_out_neighbors(current)
            for n in neighbors:
                if n in pred:
                    continue
                self.set_node_attr(n, 'component', component_nr)
                pred[n] = current
                depth[n] = depth[current]+1
                q.append(n)
        for i in range(len(sequence)-1):
            self.set_node_attr(sequence[i], 'thread', int(sequence[i+1]))
        self.set_node_attr(sequence[-1], 'thread', int(sequence[0]))
        for n in pred:
            self.set_node_attr(n, 'pred', pred[n])
            self.set_node_attr(n, 'depth', depth[n])
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
        el = self.get_edge_list()
        # check arc (cycle[k-1], cycle[0])
        if (cycle[k-1], cycle[0]) in el:
            min_capacity = self.get_edge_attr(cycle[k-1], cycle[0], 'capacity')-\
                              self.get_edge_attr(cycle[k-1], cycle[0], 'flow')
        else:
            min_capacity = self.get_edge_attr(cycle[0], cycle[k-1], 'flow')
        # check rest of the arcs in the cycle
        while index<(k-1):
            i = cycle[index]
            j = cycle[index+1]
            if (i,j) in el:
                capacity_ij = self.get_edge_attr(i, j, 'capacity') -\
                              self.get_edge_attr(i, j, 'flow')
            else:
                capacity_ij = self.get_edge_attr(j, i, 'flow')
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
            self.set_node_attr(n, 'component', None)
        component_nr = int(nl[0])
        self.set_node_attr(nl[0], 'component', component_nr)
        while True:
            while q:
                current = q.pop()
                visited.append(current)
                neighbors = self.get_in_neighbors(current) +\
                    self.get_out_neighbors(current)
                for n in neighbors:
                    if n==pred[current]:
                        continue
                    self.set_node_attr(n, 'component', component_nr)
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
                if self.get_node_attr(n, 'component') is None:
                    q.append(n)
                    depth = {n:0}
                    pred = {n:None}
                    visited = []
                    component_nr = int(n)
                    self.set_node_attr(n, 'component', component_nr)
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
        simplex_g = self.__class__(graph_type='digraph')
        for e in self.get_edge_list():
            flow_e = self.get_edge_attr(e[0], e[1], 'flow')
            capacity_e = self.get_edge_attr(e[0], e[1], 'capacity')
            if flow_e>0 and flow_e<capacity_e:
                simplex_g.add_edge(e[0], e[1])
            for i in self.get_node_list():
                if i in simplex_g.get_node_list():
                    continue
                else:
                    simplex_g.add_node(i)
        return simplex_g

    def simplex_compute_potentials(self, t):
        '''
        API:
            simplex_compute_potentials(self)
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
        Post:
            Keeps the node potentials as 'potential' attribute.
        '''
        self.set_node_attr(1, 'potential', 0)
        j = t.get_node_attr(1, 'thread')
        while j is not 1:
            i = t.get_node_attr(j, 'pred')
            potential_i = self.get_node_attr(i,'potential')
            if (str(i),str(j)) in self.get_edge_list():
                c_ij = self.get_edge_attr(i, j, 'cost')
                self.set_node_attr(j, 'potential', potential_i - c_ij)
            if (str(j),str(i)) in self.get_edge_list():
                c_ji = self.get_edge_attr(j, i, 'cost')
                self.set_node_attr(j, 'potential', potential_i + c_ji)
            j = t.get_node_attr(j, 'thread')

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
            depth_i = t.get_node_attr(i, 'depth')
            depth_j = t.get_node_attr(j, 'depth')
            if depth_i > depth_j:
                i = t.get_node_attr(i, 'pred')
                li.append(i)
            elif depth_i < depth_j:
                j = t.get_node_attr(j, 'pred')
                lj.append(j)
            else:
                i = t.get_node_attr(i, 'pred')
                li.append(i)
                j = t.get_node_attr(j, 'pred')
                lj.append(j)
        cycle.extend(lj)
        li.pop()
        li.reverse()
        cycle.extend(li)
        # l is beginning k is end
        return cycle

    def cycle_canceling(self, display):
        '''
        API:
            cycle_canceling(self, display)
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
        Inputs:
            display: 'off' for no display, 'pygame' for live update.
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
            # display cycle
            if self.display_mode is not 'off':
                self.paint_cycle(ncycle)
                self.relabel()
                self.display()
            # find capacity of cycle
            cap = residual_g.find_cycle_capacity(ncycle)
            # augment capacity amount along the cycle
            self.augment_cycle(cap, ncycle)
            if self.display_mode is not 'off':
                # set labels for display purposes
                self.relabel()
                self.display()
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
        for i in self.get_node_list():
            b_i = self.get_node_attr(i, 'demand')
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
        for i in self.get_out_neighbors('s'):
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
        self.set_node_attr(source, 'distance', 0)
        pred[source] = None
        for n in self.get_node_list():
            if n!=source:
                self.set_node_attr(n, 'distance', 'inf')
        q = [source]
        while q:
            i = q[0]
            q = q[1:]
            for j in self.get_out_neighbors(i):
                distance_j = self.get_node_attr(j, 'distance')
                distance_i = self.get_node_attr(i, 'distance')
                c_ij = self.get_edge_attr(i, j, 'cost')
                if distance_j > distance_i + c_ij:
                    self.set_node_attr(j, 'distance', distance_i+c_ij)
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
        for n in self.get_node_list():
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

    def paint_cycle(self, cycle):
        '''
        API:
            paint_cycle(self)
        Description:
            Changes colors of the arcs in the cycle
        Post:
            'color' attributes of arcs in the cycle will be changed.
        '''
        index = 0
        k = len(cycle)
        while index<(k-1):
            i = cycle[index]
            j = cycle[index+1]
            if (str(i),str(j)) in self.get_edge_list():
                self.set_edge_attr(i, j, 'color', 'red')
            else:
                self.set_edge_attr(j, i, 'color', 'red')
            index += 1

    def relabel(self):
        '''
        API:
            relabel(self)
        Description:
            Updates label attributes of edges to cost/flow/capacity
        Pre:
            (1) Arcs should have 'cost', 'flow' and 'capacity' attributes
        Post:
            Changes 'label' attributes of arcs.
        '''
        for e in self.get_edge_list():
            cost = self.get_edge_attr(e[0], e[1], 'cost')
            flow = self.get_edge_attr(e[0], e[1], 'flow')
            capacity = self.get_edge_attr(e[0], e[1], 'capacity')
            self.set_edge_attr(e[0], e[1], 'label', '%d/%d/%d'
                               %(cost, flow, capacity))

    #TODO(aykut): this is a game changer, all algorithms that depend on
    # residual graph can be better implemented using this method. Create
    # residual graph and use existing search/traverse methods on residual graph
    # instance created.
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
        if self.graph_type=='graph':
            raise 'residual graph is defined for directed graphs.'
        residual_g = self.__class__(graph_type = 'digraph')
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
            if (str(i),str(j)) in self.get_edge_list():
                flow_ij = self.get_edge_attr(i, j, 'flow')
                self.set_edge_attr(i, j, 'flow', flow_ij+amount)
            else:
                flow_ji = self.get_edge_attr(j, i, 'flow')
                self.set_edge_attr(j, i, 'flow', flow_ji-amount)
            index += 1
        i = cycle[k-1]
        j = cycle[0]
        if (str(i),str(j)) in self.get_edge_list():
            flow_ij = self.get_edge_attr(i, j, 'flow')
            self.set_edge_attr(i, j, 'flow', flow_ij+amount)
        else:
            flow_ji = self.get_edge_attr(j, i, 'flow')
            self.set_edge_attr(j, i, 'flow', flow_ji-amount)


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
            (3) Node names should be integers starting from 1. 1 will be the
            root node (required for simplex algorithm).
            (4) The graph should be connected.
            (5) Assumes (i,j) and (j,i) does not exist together. Needed when
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
            algorithm = 'simlex'
        if algorithm is 'simplex':
            if 'pivot' in args:
                if not self.network_simplex(display, args['pivot']):
                    print 'problem is infeasible'
            else:
                if not self.network_simplex(display, 'dantzig'):
                    print 'problem is infeasible'
        elif algorithm is 'cycle_canceling':
            if not self.cycle_canceling(display):
                print 'problem is infeasible'
        else:
            print args['algo'], 'is not a defined algorithm. Exiting.'
            return


class Subgraph(Dotsubgraph, Graph):
    
    def __init__(self, display = 'off', type = 'digraph', **attrs):
        self.display_mode = display
        self.graph_type = type
        self.num_components = None
        if self.graph_type == 'digraph':
            self.in_neighbor_lists = {}
            self.out_neighbor_lists = {}
        else:
            self.neighbor_lists = {}
        if display == 'pygame':
            if pygame_installed:
                init()
            else:
                print "Pygame module not installed, graphical display disabled"
        Dotsubgraph.__init__(self, **attrs)
        attrs['graph_type'] = 'subgraph'

class Cluster(Dotcluster, Graph):
    
    def __init__(self, display = 'off', type = 'digraph', **attrs):
        self.display_mode = display
        self.graph_type = type
        self.num_components = None
        if self.graph_type == 'digraph':
            self.in_neighbor_lists = {}
            self.out_neighbor_lists = {}
        else:
            self.neighbor_lists = {}
        if display == 'pygame':
            if pygame_installed:
                init()
            else:
                print "Pygame module not installed, graphical display disabled"
        Dotcluster.__init__(self, **attrs)
        attrs['graph_type'] = 'subgraph'

class Tree(Graph):
    
    def __init__(self, display = 'off', **attrs):
        attrs['graph_type'] = 'digraph'
        if 'layout' not in attrs:
            attrs['layout'] = 'dot'
        Graph.__init__(self, display, **attrs)
        self.root = None
        
    def get_children(self, n):
        return self.get_out_neighbors(n)

    def get_parent(self, n):
        return self.get_node_attr(n, 'parent')
        
    def add_root(self, root, **attrs):
        attrs['level'] = 0
        self.add_node(root, **attrs)
        self.root = root
        
    def add_child(self, n, parent, **attrs):
        attrs['level'] = self.get_node_attr(parent, 'level') + 1
        attrs['parent'] = str(parent)
        self.add_node(n, **attrs)
        self.add_edge(parent, n)
            
    def dfs(self, root = None, display = 'dot'):
        if root == None:
            root = self.root
        self.traverse(root, display, Stack())

    def bfs(self, root = None, display = 'dot'):
        if root == None:
            root = self.root
        self.traverse(root, display, Queue())

    def traverse(self, display = 'dot', root = None, q = Stack()):
        if root == None:
            root = self.root
        if isinstance(q, Queue):
            addToQ = q.enqueue
            removeFromQ = q.dequeue
        elif isinstance(q, Stack):
            addToQ = q.push
            removeFromQ = q.pop
    
        addToQ(root)
#        while not q.isEmpty():
        while not q.empty():
            current = removeFromQ()
            print current
            if display:
                current.set('color', 'red')
                self.display()
                current.set('color', '')
            for n in self.get_children(current):
                addToQ(n)
                
    def write_as_svg(self, filename, prevfile = None, nextfile = None, 
                     mode = 'Dot', highlight = None, label_attr = None, 
                     tooltip_attr = None):
        if not etree_installed:
            print 'Etree not installed. Exiting.'
            return
        if highlight != None:
            if not isinstance(highlight, Node):
                highlight = self.get_node(highlight)
            highlight.set('color', 'red')    
        if mode == 'Dot':
            node_names = self.get_node_list()
            edge_names = self.get_edge_list()
            for name in node_names:
                node = self.get_node(name)
                if tooltip_attr is None:
                  node.set_tooltip(str(node.get_label()))
                else:
                  node.set_tooltip(str(node.get(tooltip_attr)))  
                if label_attr is not None:
                  node_label = node.get(label_attr)
                  node.set("label", node_label)
                node.set_style('"filled"')
                node.set_fillcolor('"white"')
            for (m_name, n_name) in edge_names:
                edge = self.get_edge(m_name, n_name)
                edge.set_edgetooltip('"Arc"')

            try:
                
                svgGraph = self.create('dot', 'svg')
                svgText = StringIO(svgGraph)
                svgParsed = etree.parse(svgText)
                svgRoot = svgParsed.getroot()
                
                widthStr = svgRoot.get("width")
                try:
                    width = int(widthStr)
                except:
                    try:
                        width = int(widthStr[:-2])
                    except:
                        raise Exception("Could not parse SVG width")
                
                xlinkPrefix = svgRoot.nsmap['xlink']
                
                if not (prevfile is None):
                    prevg = etree.XML('<g id="prev" class="nav-link"></g>')
                    svgRoot.append(prevg)
                    prevlink = etree.SubElement(prevg, "a")
                    prevlink.set("{%s}href" % xlinkPrefix, prevfile + ".svg")
                    prevtext = etree.SubElement(prevlink, "text", x="5", y="15")
                    prevtext.text = "Prev"
##                    print etree.tostring(prevg, pretty_print=True)
                    
                if not (nextfile is None):
                    nextg = etree.XML('<g id="next" class="nav-link"></g>')
                    svgRoot.append(nextg)
                    nextlink = etree.SubElement(nextg, "a")
                    nextlink.set("{%s}href" % xlinkPrefix, nextfile + ".svg")
                    nexttext = etree.SubElement(nextlink, "text", 
                                                x="%s" % (width - 5 - 20), 
                                                y="15") # -20 for width of Next
                    nexttext.text = "Next"
##                    print etree.tostring(nextg, pretty_print=True)
                    
##                print etree.tostring(svgParsed.getroot())
                svgParsed.write(filename + ".svg")
                
            except Exception as e:
                print e
        else:
            raise Exception("Only Dot mode supported in write_as_svg")
            print "No .svg file created"

        if highlight != None:
            highlight.set('color', 'black')    
        
    def write_as_dot(self, filename, mode = 'Dot', highlight = None):
        if highlight != None:
            if not isinstance(highlight, Node):
                highlight = self.get_node(highlight)
            highlight.set('color', 'red')    
        if mode == 'Dot':
            node_names = self.get_node_list()
            edge_names = self.get_edge_list()
            for name in node_names:
                node = self.get_node(name)
                node.set_tooltip('%s' % node.get_label())
                node.set_style('"filled"')
                node.set_fillcolor('"white"')
            for (m_name, n_name) in edge_names:
                edge = self.get_edge(m_name, n_name)
                edge.set_edgetooltip('"Arc"')

            try:
                
                self.write_raw(filename + ".dot")
                
            except Exception as e:
                print e
        else:
            raise Exception("Only Dot mode supported in write_as_dot")
            print "No .dot file created"
            
        if highlight != None:
            highlight.set('color', 'black')
        
class BinaryTree(Tree):

    def __init__(self, display = 'off', **attrs):
        Tree.__init__(self, display, **attrs)

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
                
    def print_nodes(self, order = 'in', priority = 'L', display = None, 
                    root = None):
        if root == None:
            root = self.root
        if display == None:
            display = self.display_mode
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
            display = self.display_mode
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
            print current                
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
            display = self.display_mode
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
            display = self.display_mode
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
           
    
class DisjointSet(Graph):
    
    def __init__(self, optimize = True, **attrs):
        attrs['graph_type'] = 'digraph'
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
        while len(self.get_out_neighbors(current)) != 0:
            successor = self.get_out_neighbors(current)[0]
            edge_list.append((current, successor))
            current = successor
        if self.optimize:
            for e in edge_list:
                if e[1] != current:
                    self.del_edge(e[0], e[1])                   
                    self.add_edge(e[0], current)
        return current

class BBTree(BinaryTree):
    
    def __init__(self, display = False, **attrs):
        BinaryTree.__init__(self, display, **attrs)

    def write_as_dynamic_gexf(self, filename, mode = "Dot"):
        if not gexf_installed:
            print 'Gexf not installed. Exiting.'
            return
        if mode == 'Dot':
            try:
                
                gexf = Gexf("Mike O'Sullivan", "Dynamic graph file")
                graph = gexf.addGraph("directed", "dynamic", "Dynamic graph")
                objAtt = graph.addNodeAttribute("obj", "0.0", "float")
                currAtt = graph.addNodeAttribute("current", "1.0", 
                                                 "integer", "dynamic") 
                
                node_names = self.get_node_list()
                for name in node_names:
                    node = self.get_node(name)
                    step = node.get_label()
                    next = "%s" % (atoi(step) + 1)
                    n = graph.addNode(node.get_label(), node.get_label(), 
                                      start=step)

                    if node.get("obj") is None:
                        raise Exception("Node without objective in BBTree", 
                                        "node =", node)
                    
                    n.addAttribute(objAtt, "%s" % node.get("obj"))
                    n.addAttribute(currAtt, "1", start=step, end=next)
                    n.addAttribute(currAtt, "0", start=next)
                edge_names = self.get_edge_list()
                for i, (m_name, n_name) in enumerate(edge_names):
                    edge = self.get_edge(m_name, n_name)
                    graph.addEdge(i, edge.get_source(), edge.get_destination(),
                                  start=edge.get_destination())
                output_file = open(filename + ".gexf", "w")
                gexf.write(output_file)
                
            except Exception as e:
                print e
                print "No .gexf file created"
        else:
            raise Exception("Only Dot mode supported in write_bb_as_gexf")

class BBTree(BinaryTree):
    
    def __init__(self, display = False, **attrs):
        BinaryTree.__init__(self, display, **attrs)

    def write_as_dynamic_gexf(self, filename, mode = "Dot"):
        if mode == 'Dot':
            try:
                
                gexf = Gexf("Mike O'Sullivan", "Dynamic graph file")
                graph = gexf.addGraph("directed", "dynamic", "Dynamic graph")
                objAtt = graph.addNodeAttribute("obj", "0.0", "float")
                currAtt = graph.addNodeAttribute("current", "1.0", "integer", "dynamic")
                
                node_names = self.get_node_list()
                for name in node_names:
                    node = self.get_node(name)
                    step = name #node.get_label()
                    next = "%s" % (atoi(step) + 1)
                    n = graph.addNode(name, node.get_label(), start=step)

                    if node.get("obj") is None:
                        raise Exception("Node without objective in BBTree, node =", node)
                    
                    n.addAttribute(objAtt, "%s" % node.get("obj"))
                    n.addAttribute(currAtt, "1", start=step, end=next)
                    n.addAttribute(currAtt, "0", start=next)
                edge_names = self.get_edge_list()
                for i, (m_name, n_name) in enumerate(edge_names):
                    edge = self.get_edge(m_name, n_name)
                    graph.addEdge(i, edge.get_source(), edge.get_destination(), start=edge.get_destination())
                output_file = open(filename + ".gexf", "w")
                gexf.write(output_file)
                
            except Exception as e:
                print e
                print "No .gexf file created"
        else:
            raise Exception("Only Dot mode supported in write_bb_as_gexf")

if __name__ == '__main__':
        
    G = Graph(graph_type = 'graph', splines='false', layout = 'dot', K = 1)
    G.random(numnodes = 7, density = 0.7, length_range = (-5, 5), seedInput = 5)
#    G.random(numnodes = 10, density = 0.7, seedInput = 5)

    G.set_display_mode('off')

    G.display()

#    G.search(0, display = 'pygame', algo = 'DFS')
#    G.minimum_spanning_tree_kruskal(display = 'pygame')
    G.search(source = '0', algo = 'Prim')
