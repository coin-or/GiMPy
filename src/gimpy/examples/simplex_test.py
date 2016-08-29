'''
tests network simplex method and cycle canceling method of GIMPy.

'''

from coinor.gimpy import Graph, DIRECTED_GRAPH
from random import seed, randint, random
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, value, GLPK
import time

# global variables, experimental parameters
capacity_range = (10,20)
cost_range = (30,50)
demand_range = (10,15)
demand_numnodes = 3
supply_numnodes = 2
numnodes = 6
density = 0.4

#testing
# nodes       10, 15, 20, 25, 30
# arcs sparse 20, 30, 45, 65, 90
# arcs dense  35, 80, 150, 200, 300

def get_solution(g):
    '''
    returns optimal solution (optimal flows) of min cost flow problem for a
    given graph instance g. return type is dictionary, keys are edge keys values
    are int.
    '''
    sol = {}
    for e in g.get_edge_list():
        sol[e] = g.get_edge_attr(e[0],e[1],'flow')
    return sol

def generate_graph(seed_i):
    g = mGraph(type=DIRECTED_GRAPH, splines='true', layout = 'dot')
    #g = mGraph(type=DIRECTED_GRAPH)
    seed(seed_i)
    for i in range(numnodes):
        for j in range(numnodes):
            if i==j:
                continue
            if (i, j) in g.get_edge_list():
                continue
            if (j, i) in g.get_edge_list():
                continue
            if random() < density:
                cap = randint(capacity_range[0], capacity_range[1])
                cos = randint(cost_range[0], cost_range[1])
                g.add_edge(i, j, cost=cos, capacity=cap)
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
    for n in g.get_node_list():
        if n in demand_node:
            g.set_node_attr(n, 'demand', -1*demand_node[n])
        elif n in supply_node:
            g.set_node_attr(n, 'demand', supply_node[n])
        else:
            g.set_node_attr(n, 'demand', 0)
    return g, demand_node, supply_node

def get_obj_value(g):
    el = g.get_edge_list()
    cost = 0
    for e in el:
        cost_e = g.get_edge_attr(e[0], e[1], 'cost')
        flow_e = g.get_edge_attr(e[0], e[1], 'flow')
        cost += cost_e*flow_e
    return cost

def solve(g):
    el = g.get_edge_list()
    nl = g.get_node_list()
    p = LpProblem('min_cost', LpMinimize)
    capacity = {}
    cost = {}
    demand = {}
    x = {}
    for e in el:
        capacity[e] = g.get_edge_attr(e[0], e[1], 'capacity')
        cost[e] = g.get_edge_attr(e[0], e[1], 'cost')
    for i in nl:
        demand[i] = g.get_node_attr(i, 'demand')
    for e in el:
        x[e] = LpVariable("x"+str(e), 0, capacity[e])
    # add obj
    objective = lpSum (cost[e]*x[e] for e in el)
    p += objective
    # add constraints
    for i in nl:
        out_neig = g.get_out_neighbors(i)
        in_neig = g.get_in_neighbors(i)
        p += lpSum(x[(i,j)] for j in out_neig) -\
             lpSum(x[(j,i)] for j in in_neig)==demand[i]
    p.solve()
    return x, value(objective)

