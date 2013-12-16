'''
Original Authors : Murat H. Mut, Serdar Yildiz,
                   Lehigh University ISE Department 05/07/2010
Edited by Victor Pillac on Aug 5 2010
Edited by Ted Ralphs September 15, 2011
Reimplemented Using GiMPy by Ted Ralphs February 1, 2013

This code solves an integer program by using an LP-based branch and bound
algorithm. The search strategy is controlled by the priority given to nodes in
the queue and there are two different rules available for solecting the
branching variable (most fractional and fixed). The complete_enumeration
variable can be used to turn off fathoming by bound.

'''

from pulp import LpVariable, lpSum, LpProblem, LpMaximize, LpConstraint, LpStatus, value
import math
import time
from coinor.gimpy import BinaryTree, ETREE_INSTALLED, PYGAME_INSTALLED, XDOT_INSTALLED

#from coinor.gimpy import etree_installed, pygame_installed, xdot_installed
#from coinor.gimpy import Cluster

try:
    from coinor.grumpy import BBTree, gexf_installed
    grumpy_installed = True
except ImportError:
    grumpy_installed = False

from coinor.blimpy import PriorityQueue
from random import random, randint, seed

display_mode = 'xdot'
layout = 'dot'
display_interval = 100
if not grumpy_installed:
    layout = 'dot'

if layout == 'bak' and grumpy_installed:
    T = BBTree()
else:
    T = BinaryTree()
T.set_display_mode(display_mode)
T.set_layout(layout)

'''
#Add key
C = Cluster(graph_name = 'Key', label = 'Key', fontsize = '12')
C.add_node('C', label = 'Candidate', style = 'filled', color = 'yellow', fillcolor = 'yellow')
C.add_node('I', label = 'Infeasible', style = 'filled', color = 'orange', fillcolor = 'orange')
C.add_node('S', label = 'Solution', style = 'filled', color = 'lightblue', fillcolor = 'lightblue')
C.add_node('P', label = 'Pruned', style = 'filled', color = 'red', fillcolor = 'red')
C.add_edge('C', 'I', style = 'invisible', arrowhead = 'none')
C.add_edge('I', 'S', style = 'invisible', arrowhead = 'none')
C.add_edge('S', 'P', style = 'invisible', arrowhead = 'none')
T.add_subgraph(C)
'''

T.add_node('C', label = 'Candidate', style = 'filled', color = 'yellow', fillcolor = 'yellow')
T.add_node('I', label = 'Infeasible', style = 'filled', color = 'orange', fillcolor = 'orange')
T.add_node('S', label = 'Solution', style = 'filled', color = 'lightblue', fillcolor = 'lightblue')
T.add_node('P', label = 'Pruned', style = 'filled', color = 'red', fillcolor = 'red')
T.add_edge('C', 'I', style = 'invisible', arrowhead = 'none')
T.add_edge('I', 'S', style = 'invisible', arrowhead = 'none')
T.add_edge('S', 'P', style = 'invisible', arrowhead = 'none')
cluster_attrs = {'name':'Key', 'label':'Key', 'fontsize':'12'}
T.create_cluster(['C', 'I', 'S', 'P'], cluster_attrs)

import_instance = False
if import_instance:
    from milp2 import CONSTRAINTS, VARIABLES, OBJ, MAT, RHS

    #the number of variables and constraints
    numVars = len(VARIABLES)
    numCons = len(CONSTRAINTS)
else:
    seed(2)
    numVars = 40
    numCons = 20
    density = 0.2
    maxObjCoeff = 10
    maxConsCoeff = 10
    CONSTRAINTS = ["C"+str(i) for i in range(numCons)]
    if layout == 'ladot':
        VARIABLES = ["x_{"+str(i)+"}" for i in range(numVars)]
    else:
        VARIABLES = ["x"+str(i) for i in range(numVars)]
    OBJ = {i : randint(1, maxObjCoeff) for i in VARIABLES}
    MAT = {i : [randint(1, maxConsCoeff) if random() <= density else 0
                for j in CONSTRAINTS] for i in VARIABLES}
    RHS = [randint(int(numVars*density*maxConsCoeff/2), int(numVars*density*maxConsCoeff/1.5)) for i in CONSTRAINTS]

var   = LpVariable.dicts("", VARIABLES, 0, 1)

################################################################

#Branching strategies
MOST_FRAC = "MOST FRACTIONAL"
FIXED = "FIXED"

#search strategies
DEPTH_FIRST = "Depth First"
BEST_FIRST = "Best First"

#Selected branching strategy
branch_strategy = FIXED
search_strategy = BEST_FIRST

# 1 to force complete enumeration of nodes (no fathoming by bounding)
complete_enumeration = 0

# List shows if the corresponding variable is fixed to 0 or 1 or if it is not
# fixed when the corresponding value is 2.
# Initially each variable is assigned to be unfixed
INFINITY = 9999

