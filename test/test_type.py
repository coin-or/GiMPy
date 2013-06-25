from gimpy import Graph, DIRECTED_GRAPH, UNDIRECTED_GRAPH

g = Graph(display='pygame')
g.random(numnodes=10, degree_range=(2,5))
g.display()
