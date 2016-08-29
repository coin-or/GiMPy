from coinor.gimpy import Graph
from coinor.gimpy import DIRECTED_GRAPH

import random

'''
# Here is some static data for testing
demand = [10,
          4,
          7]

harvest = [[7, 2],
           [3, 5],
           [2, 1]]

numForests = len(harvest[0])
numYears = len(demand)
'''

random.seed(0)
numForests = 2
numYears = 3
demand = [random.randint(25, 50) for i in range(numYears)]
harvest = [[random.randint(5, 10) for j in range(numForests)]
           for i in range(numYears)]

forest = ['f'+ str(i) for i in range(numForests)]
year = ['y'+ str(i) for i in range(numYears)]

g = Graph(display='off',type=DIRECTED_GRAPH, splines = 'true', K = 1.5,
          rankdir = 'LR', layout = 'dot')

for i in range(numYears):
    g.add_node(year[i], label = 'Total Production\nin Year %s' %(i+1))
    g.add_edge(year[i], 'sink', capacity = demand[i])

for j in range(numForests):
    g.add_node(forest[j], label = 'Forest ' + str(j+1))
    g.add_edge('source', forest[j])
    for i in range(numYears):
        g.add_node((forest[j], year[i]),
                   label = "Production\nof Forest %s\nin Year %s"%(str(j+1), str(i+1)))
        g.add_edge(forest[j], (forest[j], year[i]), capacity = harvest[i][j])
        g.add_edge((forest[j], year[i]), year[i])
    for i in range(numYears-1):
        g.add_edge((forest[j], year[i]), (forest[j], year[i+1]))

g.max_flow('source', 'sink')
g.set_display_mode('file')
g.display()
