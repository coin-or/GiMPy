from gimpy import Graph

if __name__=="__main__":
    g = Graph(display='PIL', layout='dot')
    g.random(numnodes= 20, density =0.2)
    g.display(basename='g', format='png')
