'''
tests network simplex visualization
'''

from coinor.gimpy import Graph, DIRECTED_GRAPH
from random import seed, randint, random

def generate_graph():
    g = Graph(type=DIRECTED_GRAPH)
    # supply nodes; 1,2
    g.add_node(1, demand=20, pos='"0,3!"')
    g.add_node(2, demand=10, pos='"0,1!"')
    # transhipment nodes; 3,4
    g.add_node(3, demand=0, pos='"3,4!"')
    g.add_node(4, demand=0, pos='"3,1!"')
    # demand nodes; 5,6,7
    g.add_node(5, demand=-5, pos='"6,3!"')
    g.add_node(6, demand=-10, pos='"6,2!"')
    g.add_node(7, demand=-15, pos='"6,0!"')
    # add edges
    g.add_edge(1,2,cost=5,capacity=10)
    g.add_edge(1,3,cost=6,capacity=15)
    g.add_edge(1,4,cost=10,capacity=15)
    g.add_edge(2,3,cost=7,capacity=10)
    g.add_edge(3,4,cost=4,capacity=15)
    g.add_edge(3,5,cost=5,capacity=10)
    g.add_edge(3,6,cost=7,capacity=10)
    g.add_edge(4,5,cost=6,capacity=8)
    g.add_edge(4,6,cost=4,capacity=10)
    g.add_edge(4,7,cost=8,capacity=20)
    g.add_edge(5,6,cost=2,capacity=10)
    g.add_edge(6,7,cost=2,capacity=20)
    return g

def generate_graph2():
    '''
    this example is form lecture notes of Prof. James Orlin in Optimization
    Methods in Management Science class. Link to lecture notes is as follows.
    http://ocw.mit.edu/courses/sloan-school-of-management/
    15-053-optimization-methods-in-management-science-spring-2007/
    lecture-notes/lec15.pdf
    '''
    g = Graph(type=DIRECTED_GRAPH)
    # supply nodes; 2,3,6
    g.add_node(2, demand=6, pos='"1,2!"')
    g.add_node(3, demand=6, pos='"0,0!"')
    g.add_node(6, demand=12, pos='"5,2!"')
    # demand nodes; 1,4,5,7
    g.add_node(1, demand=-3, pos='"3,4!"')
    g.add_node(4, demand=-11, pos='"2,0!"')
    g.add_node(5, demand=-3, pos='"3,2!"')
    g.add_node(7, demand=-7, pos='"4,0!"')
    # add edges
    g.add_edge(1,2,cost=1,capacity=10)
    g.add_edge(2,4,cost=2,capacity=15)
    g.add_edge(2,5,cost=2,capacity=15)
    g.add_edge(3,2,cost=2,capacity=10)
    g.add_edge(3,4,cost=1,capacity=4)
    g.add_edge(4,7,cost=1,capacity=10)
    g.add_edge(6,1,cost=3,capacity=10)
    g.add_edge(6,5,cost=2,capacity=2)
    g.add_edge(6,7,cost=10,capacity=5)
    return g

if __name__=='__main__':
    g = generate_graph()
    g.set_display_mode('pygame')
    g.min_cost_flow(algo='simplex')
