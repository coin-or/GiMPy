'''
Compare running times of gimpy and regimpy (reimplementation) and theoretical
for following algorithms DFS, BFS, augmenting flow, cycle canceling, simplex.
'''


#TODO(aykut)
#-> Add average support
#-> Enable algorithm and gimpy picking

# import reimplemented gimpy
import gimpy as regimpy
# import gimpy
import imp
#gimpy = imp.load_source('old', '../../trunk/gimpy.py')
gimpy = imp.load_source('reimplementation', '../gimpy.py')
import time
from random import seed, random, randint
import math
import matplotlib.pyplot as pyplot

#testing
# nodes       10, 15, 20, 25, 30
# arcs sparse 20, 30, 45, 65, 90
# arcs dense  35, 80, 150, 200, 300

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
sparse_generator = [
(24, 0.2, 3, 2, (5,10), (30,50), (10,20)),
(28, 0.2, 3, 2, (5,10), (30,50), (10,20)),
(32, 0.2, 4, 3, (5,10), (30,50), (10,20)),
(36, 0.1, 4, 3, (5,10), (30,50), (10,20)),
(40, 0.1, 5, 3, (5,10), (30,50), (10,20)),
(44, 0.1, 5, 3, (5,10), (30,50), (10,20)),
(48, 0.1, 6, 4, (5,10), (30,50), (10,20)),
(52, 0.1, 6, 4, (5,10), (30,50), (10,20)),
(56, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(60, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(64, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(68, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(72, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(76, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(80, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(84, 0.1, 7, 5, (5,10), (30,50), (10,20)),
(88, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(92, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(96, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(100, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(104, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(108, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(112, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(116, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(120, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(124, 0.1, 7, 5, (5,10), (30,50), (10,20)),
#(128, 0.1, 7, 5, (5,10), (30,50), (10,20))
]
dense_generator = [
(24, 0.6, 3, 2, (5,10), (30,50), (10,20)),
(28, 0.6, 3, 2, (5,10), (30,50), (10,20)),
(32, 0.6, 4, 3, (5,10), (30,50), (10,20)),
(36, 0.6, 4, 3, (5,10), (30,50), (10,20)),
(40, 0.6, 5, 3, (5,10), (30,50), (10,20)),
(44, 0.6, 5, 3, (5,10), (30,50), (10,20)),
(48, 0.6, 6, 4, (5,10), (30,50), (10,20)),
(52, 0.6, 6, 4, (5,10), (30,50), (10,20)),
(56, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(60, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(64, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(68, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(72, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(76, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(80, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(84, 0.6, 7, 5, (5,10), (30,50), (10,20)),
(88, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(92, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(96, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(100, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(104, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(108, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(112, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(116, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(120, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(124, 0.6, 7, 5, (5,10), (30,50), (10,20)),
#(128, 0.6, 7, 5, (5,10), (30,50), (10,20)),
]

# algorithms to be tested
algo = ['DFS', 'BFS', 'Dijkstra', 'Kruskal', 'Prim', 'PreflowPush', 'AugmentingPath', 'CycleCanceling', 'Simplex']
module = ['gimpy', 'regimpy', 'theoretical']
# run_time dictionary keys are modules and values are {algo: list of run-time
# in secs}
run_time = dict([(a,dict([(m,[]) for m in module])) for a in algo])
# keys are algo values are file objects that are in the following form
# instance    gimpy_time    regimpy_time    theoretical_time
# 0       10            10              5
result_file = dict([(a, None) for a in algo])
#
method = {'gimpy': {}, 'regimpy':{}}

def generate_graph(seed_i):
    '''
    Generates random directed graphs for min cost flow problem.
    '''
    #g = gimpy.Graph(graph_type='digraph', splines='true', layout = 'dot')
    rg = regimpy.Graph(type=regimpy.DIRECTED_GRAPH, splines='true', layout = 'dot')
    seed(seed_i)
    for i in range(numnodes):
        for j in range(numnodes):
            if i==j:
                continue
            if (i, j) in rg.edge_attr:
                continue
            if (j,i) in rg.edge_attr:
                continue
            if random() < density:
                cap = randint(capacity_range[0], capacity_range[1])
                cos = randint(cost_range[0], cost_range[1])
                #g.add_edge(i, j, cost=cos, capacity=cap)
                rg.add_edge(i, j, cost=cos, capacity=cap)
    # set supply/demand
    # select random demand_numnodes many nodes
    demand_node = {}
    while len(demand_node) < demand_numnodes:
        n = randint(0,numnodes-1)
        if n in demand_node:
            continue
        demand_node[n] = 0
    # select random supply_numnodes many nodes (different than above)
    supply_node = {}
    while len(supply_node) < supply_numnodes:
        n = randint(0,numnodes-1)
        if n in demand_node or n in supply_node:
            continue
        supply_node[n] = 0
    # set demand amounts
    total_demand = 0
    for n in demand_node:
        demand_node[n] = randint(demand_range[0], demand_range[1])
        total_demand += demand_node[n]
    # set supply amounts
    total_supply = 0
    for n in supply_node:
        supply_node[n] = randint(demand_range[0], demand_range[1])
        total_supply += supply_node[n]
    if total_demand > total_supply:
        # this line may create random behavior, because of dictionary query
        for n in supply_node:
            excess = total_demand-total_supply
            supply_node[n] += excess
            break
    elif total_demand < total_supply:
        for n in demand_node:
            excess = total_supply-total_demand
            demand_node[n] += excess
            break
    # set demand attributes
    for n in rg.get_node_list():
        if n in demand_node:
            rg.get_node(n).set_attr('demand', -1*demand_node[n])
            #g.set_node_attr(n, 'demand', -1*demand_node[n])
        elif n in supply_node:
            rg.get_node(n).set_attr('demand', supply_node[n])
            #g.set_node_attr(n, 'demand', supply_node[n])
        else:
            rg.get_node(n).set_attr('demand', 0)
            #g.set_node_attr(n, 'demand', 0)
    #return g, rg
    return rg

def test_DFS(g, rg):
    root = rg.get_node_list()[0]
    gtime = time.time()
    #g.dfs(root)
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.dfs(root)
    rgtime = time.time() - rgtime
    run_time['DFS']['gimpy'].append(gtime)
    run_time['DFS']['regimpy'].append(rgtime)

def test_BFS(g, rg):
    root = rg.get_node_list()[0]
    gtime = time.time()
    #g.bfs(root)
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.bfs(root)
    rgtime = time.time() - rgtime
    run_time['BFS']['gimpy'].append(gtime)
    run_time['BFS']['regimpy'].append(rgtime)

def test_dijkstra(g, rg):
    root = rg.get_node_list()[0]
    gtime = time.time()
    #g.search(root, algo='Dijkstra')
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.search(root, algo='Dijkstra')
    rgtime = time.time() - rgtime
    run_time['Dijkstra']['gimpy'].append(gtime)
    run_time['Dijkstra']['regimpy'].append(rgtime)

def test_kruskal(g, rg):
    gtime = time.time()
    #g.minimum_spanning_tree_kruskal(display='off')
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.minimum_spanning_tree_kruskal()
    rgtime = time.time() - rgtime
    run_time['Kruskal']['gimpy'].append(gtime)
    run_time['Kruskal']['regimpy'].append(rgtime)

def test_prim(g, rg):
    root = rg.get_node_list()[0]
    gtime = time.time()
    #g.minimum_spanning_tree_prim(source=root, display='off')
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.minimum_spanning_tree_prim(source=root)
    rgtime = time.time() - rgtime
    run_time['Prim']['gimpy'].append(gtime)
    run_time['Prim']['regimpy'].append(rgtime)

def test_preflow_push(g, rg):
    source = rg.get_node_list()[0]
    sink = rg.get_node_list()[-1]
    gtime = time.time()
    #g.max_flow_preflowpush(source, sink, algo='FIFO', display='off')
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.max_flow_preflowpush(source, sink, algo='FIFO')
    rgtime = time.time() - rgtime
    run_time['PreflowPush']['gimpy'].append(gtime)
    run_time['PreflowPush']['regimpy'].append(rgtime)

def test_augmenting_path(g, rg):
    source = rg.get_node_list()[0]
    sink = rg.get_node_list()[-1]
    gtime = time.time()
    #g.max_flow(source, sink)
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.max_flow(source, sink)
    rgtime = time.time() - rgtime
    run_time['AugmentingPath']['gimpy'].append(gtime)
    run_time['AugmentingPath']['regimpy'].append(rgtime)

def test_cycle_canceling(g, rg):
    gtime = time.time()
    #g.min_cost_flow(algo="cycle_canceling")
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.min_cost_flow(algo="cycle_canceling")
    rgtime = time.time() - rgtime
    run_time['CycleCanceling']['gimpy'].append(gtime)
    run_time['CycleCanceling']['regimpy'].append(rgtime)

def test_network_simplex(g, rg):
    gtime = time.time()
    #g.min_cost_flow(algo="simplex", pivot='dantzig')
    gtime = time.time() - gtime
    rgtime = time.time()
    rg.min_cost_flow(algo="simplex", pivot='dantzig')
    rgtime = time.time() - rgtime
    run_time['Simplex']['gimpy'].append(gtime)
    run_time['Simplex']['regimpy'].append(rgtime)

def write_result_files():
    '''
    Write results using run_time to result_file
    run_time dictionary keys are modules and values are {algo: list of run-time in secs}
    '''
    for a in algo:
        result_file[a] = open(a+'.txt', 'w')
        result_file[a].write("Runing time comparison for "+a+"\n")
        result_file[a].write("# instance    gimpy_time    regimpy_time    theoretical_time\n")
        for s in range(len(run_time[a]['gimpy'])):
            result_file[a].write("  ")
            result_file[a].write(str(s).ljust(8))
            result_file[a].write("    ")
            result_file[a].write(str(run_time[a]['gimpy'][s]).ljust(10))
            result_file[a].write("    ")
            result_file[a].write(str(run_time[a]['regimpy'][s]).ljust(12))
            result_file[a].write("    ")
            result_file[a].write(str(run_time[a]['theoretical'][s]).ljust(16))
            result_file[a].write("\n")
        result_file[a].close()

def insert_theoretical_runing_times(rg):
    # number of nodes
    n = rg.get_node_num()
    # number of edges
    m = rg.get_edge_num()
    # determine C, maximum cost
    C = 0
    for e in rg.get_edge_list():
        cost_e = rg.edge_attr[e]['cost']
        if C<cost_e:
            C = cost_e
    # determine U, max arc capacity
    U = 0
    for e in rg.get_edge_list():
        capacity_e = rg.edge_attr[e]['capacity']
        if U<capacity_e:
            U = capacity_e
    # insert DFS O(n+m)
    tt = n+m
    run_time['DFS']['theoretical'].append(tt)
    # insert BFS O(n+m)
    run_time['BFS']['theoretical'].append(tt)
    # insert Dijsktra with binary heap O((n+m) log n)
    tt = (n+m) * math.log(n)
    run_time['Dijkstra']['theoretical'].append(tt)
    # insert Kruskal with DisjointSet O(m log n)
    tt = m * math.log(n)
    run_time['Kruskal']['theoretical'].append(tt)
    # insert Prim with binary heap O(m log n)
    tt = m * math.log(n)
    run_time['Prim']['theoretical'].append(tt)
    # insert PreflowPush with FIFO O(n^3)
    tt = n*n*n
    run_time['PreflowPush']['theoretical'].append(tt)
    # insert AugmentingPath O(n m^2)
    tt = n*m*m
    run_time['AugmentingPath']['theoretical'].append(tt)
    # insert CycleCanceling O(n m^2 C U), C for cost U for arc capacity
    tt = n*m*m*C*U
    run_time['CycleCanceling']['theoretical'].append(tt)
    # insert Simplex, with Dantzig's pivot rule O(n^2 m log(nC))
    tt = n*n*m*math.log(n*C)
    run_time['Simplex']['theoretical'].append(tt)

def produce_graphs():
    '''
    Compare runing time of reimplementation with theoretical and old gimpy with
    theoretical.
    '''
    # get number of runs, common for all graphs
    n = range(len(run_time['DFS']['theoretical']))
    for a in algo:
        # ========= reimplementation
        # create graph for algorithm a
        scale = run_time[a]['regimpy'][-1] / run_time[a]['theoretical'][-1]
        scaled_theoretical = [scale*t for t in run_time[a]['theoretical']]
        pyplot.plot(n, run_time[a]['regimpy'], 'bs', label='actual runtime')
        pyplot.plot(n, scaled_theoretical, 'g^', label='theoretical runtime')
        pyplot.legend(loc='lower right')
        pyplot.title('regimpy '+a+' running time vs theoretical')
        pyplot.xlabel('instances')
        pyplot.ylabel('running time')
        print a+"_regimpy.png written to disk."
        pyplot.savefig(a+'_regimpy.png')
        pyplot.close()
        # ========= old gimpy
        # create graph for algorithm a
        scale = run_time[a]['gimpy'][-1] / run_time[a]['theoretical'][-1]
        scaled_theoretical = [scale*t for t in run_time[a]['theoretical']]
        pyplot.plot(n, run_time[a]['gimpy'], 'bs', label='actual runtime')
        pyplot.plot(n, scaled_theoretical, 'g^', label='theoretical runtime')
        pyplot.legend(loc='lower right')
        pyplot.title('old gimpy '+a+' running time vs theoretical')
        pyplot.xlabel('instances')
        pyplot.ylabel('running time')
        print a+"_gimpy.png written to disk."
        pyplot.savefig(a+'_gimpy.png')
        pyplot.close()

if __name__=='__main__':
    nr_seed = 1
    for i in range(nr_seed):
        print "Seed", i
        for gen in dense_generator:
            print gen
            # unzip generator
            (numnodes, density, demand_numnodes, supply_numnodes,
             demand_range, cost_range, capacity_range) = gen
            # generate graphs
            #g, rg = generate_graph(i+1)
            g = None
            rg = generate_graph(i+1)
            print "Testing DFS..."
            test_DFS(g, rg)
            print "Testing BFS..."
            test_BFS(g, rg)
            print "Testing Dijkstra..."
            test_dijkstra(g, rg)
            print "Testing Kruskal..."
            test_kruskal(g, rg)
            print "Testing Prim..."
            test_prim(g, rg)
            print "Testing PreflowPush..."
            test_preflow_push(g, rg)
            print "Testing augmenting path..."
            test_augmenting_path(g, rg)
            print "Testing cycle canceling..."
            test_cycle_canceling(g, rg)
            print "Testing network simplex..."
            test_network_simplex(g, rg)
            insert_theoretical_runing_times(rg)
    write_result_files()
    produce_graphs()
