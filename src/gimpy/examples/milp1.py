#List of constraint index
CONSTRAINTS = ["Capacity"]

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
MAT = {"x1" : [2], 
       "x2" : [4], 
       "x3" : [1], 
       "x4" : [6], 
       "x5" : [2], 
       "x6" : [5], 
       "x7" : [9], 
       "x8" : [4], 
       "x9" : [2], 
       "x10": [1], 
       "x11": [3], 
       "x12": [3], 
       "x13": [3], 
       "x14": [5], 
       "x15": [2]}

#Right hand side of the constraints
RHS = [29]

#List of variable indices
VARIABLES = list(OBJ.keys())
VARIABLES.sort()

