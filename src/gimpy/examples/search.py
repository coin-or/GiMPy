from coinor.gimpy import *

G = Graph(type = UNDIRECTED_GRAPH, splines = 'true', K = 1.5)
G.random(numnodes = 20, Euclidean = True, seedInput = 1, 
         add_labels = True,
         #scale = 10,
         #scale_cost = 10,
         #degree_range = (2, 4),
         #length_range = (1, 10)
         )
G.set_display_mode('matplotlib')
G.display()
print(G.tsp(0, 11))
#G.search(0, display = 'matplotlib', algo = 'DFS')
#G.search(0, display = 'matplotlib', algo = 'BFS')
#G.search(0, display = 'matplotlib', algo = 'Prim')
#G.minimum_spanning_tree_kruskal()
