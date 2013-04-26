from gimpy import Graph, DIRECTED_GRAPH

def generate_test_instance1():
    g = Graph(type=DIRECTED_GRAPH, display='pygame')
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    g.add_edge(2,3)
    g.add_edge(3,4)
    g.add_edge(5,6)
    g.add_edge(6,7)
    g.add_edge(7,8)
    g.add_edge(8,6)
    g.add_edge(6,9)
    g.add_edge(10,11)
    return g

def generate_test_instance2():
    g = Graph(type=DIRECTED_GRAPH, display='pygame')
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(2,3)
    g.add_edge(3,0)
    g.add_edge(0,4)
    g.add_edge(4,5)
    g.add_edge(5,6)
    g.add_edge(6,4)
    g.add_edge(4,7)
    g.add_edge(7,1)
    g.add_edge(1,8)
    return g

if __name__=='__main__':
    g = generate_test_instance1()
    #g.label_strong_component(0)
    g.tarjan()
    for n in g.get_node_list():
        print n, g.get_node_attr(n, 'component')
    g.display()