class mGraph(Graph):

    def __init__(self, **attrs):
        Graph.__init__(self, **attrs)

    def network_simplex(self, display, pivot, root):
        '''
        API:
            network_simplex(self, display, pivot)
        Description:
            Solves minimum cost feasible flow problem using network simplex
            algorithm. It is recommended to use min_cost_flow(algo='simplex')
            instead of using network_simplex() directly. Returns True when an
            optimal solution is found, returns False otherwise. 'flow' attribute
            values of arcs should be considered as junk when returned False.
        Pre:
            (1) check Pre section of min_cost_flow()
        Inputs:
            pivot: specifies pivot rule. Check min_cost_flow()
            display: 'off' for no display, 'pygame' for live update of
            spanning tree.
        Post:
            (1) Changes 'flow' attribute of edges.
        Return:
            Returns True when an optimal solution is found, returns
            False otherwise.
        '''
        # ==== determine an initial tree structure (T,L,U)
        # find a feasible flow
        iter = 0
        if not self.find_feasible_flow():
            return (False, iter)
        t = self.simplex_find_tree()
        # mark spanning tree arcs
        self.simplex_mark_st_arcs(t)
        self.set_display_mode(display)
        # display initial spanning tree
        self.display()
        self.set_display_mode('off')
        # set predecessor, depth and thread indexes
        t.simplex_search(root, 1)
        # compute potentials
        self.simplex_compute_potentials(t, root)
        # while some nontree arc violates optimality conditions
        while not self.simplex_optimal(t):
            self.set_display_mode(display)
            self.display()
            self.set_display_mode('off')
            # select an entering arc (k,l)
            (k,l) = self.simplex_select_entering_arc(t, pivot)
            self.simplex_mark_entering_arc(k, l)
            # determine leaving arc
            ((p,q), capacity, cycle)=self.simplex_determine_leaving_arc(t,k,l)
            # mark leaving arc
            self.simplex_mark_leaving_arc(p, q)
            self.set_display_mode(display)
            # display after marking leaving arc
            self.display()
            self.simplex_mark_st_arcs(t)
            self.display()
            self.set_display_mode('off')
            # remove arc
            self.simplex_remove_arc(t, p, q, capacity, cycle)
            # set predecessor, depth and thread indexes
            t.simplex_search(root, 1)
            # compute potentials
            self.simplex_compute_potentials(t, root)
        return (True, iter)

if __name__=='__main__':
    print
    dantzig_file = open('dantzig_results.txt', 'w')
    eligible_file = open('eligible_results.txt', 'w')
    dantzig_file.write('# seed, simplex obj value, pulp obj value,'+\
                           ' time, iteration\n')
    eligible_file.write('# seed, simplex obj value, pulp obj value,'+\
                            ' time, iteration\n')
    for seed_i in range(0,100):
        g, d, s = generate_graph(seed_i)
        root = 0
        #==========solve using simplex, first eligible
        start = time.clock()
        tup = g.network_simplex('pygame', 'first_eligible', root)
        elapsed_time = time.clock() - start
        if tup[0]:
            sol = get_solution(g)
            eligible_obj_value = get_obj_value(g)
        else:
            # skip infeasible ones
            continue
            # set obj value to 0 if the problem is infeasible.
            eligible_obj_value = 0.0
        #==========solve using pulp
        x, pulp_obj_value = solve(g)
        pulp_obj_value = int(pulp_obj_value)
        # check success of simplex with first eligible
        flag = True
        if eligible_obj_value != pulp_obj_value:
            flag = False
        e_line = str(seed_i).ljust(5)+str(eligible_obj_value).ljust(6)+\
            str(pulp_obj_value).ljust(6)+str(elapsed_time).ljust(7)+str(tup[1])+'\n'
        eligible_file.write(e_line)
        #==========solve using simplex, dantzig
        start = time.clock()
        tup = g.network_simplex('pygame', 'dantzig', root)
        elapsed_time = time.clock() - start
        if tup[0]:
            sol = get_solution(g)
            dantzig_obj_value = get_obj_value(g)
        else:
            # set obj value to 0 if the problem is infeasible.
            simplex_obj_value = 0.0
        # write to file
        d_line = str(seed_i).ljust(5)+str(dantzig_obj_value).ljust(6)+\
            str(pulp_obj_value).ljust(6)+str(elapsed_time).ljust(7)+str(tup[1])+'\n'
        dantzig_file.write(d_line)
        flag = True
        if dantzig_obj_value != pulp_obj_value:
            flag = False
    dantzig_file.close()
    eligible_file.close()
    if flag:
        print 'All problems solved accurately.'