#The initial lower bound
LB = -INFINITY

#The number of LP's solved, and the number of nodes solved
node_count = 1
iter_count = 0
lp_count = 0

#List of incumbent solution variable values
opt = dict([(i, 0) for i in VARIABLES])

print "==========================================="
print "Starting Branch and Bound"

if branch_strategy == MOST_FRAC:
    print "Most fractional variable"
elif branch_strategy == FIXED:
    print "Fixed order"
else:
    print "Unknown branching strategy %s" %branch_strategy

if search_strategy == DEPTH_FIRST:
    print "Depth first search strategy"
elif search_strategy == BEST_FIRST:
    print "Best first search strategy"
else:
    print "Unknown search strategy %s" %search_strategy

print "==========================================="

# List of candidate nodes
Q = PriorityQueue()

# The current tree depth
cur_depth = 0
cur_index = 0

# Timer
timer = time.time()

Q.push((0, None, None, None, None), INFINITY)

# Branch and Bound Loop
while not Q.isEmpty():

    cur_index, parent, branch_var, sense, rhs = Q.pop()
    if cur_index is not 0:
        cur_depth = T.get_node_attr(parent, 'level') + 1
    else:
        cur_depth = 0

    print ""
    print "----------------------------------------------------"
    print ""
    print "Node: %s, Depth: %s, LB: %s" %(cur_index,cur_depth,LB)

    #====================================
    #    LP Relaxation
    #====================================
    #Compute lower bound by LP relaxation
    prob = LpProblem("relax",LpMaximize)
    prob += lpSum([OBJ[i]*var[i] for i in VARIABLES]), "Objective"
    for j in range(numCons):
        prob += lpSum([MAT[i][j]*var[i] for i in VARIABLES]) <= RHS[j], \
            CONSTRAINTS[j]

    #Fix all prescribed variables
    branch_vars = []
    if cur_index is not 0:
        print "Branching variables: "
        branch_vars.append(branch_var)
        if sense == '>=':
            prob += LpConstraint(lpSum(var[branch_var]) >= rhs)
        else:
            prob += LpConstraint(lpSum(var[branch_var]) <= rhs)
        print branch_var,
        pred = parent
        while str(pred) is not '0':
            pred_branch_var = T.get_node_attr(pred, 'branch_var')
            pred_rhs = T.get_node_attr(pred, 'rhs')
            pred_sense = T.get_node_attr(pred, 'sense')
            if pred_sense == '<=':
                prob += LpConstraint(lpSum(var[pred_branch_var]) <= pred_rhs)
            else:
                prob += LpConstraint(lpSum(var[pred_branch_var]) >= pred_rhs)
            print pred_branch_var,
            branch_vars.append(pred_branch_var)
            pred = T.get_node_attr(pred, 'parent')

    print ""

    # Solve the LP relaxation
    prob.solve()

    lp_count = lp_count +1

    # Check infeasibility
    infeasible = LpStatus[prob.status] == "Infeasible"

    # Print status
    if infeasible:
        print "LP Solved, status: Infeasible"
    else:
        print "LP Solved, status: %s, obj: %s" %(LpStatus[prob.status],
                                                 value(prob.objective))


    if(LpStatus[prob.status] == "Optimal"):
        relax = value(prob.objective)
    else:
        relax = INFINITY

    integer_solution = 0

    if (LpStatus[prob.status] == "Optimal"):
        var_values = dict([(i, var[i].varValue) for i in VARIABLES])
        integer_solution = 1
        for i in VARIABLES:
            if (var_values[i] not in set([0,1])):
                integer_solution = 0
                break
        if (integer_solution and relax>LB):
            LB = relax
            for i in VARIABLES:
                #these two have different data structures first one list
                #second one dictionary
                opt[i] = var_values[i]
            print "New best solution found, objective: %s" %relax
            for i in VARIABLES:
                if var_values[i] > 0:
                    print "%s = %s" %(i, var_values[i])
        elif (integer_solution and relax<=LB):
            print "New integer solution found, objective: %s" %relax
            for i in VARIABLES:
                if var_values[i] > 0:
                    print "%s = %s" %(i, var_values[i])
        else:
            print "Fractional solution:"
            for i in VARIABLES:
                if var_values[i] > 0:
                    print "%s = %s" %(i, var_values[i])

    #For complete enumeration
    if complete_enumeration:
        relax = LB - 1

    if integer_solution:
        print "Integer solution"
        status = 'S'
        BAKstatus = 'integer'
        color = 'lightblue'
    elif infeasible:
        print "Infeasible node"
        status = 'I'
        BAKstatus = 'infeasible'
        color = 'orange'
    elif not complete_enumeration and relax <= LB:
        print "Node pruned by bound (obj: %s, UB: %s)" %(relax,LB)
        status = 'P'
        BAKstatus = 'fathomed'
        color = 'red'
    elif cur_depth >= numVars :
        print "Reached a leaf"
        BAKstatus = 'fathomed'
        status = 'L'
    else:
        status = 'C'
        BAKstatus = 'candidate'
        color = 'yellow'

    if status is not 'I':
