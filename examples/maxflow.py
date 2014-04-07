'''
Small example for demonstrating flow agumenting path (ford-fulkerson)
algorithm.
This example is taken from youtube lecture series on Advanced Operations
Research by Prof. G.Srinivasan.
Link to the video is:
http://www.youtube.com/watch?v=J0wzih3_5Wo

black: there is no flow on the arc
red  : the flow equals to the arc capacity
green: there is positive flow on the arc, less then capacity.
'''

try:
    from src.gimpy import Graph, DIRECTED_GRAPH
except ImportError:
    from coinor.gimpy import Graph, DIRECTED_GRAPH

if __name__=='__main__':
    g = Graph(type = DIRECTED_GRAPH, display = 'off')
    g.add_node(1,pos='"0,2!"')
    
    g.add_node(3,pos='"2,4!"')
    g.add_node(2,pos='"2,0!"')
    g.add_node(4,pos='"4,2!"')
    g.add_node(6,pos='"6,4!"')
    
    g.add_node(5,pos='"6,0!"')
    g.add_node(7,pos='"8,2!"')
    g.add_edge(1, 3, capacity=40, label='40')
    g.add_edge(1, 2, capacity=40, label='40')
    g.add_edge(3, 4, capacity=10, label='10')
    g.add_edge(3, 6, capacity=10, label='10')
    g.add_edge(2, 4, capacity=15, label='15')
    g.add_edge(2, 5, capacity=20, label='20')
    g.add_edge(4, 6, capacity=20, label='20')
    g.add_edge(4, 7, capacity=10, label='10')
    g.add_edge(4, 5, capacity=10, label='10')
    g.add_edge(6, 7, capacity=30, label='30')
    g.add_edge(5, 7, capacity=20, label='20')
    g.set_display_mode('pygame')

#    g.max_flow_preflowpush(1, 7, algo = 'HighestLabel')
    g.max_flow(1, 7, algo = 'BFS')
    
    nl = list(int(n) for n in g.get_node_list())
    nl.sort()
    for n in nl:
        for m in nl:
            if g.check_edge(n, m):
                print n, m, g.get_edge_attr(n, m, 'flow')
