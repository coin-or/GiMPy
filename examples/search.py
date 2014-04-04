try:
    from src.gimpy import Graph, UNDIRECTED_GRAPH
except ImportError:
    from coinor.gimpy import Graph, UNDIRECTED_GRAPH

G = Graph(type = UNDIRECTED_GRAPH, splines = 'true', K = 0.5)
G.random(numnodes = 15, Euclidean = True, seedInput = 11, scale_cost = 5)
#G = Graph(type = DIRECTED_GRAPH, splines = 'true', K = 2)
#    G.random(numnodes = 15, density = 0.4, degree_range=(1, 4), Euclidean = True, seedInput = 3)
#    G.random(numnodes = 7, density = 0.7, length_range = (1, 10), seedInput = 5)
#G.random(numnodes = 7, density = 0.7, Euclidean = True,
#         seedInput = 9, add_labels = True)
G.set_display_mode('xdot')
G.display()
#G.dfs(0)
G.search(0, display = 'pygame', algo = 'Dijkstra')
G.set_display_mode('xdot')
G.display()
        

#    G.random(numnodes = 10, density = 0.5, seedInput = 5)

#    G.set_display_mode('xdot')
#    print G.to_string()
#    G.display()
#    G.display(basename='try.png', format='png')

#    for i in G.nodes:
#        G.nodes[i].set_attr('label', '-,-')
#    G.dfs(0, display = 'pygame')
#    G.search(0, display = 'pygame', algo = 'Dijkstra')
#    G.minimum_spanning_tree_kruskal(display = 'pygame')
#    G.search(0, display = 'pygame')
#    G.cycle_canceling('pygame')
