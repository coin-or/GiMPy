'''
Created on Feb 29, 2012

@author: tkr2
'''

from pydot import Dot, Node, Edge
from pydot import quote_if_necessary
from random import random, randint, seed
from queues_solution import Queue
from stacks_solution import Stack
from lists_solution import LinkedList
import operator
from StringIO import StringIO
from sys import exit
from priority_queue import PriorityQueue
from operator import itemgetter
from PIL import Image

try:
    from pygame.locals import QUIT, KEYDOWN
    from pygame import display, image, event, init
except ImportError:
    pygame_installed = False
else:
    pygame_installed = True

try:
    from baktree import BAKTree as Bak
except ImportError:
    bak_installed = False
else:
    bak_installed = True

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
        self.type = attrs['graph_type']
        self.num_components = None
        if self.type == 'digraph':
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
        if self.type == 'digraph':
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
        if self.type == 'digraph':
            try:
                for neighbor in self.out_neighbor_lists[str(name)]:
                    self.del_edge(name, neighbor)
                for neighbor in self.in_neighbor_lists[str(name)]:
                    self.del_edge(neighbor, name)
                del self.out_neighbor_lists[str(name)]
                del self.in_neighbor_lists[str(name)]
            except KeyError:
                return False
        if self.type == 'graph':
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
        if self.type == 'digraph':
            self.out_neighbor_lists[str(m)].append(str(n))
            self.in_neighbor_lists[str(n)].append(str(m))
        else:
            self.neighbor_lists[str(m)].append(str(n))
            self.neighbor_lists[str(n)].append(str(m))
        self.num_components = None
        
    def del_edge(self, m, n):
        if self.type == 'digraph':
            try:
                del self.get_out_neighbors(str(m))[str(n)]
                del self.get_in_neighbors(str(n))[str(m)]
            except KeyError:
                return False
        if self.type == 'graph':
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
        if self.type == 'digraph':
            raise Exception, "get_neighbors method called for digraph" 
        return self.neighbor_lists[str(n)]

    def get_out_neighbors(self, n):
        if self.type != 'digraph':
            raise Exception, "get_out_neighbors method called for undirected graph"
        try:
            return self.out_neighbor_lists[str(n)]
        except KeyError:
            pass

    def get_in_neighbors(self, n):
        if self.type != 'digraph':
            raise Exception, "get_in_neighbors method called for undirected graph"
        return self.in_neighbor_lists[str(n)]

    def label_components(self, display = None):
        '''
        This method labels the nodes of an undirected graph with component numbers
        so that each node has the same label as all nodes in the same component
        '''
        if self.type == 'digraph':
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
        if self.type == 'graph':
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
        if self.type == 'digraph':
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
        #if self.type == 'digraph':
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
        if self.type == 'digraph':
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
            self.set_display_mode = display
            
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

        if self.type == 'digraph':
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
                    if self.type == 'digraph':
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
            print "Random Euclidean graph generation not implemented yet"

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
        if self.type == 'graph':
            for n in self.get_node_list():
                dd[n] = len(self.get_neighbors(n))
        elif self.type == 'digraph':
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
                    exit()
        elif self.display_mode == 'PIL':
            im2 = Image.open(im)
            im2.show()
        else:
            print "Unknown display mode"
        
    def exit_window(self):
        if self.display_mode != 'pygame':
            return
        while True:
            e = event.wait()
            if e.type == QUIT:
                break

