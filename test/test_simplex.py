#import pycallgraph
import cProfile
import pstats

from compare import generate_graph

if __name__=='__main__':
    gen = (38, 0.6, 7, 5, (5,10), (30,50), (10,20))
    #gen = (35, 0.2, 6, 4, (5,10), (30,50), (0,100))
    g, rg = generate_graph(1, gen)
    rg.min_cost_flow(algo="simplex", pivot="dantzig")
    #pycallgraph.start_trace()
    #cProfile.run('rg.min_cost_flow(algo="simplex", pivot="dantzig")', 'cprof.out')
    #p = pstats.Stats('cprof.out')
    #p.sort_stats('cumulative').print_stats(30)
    #pycallgraph.make_dot_graph('simplex_call_graph.png')
