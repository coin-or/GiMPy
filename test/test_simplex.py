#import pycallgraph
import cProfile
import pstats

from test_algorithms import generate_graph

# a generator is in the following form (numnode, density, demand_numnode,
# supply_numnode, demand_range, cost_range, capacity_range)
# The following is an example for individual elements in a generator tuple
# numnodes = 10
# density = 0.5
# demand_numnodes = 3
# supply_numnodes = 2
# demand_range = (5,10)
# cost_range = (30,50)
# capacity_range = (10,20)

if __name__=='__main__':
    generator = (38, 0.6, 7, 5, (5,10), (30,50), (10,20))
    g = generate_graph(1, generator)
    g.min_cost_flow(algo="simplex", pivot="dantzig")
    #pycallgraph.start_trace()
    #cProfile.run('rg.min_cost_flow(algo="simplex", pivot="dantzig")', 'cprof.out')
    #p = pstats.Stats('cprof.out')
    #p.sort_stats('cumulative').print_stats(30)
    #pycallgraph.make_dot_graph('simplex_call_graph.png')
