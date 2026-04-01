'''
tests if cycle canceling method works properly.
'''

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
    generator = (10, 0.8, 3, 2, (5,10), (0,5), (100,200))
    print('Seed'.ljust(5), 'simplex'.ljust(8), 'cycle canceling')
    for seed in range(10):
        # cycle canceling flows
        cc_flows = {}
        # simplex flows
        s_flows = {}
        g = generate_graph(seed, generator)
        el = g.get_edge_list()
        g.min_cost_flow(algo="simplex", pivot="dantzig")
        for e in el:
            s_flows[e] = g.get_edge_attr(e[0], e[1], 'flow')
            g.set_edge_attr(e[0], e[1], 'flow', 0)
        g.min_cost_flow(algo="cycle_canceling")
        for e in el:
            cc_flows[e] = g.get_edge_attr(e[0], e[1], 'flow')
        # measure total cost of flow
        cc_cost = 0
        s_cost = 0
        for e in el:
            cost_e = g.get_edge_attr(e[0], e[1], 'cost')
            s_cost += s_flows[e]*cost_e
            cc_cost += cc_flows[e]*cost_e
        print(str(seed).ljust(5), str(s_cost).ljust(8), str(cc_cost))