class Tree(Graph):
    
    def __init__(self, display = False, **attrs):
        attrs['graph_type'] = 'digraph'
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
        if bak_installed:
            self.__bases__ += Bak
            Bak.__init__(self)

    def add_root(self, root, branch_direction = None, vertical_position = None, **attrs):
        Tree.add_root(self, root, **attrs)
        if vertical_position == None:
            vertical_position = 0
        if bak_installed:
            self.AddOrUpdateNode(root, None, None, 'candidate', 
                                 vertical_position, None, None)
    
    def add_child(self, n, parent, branch_direction = None, vertical_position = None, **attrs):
        children = self.get_children(parent)
        if branch_direction == None:
            if len(children) == 0:
                # Add left child first by default
                branch_direction = 'L'
            elif len(children) == 1:
                if self.get_node_attr(children[0], 'which') == 'L':
                    branch_direction = 'R'
                elif self.get_node_attr(children[0], 'which') == 'R':
                    branch_direction = 'L'
                else:
                    raise Exception("BinaryTree child node is neither left nor right")
            else:
                raise Exception("Trying to add a 3rd child to a BinaryTree node")
        if vertical_position == None:
            vertical_position = self.get_node_attr(parent, 'level') + 1
        attrs['which'] = branch_direction
        attrs['parent'] = parent
        self.add_node(n, **attrs)
        self.add_edge(parent, n)
        if branch_direction == 'L' and len(children) == 1:
            #We want the left child to come first in the sequence
            self.get_node(children[0]).set_sequence(self.get_next_sequence_number())
            self.get_edge(parent, children[0]).set_sequence(self.get_next_sequence_number())
        if bak_installed:
            self.AddOrUpdateNode(n, parent, branch_direction, 'candidate', 
                                 vertical_position, None, None)
        
    def add_right_child(self, n, parent, **attrs):
        attrs['which'] = 'R'
        BinaryTree.add_child(self, n, parent, **attrs)
        
    def add_left_child(self, n, parent, **attrs):
        attrs['which'] = 'R'
        BinaryTree.add_child(self, n, parent, **attrs)
        
    def get_right_child(self, n):
        for child in self.get_children(n):
            if self.get_node_attr(child, 'which') == 'R':
                return child
        return None

    def get_left_child(self, n):
        for child in self.get_children(n):
            if self.get_node_attr(child, 'which') == 'L':
                return child
        return None
                
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
    
    G = Graph(graph_type = 'digraph', splines = 'true', layout = 'dot', display = 'pygame')
    G.add_node('Chem 30')
    G.add_node('Math 21')
    G.add_node('Math 22')
    G.add_edge('Math 21', 'Math 22')
    G.add_node('Math 23')
    G.add_edge('Math 22', 'Math 23')
    G.add_node('Math 205')
    G.add_edge('Math 22', 'Math 205')
    G.add_node('Physics 11/12')
    G.add_edge('Math 21', 'Physics 11/12')
    G.add_node('Physics 21/22')
    G.add_edge('Math 23', 'Physics 21/22')
    G.add_node('ME 104')
    G.add_edge('Math 23', 'ME 104')
    G.add_node('Mech 2')
    G.add_edge('Math 22', 'Mech 2')
    G.add_node('ECE 84')
    G.add_node('Eco 1')
    G.add_node('Engl 1')
    G.add_node('Engl 2')
    G.add_node('Eng 97')
    G.add_node('Eng 98')
    G.add_node('IE 111')
    G.add_edge('Math 22', 'IE 111')
    G.add_node('IE 121')
    G.add_edge('IE 111', 'IE 121')
    G.add_node('IE 131/132')
    G.add_edge('IE 111', 'IE 131/132')
    G.add_node('IE 305')
    G.add_edge('IE 121', 'IE 305')
    G.add_node('IE 230')
    G.add_edge('IE 111', 'IE 230')
    G.add_node('IE 240')
    G.add_edge('Math 205', 'IE 240')
    G.add_node('IE 251')
    G.add_edge('IE 121', 'IE 251')
    G.add_edge('IE 230', 'IE 251')
    
#    G. display()
    
    G = Graph(graph_type = 'graph', splines='true', layout = 'fdp', K = 1)
#    G.random(numnodes = 10, degree_range = (2,4), length_range = (10, 20))
    G.random(numnodes = 6, density = 0.7, length_range = (5, 20), seedInput = 3)
    G.set_display_mode('file')
    G.display()
    G.label_strong_component(0)
    for n in G.get_node_list():
        print 'node', n, G.get_node_attr(n, 'disc_time'), G.get_node_attr(n, 'finish_time'), G.get_node_attr(n, 'component') 
    #print G.to_string()
#    G.set_node_attr(0, 'label', '0')
    #G.search(0, algo = 'Prim')
    #G.search(0, algo = 'DFS')
    #G.label_components()
    #for n in range(10):
    #    print G.get_node_attr(str(n),'component')
    #G.dfs(0)
    #for n in range(10):
    #    print n, G.get_node_attr(str(n), 'disc_time'), G.get_node_attr(str(n), 'finish_time')
#    G.set_display_mode('off')
#    for i in range(10):
#        for j in range(10):
#            if i>=j:
#                continue
#            print G.shortest_weighted_path(i,j)
#    print G.minimum_spanning_tree_kruskal()
#    print G.page_rank()
    #G.exit_window()
    '''
    G.dfs(1)
    G.label_components()
    print G.path(1, 4)
        
    aList = []
    for j in range(25):
        aList.append(randint(0, 9999))

    T = BinaryTree(display = 'dot')
    
    #pycallgraph.start_trace()
    quick_sort_count(aList, T, True)
    #pycallgraph.make_dot_graph('test.png')
            
    T.dfs()
    T.bfs()
    T.print_nodes(order = 'post')

    T = BinaryTree()
    T.add_root(0)
    T.add_right_child(1, 0)
    T.add_left_child(2, 0)
    T.dfs(priority = 'R')
    
    T = BinaryTree(display = 'dot')
    T.add_root(0, label = '*')
    T.add_left_child(1, 0, label = '+')
    T.add_left_child(2, 1, label = '4')
    T.add_right_child(3, 1, label = '5')
    T.add_right_child(4, 0, label = '7')
    T.printexp()
    print
    T.postordereval()
    T.exit_window()
    '''
    
