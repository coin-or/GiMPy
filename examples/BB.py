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

from pulp import *
import math
import time
from gimpy import Tree, BinaryTree, BBTree
from Queues import PriorityQueue
from random import randint, seed

#from milp3 import CONSTRAINTS, VARIABLES, OBJ, MAT, RHS

##the number of variables and constraints
#numVars = len(VARIABLES)
#numCons = len(CONSTRAINTS)

seed(2)
numVars = 20
numCons = 6
maxObjCoeff = 20
maxConsCoeff = 20
CONSTRAINTS = ["C"+str(i) for i in range(numCons)]
VARIABLES = ["x"+str(i) for i in range(numVars)]
OBJ = {i : randint(1, maxObjCoeff) for i in VARIABLES}
MAT = {i : [randint(1, maxConsCoeff) for j in CONSTRAINTS]
       for i in VARIABLES}
RHS = [randint(1, numVars*maxConsCoeff/2) for i in CONSTRAINTS]

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
search_strategy = DEPTH_FIRST

# 1 to force complete enumeration of nodes (no fathoming by bounding)
complete_enumeration = 0

# List shows if the corresponding variable is fixed to 0 or 1 or if it is not 
# fixed when the corresponding value is 2.
# Initially each variable is assigned to be unfixed

INFINITY = 9999

#The initial lower bound 
LB = 0

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

T = BBTree()
T.set_display_mode('pygame')

# List of candidate nodes
Q = PriorityQueue()

# The current tree depth
cur_depth = 0
cur_index = 0

# Timer
timer = time.time()

Q.push((0, None, None, None), INFINITY)

# Branch and Bound Loop
while not Q.isEmpty():

    cur_index, parent, branch_var, branch_value = Q.pop()
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
    fixed_vars = []
    if cur_index is not 0:
        sys.stdout.write("Fixed variables: ")
        fixed_vars. append(branch_var)
        prob += LpConstraint(lpSum(var[branch_var]) == branch_value)   
        print branch_var,
        pred = parent
        while str(pred) is not '0':
            fixed_var = T.get_node_attr(pred, 'branch_var')
            fixed_value = T.get_node_attr(pred, 'branch_value')
            prob += LpConstraint(lpSum(var[fixed_var]) == fixed_value)
            print fixed_var,
            fixed_vars.append(fixed_var)
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
    elif infeasible:
        print "Infeasible node"
        status = 'I'
    elif not complete_enumeration and relax <= LB:
        print "Node pruned by bound (obj: %s, UB: %s)" %(relax,LB)
        status = 'P'
    elif cur_depth >= numVars :
        print "Reached a leaf"
        status = 'L'
    else:
        status = 'C'

    if status is not 'I':
        label = status + ": " + "%.1f"%relax
    else:
        label = 'I'

    if iter_count == 0:
        T.add_root(0, label = label, status = status)
        T.write_as_svg(filename = "node%d" % iter_count, 
                       nextfile = "node%d" % (iter_count + 1), 
                       highlight = cur_index)
    else:
        T.add_child(cur_index, parent, label = label, branch_var = branch_var,
                    branch_value = branch_value, status = status)
        T.set_edge_attr(parent, cur_index, 'label', 
                        str(branch_var) + ': ' + str(branch_value))
        T.write_as_svg(filename = "node%d" % iter_count, 
                       prevfile = "node%d" % (iter_count - 1), 
                       nextfile = "node%d" % (iter_count + 1), 
                       highlight = cur_index)
    iter_count += 1

#    T.display(highlight = [cur_index])

    if status == 'C':
  
        # Branching:
        # Choose a variable for branching
        branching_var = -1
        if branch_strategy == FIXED:
            #fixed order
            for i in VARIABLES:
                if i not in fixed_vars:
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
                if i not in fixed_vars:
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
        Q.push((node_count, cur_index, branching_var, math.floor(var[branching_var].varValue)), priority)
        node_count += 1
        Q.push((node_count, cur_index, branching_var, math.ceil(var[branching_var].varValue)), priority)
 
timer = int(math.ceil((time.time()-timer)*1000))

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
