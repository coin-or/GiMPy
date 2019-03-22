#List of constraint index
CONSTRAINTS = ["Capacity", "Budget", "Cardinality"]

#Dictionary of objective function coefficients of variables
OBJ = {"x1" : 4,
       "x2" : 1,
       "x3" : 3,
       "x4" : 4,
       "x5" : 8,
       "x6" : 9,
       "x7" : 11,
       "x8" : 1,
       "x9" : 2,
       "x10": 0,
       "x11": 3,
       "x12": 1,
       "x13": 2,
       "x14": 3,
       "x15": 1}

#Dictionary of variable coefficients in each constraint (column)
MAT = {"x1" : [2, 7, 1], 
       "x2" : [4, 2, 1], 
       "x3" : [1, 3, 1], 
       "x4" : [6, 5, 1], 
       "x5" : [2, 1, 1], 
       "x6" : [5, 7, 1], 
       "x7" : [9, 6, 1], 
       "x8" : [4, 4, 1], 
       "x9" : [2, 1, 1], 
       "x10": [1, 0, 1], 
       "x11": [3, 2, 1], 
       "x12": [3, 3, 1], 
       "x13": [3, 7, 1], 
       "x14": [5, 9, 1], 
       "x15": [2, 2, 1]}

#Right hand side of the constraints
RHS = [29, 35, 8]

#List of variable indices
VARIABLES = list(OBJ.keys())
VARIABLES.sort()

VARIABLES = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", 
             "x11", "x12", "x13", "x14", "x15"]