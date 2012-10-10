'''
This module implements a Graph class based on the class provided by Pydot.
You must have installed Pydot and Graphviz. Optionally, if you have
PIL, xdot, or Pygame installed, these can also be used for display
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__        = None
__title__      = 'GiMPy (Graph Methods in Python)'

import sys
#sys.path.append('..\pydot')
#sys.path.append('..\xdot')
#sys.path.append('..\GrUMPy')
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

try:
    from PIL import Image
except ImportError:
    PIL_installed = False
    print 'Pyton Image Library not installed'
else:
    PIL_installed = True
    print 'Found Python Image Library'

try:
    import gtk
    import gtk.gdk
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
    from baktree import BAKTree as Bak
except ImportError:
    bak_installed = False
    print 'BAK not installed'
else:
    bak_installed = True
    print 'Found BAK installation'

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
            raise Exception("Multiple instances of node", name, "present in Tree")

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
        Dot.del_edge(self, quote_if_necessary(str(m)), quote_if_necessary(str(n)))

    def get_edge(self, m, n):
        edges = Dot.get_edge(self, quote_if_necessary(str(m)), quote_if_necessary(str(n)))
        if len(edges) == 1:
            return edges[0]
        elif len(edges) == 0:
            return None
        else:
            raise Exception("Multiple instances of edge (", m, n, ") present in Tree")

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
            raise Exception, "get_out_neighbors method called for undirected graph"
        try:
            return self.out_neighbor_lists[str(n)]
        except KeyError:
            pass

    def get_in_neighbors(self, n):
        if self.graph_type != 'digraph':
            raise Exception, "get_in_neighbors method called for undirected graph"
        return self.in_neighbor_lists[str(n)]

    def label_components(self, display = None):
        '''
        This method labels the nodes of an undirected graph with component numbers
        so that each node has the same label as all nodes in the same component
        '''
        if self.graph_type == 'digraph':
            raise Exception, "label_components only works for undirected graphs"
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
    
    def label_strong_component(self, root, disc_count = 0, finish_count = 1, component = None):
        if self.graph_type == 'graph':
            raise Exception, "label_strong_componentsis only for directed graphs"
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
                    disc_count, finish_count = self.dfs(i, disc_count, finish_count, 
                                                   component, transpose)
            else:
                if self.get_node_attr(i, 'component') is None:
                    disc_count, finish_count = self.dfs(i, disc_count, finish_count, 
                                                   component, transpose)
        finish_count += 1
        self.set_node_attr(root, 'finish_time', finish_count)
        return disc_count, finish_count

    def bfs(self, root, display = None, component = None):
        self.search(root, display = display, component = component, q = Queue())
        
    def path(self, source, destination, display = None):
        return self.search(source, destination, display = display)

    def shortest_unweighted_path(self, source, destination, display = None):
        return self.search(source, destination, display = display, q = Queue(), algo = 'BFS')

    def shortest_weighted_path(self, source, destination = None, display = None, q = PriorityQueue()):
        '''
        This method determines the shortest paths to all nodes reachable from "source" 
        if "destination" is not given. Otherwise, it determines a shortest path from 
        "source" to "destination". The variable "q" must be an instance of a priority 
        queue. 
        '''
        nl = self.get_node_list()
        for i in nl:
            self.set_node_attr(i, 'color', 'black')
            for j in self.neighbor_lists[i]:
                self.set_edge_attr(i, j, 'color', 'black')
        
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode = display
        if isinstance(q, PriorityQueue):
            addToQ = q.push
            removeFromQ = q.pop
            peek = q.peek
            isEmpty = q.isEmpty
        #if self.graph_type == 'digraph':
        #    neighbors = self.get_out_neighbors
        #else:
        #    neighbors = self.get_neighbors
        
        neighbors = self.get_neighbors

        pred = {}
        addToQ(str(source))
        done = False
        while not isEmpty() and not done:
            current = removeFromQ()
            self.set_node_attr(current, 'color', 'blue')
            if current != str(source):
                self.set_edge_attr(pred[current], current, 'color', 'green')
            if current == str(destination):
                done = True
                break
            self.display()
            for n in neighbors(current):
                if self.get_node_attr(n, 'color') != 'green':
                    self.set_edge_attr(current, n, 'color', 'yellow')
                    self.display()
                    new_estimate = q.get_priority(current) + self.get_edge_attr(current, n, 'cost')
                    if not n in pred or new_estimate < peek(n):
                        pred[n] = current
                        self.set_node_attr(n, 'color', 'red')
                        self.set_node_attr(n, 'label', new_estimate)
                        addToQ(n, new_estimate)
                        self.display()
                        self.set_node_attr(n, 'color', 'black')
                    self.set_edge_attr(current, n, 'color', 'black')
            self.set_node_attr(current, 'color', 'green')
            self.display()
                    
        if done:
            path = [str(destination)]
            current = str(destination)        
            while current != str(source):
                path.insert(0, pred[current])
                current = pred[current]
            return path, q.get_priority(current)
        
        return pred

    def minimum_spanning_tree_prim(self, source, display = None, q = PriorityQueue()):
        '''
        This method determines a minimum spanning tree of all nodes reachable from "source" 
        using Prim's Algorithm
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode = display
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
            distance, count, current = removeFromQ()
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
        This method determines a minimum spanning tree of all nodes reachable from "source" 
        using Kruskal's Algorithm
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode = display
        
        if components is None:
            components = DisjointSet(display = 'pygame', layout = 'dot', optimize = True)
            
        sorted_edge_list = sorted(self.obj_dict['edges'].keys(), key = self.get_edge_cost)
        
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
            
    def search(self, source, destination = None, display = None, component = None, q = Stack(),
               algo = 'DFS', **kargs):
        '''
        This method determines all nodes reachable from "source" if "destination" is not given.
        Otherwise, it determines whether there is a path from "source" to "destination"
        Optionally, it marks all nodes reachable from "source" with a component number.
        The variable "q" determines the order in which the nodes are searched. 
        
        post: The return value should be a list of nodes on the path from "source" to
        "destination" if one is found. Otherwise, "None" is returned
        '''
        if display == None:
            display = self.display_mode
        else:
            self.set_display_mode(display)
            
        if algo == 'DFS':
            q = Stack()
        elif algo == 'BFS':
            q = Queue()
            #self.process_edge = Graph.process_edge
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
            neighbors = self.get_out_neighbors
        else:
            neighbors = self.get_neighbors

        nl = self.get_node_list()
        for i in nl:
            self.set_node_attr(i, 'color', 'black')
            for j in neighbors(i):
                self.set_edge_attr(i, j, 'color', 'black')

        pred = {}
        self.process_edge(None, source, pred, q, component, algo, **kargs)
        found = True
        if str(source) != str(destination):
            found = False
        while not q.isEmpty() and not found:
            current = q.peek()
            if 'pattern' in kargs:
                self.process_node(current, kargs['pattern'])
            self.set_node_attr(current, 'color', 'blue')
            if current != str(source):
                self.set_edge_attr(pred[current], current, 'color', 'green')
            if current == str(destination):
                found = True
                break
            self.display()
            for n in neighbors(current):
                if self.get_node_attr(n, 'color') != 'green':
                    self.set_edge_attr(current, n, 'color', 'yellow')
                    self.display()
                    self.process_edge(current, n, pred, q, component, algo, **kargs)
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

    def process_node(self, node, pattern):
        pass

    def process_edge_dijkstra(self, current, neighbor, pred, q, component):

        if current is None:
            self.set_node_attr(neighbor, 'color', 'red')
            self.set_node_attr(neighbor, 'label', 0)
            q.push(str(neighbor), 0)
            self.display()
            self.set_node_attr(neighbor, 'color', 'black')
            return
       
        new_estimate = q.get_priority(str(current)) + self.get_edge_attr(current, neighbor, 'cost')
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

    def process_edge(self, current, neighbor, pred, q, component, algo, **kargs):

        if algo == 'Dijkstra':
            return self.process_edge_dijkstra(current, neighbor, pred, q, component)

        if algo == 'Prim':
            return self.process_edge_prim(current, neighbor, pred, q, component)

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

    def find_maximum_flow(self, source, sink, display=None):
        '''
        API: find_maximum_flow(self, source, sink, display=None)
        Finds maximum flow from source to sink. Returns the tuple
        (flow_amount, flow_map) where flow amount is the integer value of
        maximum flow and flow_map is the flow dictionary where keys are
        tuples of nodes (n,m) where n and m are string, and values are the
        optimal flow on the edge (n,m).
        Assumes edges have 'capacity' attribute.
        Assumes directed arc for now.
        inputs:
            source: source node, integer or string
            sink: sink node, integer or string
            display: 
        return value:
            (flow_amount, flow_map)
        '''
        if display=='pygame':
            self.set_display_mode('pygame')
        if isinstance(source, int):
            source = str(source)
        if isinstance(sink, int):
            sink = str(sink)
        nl = self.get_node_list()
        # set flow of all edges to 0
        for n in nl:
            for m in nl:
                if self.get_edge(n,m)!=None:
                    self.set_edge_attr(n, m, 'flow', 0)
                    capacity = self.get_edge_attr(n, m, 'capacity')
                    self.set_edge_attr(n, m, 'label', str(capacity)+'/0')
        self.display()
        while True:
            # find an augmenting path from source to sink using DFS
            dfs_stack = []
            dfs_stack.append(source)
            pred = {source:None}
            explored = [source]
            for n in self.get_node_list():
                self.set_node_attr(n, 'color', 'black')
            for n in self.get_node_list():
                for m in self.get_node_list():
                    if self.get_edge(n,m)!=None:
                        if self.get_edge_attr(n,m,'flow')==0:
                            self.set_edge_attr(n,m,'color','black')
                        elif self.get_edge_attr(n,m,'flow')==self.get_edge_attr(n,m,'capacity'):
                            self.set_edge_attr(n,m,'color','red')
                        else:
                            self.set_edge_attr(n,m,'color','green')
            self.display()
            while dfs_stack:
                current = dfs_stack.pop()
                if current==sink:
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
                        available_capacity = self.get_edge_attr(current, m,
                                                            'capacity')-\
                                         self.get_edge_attr(current, m, 'flow')
                    else:
                        self.set_edge_attr(m, current , 'color', 'yellow')
                        available_capacity = self.get_edge_attr(m, current, 'flow')
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
                            if self.get_edge_attr(current,m,'flow')==self.get_edge_attr(current,m,'capacity'):
                                self.set_edge_attr(current,m,'color','red')
                            elif self.get_edge_attr(current,m,'flow')==0:
                                self.set_edge_attr(current, m, 'color', 'black')
                            else:
                                self.set_edge_attr(current, m, 'color', 'green')
                        else:
                            if self.get_edge_attr(m,current,'flow')==self.get_edge_attr(m,current,'capacity'):
                                self.set_edge_attr(m,current,'color','red')
                            elif self.get_edge_attr(m,current,'flow')==0:
                                self.set_edge_attr(m,current,'color', 'black')
                            else:
                                self.set_edge_attr(m,current,'color', 'green')
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
                    if min_capacity=='infinite':
                        min_capacity = potential
                    elif min_capacity>potential:
                        min_capacity = potential
                else:
                    potential = self.get_edge_attr(current, m, 'flow')
                    if min_capacity=='infinite':
                        min_capacity = potential
                    elif min_capacity>potential:
                        min_capacity = potential
                if m==source:
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
                    self.set_edge_attr(m, current, 'label', str(capacity)+'/'+str(new_flow))
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
                if m==source:
                    break
                current = m


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
                                length = randint(length_range[0], length_range[1])
                                self.add_edge(m, n, cost = length, 
                                              label = str(length), **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            if density != None:
                for m in range(numnodes):
                    if self.graph_type == 'digraph':
                        numnodes2 = numnodes
                    else:
                        numnodes2 = m
                    for n in range(numnodes2):
                        if random() < density:
                            if length_range is not None:
                                length = randint(length_range[0], length_range[1])
                                self.add_edge(m, n, cost = length, 
                                              label = str(length), **edge_format)
                            else:
                                self.add_edge(m, n, **edge_format)
            else:
                print "Must set either degree range or density"
        else:
            for m in range(numnodes):
                ''' Assigns random coordinates (between 1 and 20) to the nodes '''
                self.add_node(m, locationx = randint(1, 20), locationy = randint(1, 20), **node_format)
            if degree_range is not None:
                for m in range(numnodes):
                    for i in range(randint(degree_range[0], degree_range[1])):
                        n = randint(1, numnodes)
                        if not self.get_edge(m, n) and m != n:
                            if length_range is None:
                                ''' calculates the euclidean norm and round it to three decimal places '''
                                length = round((((self.get_node_attr(n, 'locationx') - self.get_node_attr(m, 'locationx')) ** 2 
                                           + (self.get_node_attr(n, 'locationy') - self.get_node_attr(m, 'locationy')) ** 2) ** 0.5), 3) 
                                self.add_edge(m, n, cost = length, 
                                             label = str(length), **edge_format)
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
                                ''' calculates the euclidean norm and round it to three decimal places '''
                                length = round((((self.get_node_attr(n, 'locationx') - self.get_node_attr(m, 'locationx')) ** 2 
                                           + (self.get_node_attr(n, 'locationy') - self.get_node_attr(m, 'locationy')) ** 2) ** 0.5), 3) 
                                self.add_edge(m, n, cost = length, 
                                             label = str(length), **edge_format)
                                print 'Node #' + str(n) + ' x-coordinate is ' + str(self.get_node_attr(n, 'locationx'))
                                print 'Node #' + str(m) + ' x-coordinate is ' + str(self.get_node_attr(m, 'locationx'))
                                print 'Node #' + str(n) + ' y-coordinate is ' + str(self.get_node_attr(n, 'locationy'))
                                print 'Node #' + str(m) + ' y-coordinate is ' + str(self.get_node_attr(m, 'locationy')) 
                                print
                            else:
                                self.add_edge(m, n, **edge_format)
            else:
                print "Must set either degree range or density"

    def page_rank(self, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
        """
        Compute and return the PageRank in a directed graph.
        
        This function was originally taken from here and modified for this graph class:
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
        min_value = (1.0-damping_factor)/graph_size #value for nodes without inbound links
    
        # itialize the page rank dict with 1/N for all nodes
        pagerank = dict.fromkeys(nodes, 1.0/graph_size)
        
        for i in range(max_iterations):
            diff = 0 #total difference compared to last iteraction
            # computes each node PageRank based on inbound links
            for node in nodes:
                rank = min_value
                for referring_page in self.get_in_neighbors(node):
                    rank += damping_factor * pagerank[referring_page] / len(self.get_out_neighbors(referring_page))
                
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
                dd[n] = len(self.get_in_neighbors(n)) + len(self.get_out_neighbors(n))
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
            print "Unknown display mode"
        
    def exit_window(self):
        if self.display_mode != 'pygame':
            return
        while True:
            e = event.wait()
            if e.type == QUIT:
                break

    def add_subgraph(self, S):
        Dot.add_subgraph(self, S)
    
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
    
    def __init__(self, display = False, **attrs):
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
        
class BinaryTree(Tree):

    def __init__(self, display = False, **attrs):
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
                
    def print_nodes(self, order = 'in', priority = 'L', display = None, root = None):
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

    def traverse(self, root = None, display = None, q = Stack(), priority = 'L', 
                 order = 'in'):
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
        opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}
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

if __name__ == '__main__':
    
    G = Graph(graph_type = 'graph', splines='true', layout = 'fdp', K = 1)
    G.random(numnodes = 10, density = 0.7, length_range = (5, 20), seedInput = 5)
#    G.random(numnodes = 10, density = 0.7, seedInput = 5)

#    G.search(0, display = 'pygame', algo = 'Dijkstra')

    G.set_display_mode('pygame')

    G.minimum_spanning_tree_kruskal(display = 'pygame')
        
    G.display()

    
    
