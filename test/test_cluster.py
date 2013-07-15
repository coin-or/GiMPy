'''
This script implements the graphviz example at location
http://www.graphviz.org/Gallery/directed/cluster.html
in our graph class. Main purpose of the Graph class is not to be python
interface to graphviz. Main purpose is to implement a graph class using
the methods in the literature and measuring running time performances. Hence
it is teaching/research oriented. This script demonstrates the Graph class's
capability as a graphviz interface.
'''

from gimpy import Graph, DIRECTED_GRAPH

if __name__=='__main__':
    c = Graph(type=DIRECTED_GRAPH, layout = 'dot')
    # add edges
    c.add_edge('start', 'a0')
    c.add_edge('a0', 'a1')
    c.add_edge('a1', 'a2')
    c.add_edge('a2', 'a3')
    c.add_edge('start', 'b0')
    c.add_edge('b0', 'b1')
    c.add_edge('b1', 'b2')
    c.add_edge('b2', 'b3')
    c.add_edge('b2', 'a3')
    c.add_edge('a3', 'end')
    c.add_edge('b3', 'end')
    c.add_edge('a3', 'a0')
    c.add_edge('a1', 'b3')
    # set node attributes
    c.set_node_attr('start', 'shape', 'Mdiamond')
    c.set_node_attr('end', 'shape', 'Msquare')
    # create clusters
    # create dictionaries with cluster attributes and node attributes
    cluster_attrs = {'name':'0', 'style':'filled', 'color':'lightgrey', 'label':'process #1'}
    node_attrs = {'style':'filled', 'color':'white'}
    # create cluster
    c.create_cluster(['a0', 'a1', 'a2', 'a3'], cluster_attrs, node_attrs)
    # modify attributes for the second cluster
    cluster_attrs['name']='1'
    cluster_attrs['color']='blue'
    del cluster_attrs['style']
    cluster_attrs['label'] = 'process #2'
    del node_attrs['color']
    # create second cluster
    c.create_cluster(['b0', 'b1', 'b2', 'b3'], cluster_attrs, node_attrs)
    # print graph in dot language to stdout
    print c.to_string()
    c.set_display_mode('pygame')
    c.display()
