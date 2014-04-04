try:
    from src.gimpy import Graph, UNDIRECTED_GRAPH
except ImportError:
    from coinor.gimpy import Graph, UNDIRECTED_GRAPH

G = Graph(type = UNDIRECTED_GRAPH, splines = 'true', K = 1.5)
G.random(numnodes = 10, Euclidean = True, seedInput = 11, 
         #add_labels = True,
         #scale = 10,
         #scale_cost = 10,
         #degree_range = (2, 4),
         #length_range = (1, 10)
         )
G.set_display_mode('pygame')
G.display()
#G.dfs(0)
G.search(0, display = 'pygame', algo = 'Dijkstra')
        