#        label = status + ": " + "%.1f"%relax
        label = "%.1f"%relax
    else:
        label = 'I'

    if iter_count == 0:
        if layout == 'bak':
            T.AddOrUpdateNode(0, -1, None, BAKstatus, -relax, None, None)
        else:
            T.add_root(0, label = label, status = status, obj = relax, color = color,
                       style = 'filled', fillcolor = color)
        if ETREE_INSTALLED and display_mode == 'svg':
            T.write_as_svg(filename = "node%d" % iter_count,
                           nextfile = "node%d" % (iter_count + 1),
                           highlight = cur_index)
    else:
        if layout == 'bak':
            if sense == '<=':
                T.AddOrUpdateNode(cur_index, parent, 'L', 'candidate',
                                  -relax, None, None, branch_var = branch_var,
                                  sense = sense, rhs = rhs)
            else:
                T.AddOrUpdateNode(cur_index, parent, 'R', 'candidate',
                                  -relax, None, None, branch_var = branch_var,
                                  sense = sense, rhs = rhs)
        else:
            T.add_child(cur_index, parent, label = label, branch_var = branch_var,
                        sense = sense, rhs = rhs, status = status, obj = relax,
                        color = color, style = 'filled', fillcolor = color)
            if layout == 'ladot':
                if sense == '>=':
                    T.set_edge_attr(parent, cur_index, 'label',
                                    "$"+str(branch_var) + " \geq " + str(rhs) + "$")
                else:
                    T.set_edge_attr(parent, cur_index, 'label',
                                    "$"+str(branch_var) + " \leq " + str(rhs) + "$")
            else:
                T.set_edge_attr(parent, cur_index, 'label',
                                str(branch_var) + sense + str(rhs))
        if ETREE_INSTALLED and display_mode == 'svg':
            T.write_as_svg(filename = "node%d" % iter_count,
                           prevfile = "node%d" % (iter_count - 1),
                           nextfile = "node%d" % (iter_count + 1),
                           highlight = cur_index)
    iter_count += 1

    if ((PYGAME_INSTALLED and display_mode == 'pygame')
         or (XDOT_INSTALLED and display_mode == 'xdot')):
        numNodes = len(T.get_node_list())
        if numNodes % display_interval == 0 and not layout != 'ladot':
            T.display(highlight = [cur_index])
    elif gexf_installed and display_mode == 'gexf':
        T.write_as_dynamic_gexf("graph")

    if status == 'C':

        # Branching:
        # Choose a variable for branching
        branching_var = -1
        if branch_strategy == FIXED:
            #fixed order
            for i in VARIABLES:
                frac = min(var[i].varValue-math.floor(var[i].varValue),
                           math.ceil(var[i].varValue) - var[i].varValue)
                if (frac > 0):
                    min_frac = frac
                    branching_var = i
                    break
        elif branch_strategy == MOST_FRAC:
            #most fractional variable
            min_frac = -1
            for i in VARIABLES:
                frac = min(var[i].varValue-math.floor(var[i].varValue),
                           math.ceil(var[i].varValue)- var[i].varValue )
                if (frac> min_frac):
                    min_frac = frac
                    branching_var = i

        else:
            print "Unknown branching strategy %s" %branch_strategy
            exit()

        if branching_var >= 0:
            print "Branching on variable %s" %branching_var

        #Create new nodes
        if search_strategy == DEPTH_FIRST:
            priority = -cur_depth - 1
        elif search_strategy == BEST_FIRST:
            priority = relax
        node_count += 1
        Q.push((node_count, cur_index, branching_var, '<=', math.floor(var[branching_var].varValue)), priority)
        node_count += 1
        Q.push((node_count, cur_index, branching_var, '>=', math.ceil(var[branching_var].varValue)), priority)
        T.set_node_attr(cur_index, color, 'green')
        if layout == 'bak':
            T.set_node_attr(cur_index, 'status', 'branched')

timer = int(math.ceil((time.time()-timer)*1000))

if ((XDOT_INSTALLED and display_mode == 'xdot' and layout != 'ladot') or
    layout == 'bak'):
    T.display()
if layout == 'ladot':
    T.write_as_dot(filename = 'graph')

print ""
print "==========================================="
print "Branch and bound completed in %sms" %timer
print "Strategy: %s" %branch_strategy
if complete_enumeration:
    print "Complete enumeration"
print "%s nodes visited " %node_count
print "%s LP's solved" %lp_count
print "==========================================="
print "Optimal solution"
#print optimal solution
for i in sorted(VARIABLES):
    if opt[i] > 0:
        print "%s = %s" %(i, opt[i])
print "Objective function value"
print LB
print "==========================================="
