from gimpy import Graph

if __name__=='__main__':
    g = Graph()
    g.add_edge(1,2)
    g.add_edge(1,3)
    g.add_edge(3,4)
    g.add_edge(3,5)
    g.add_edge(2,4)
    g.add_edge(6,7)
    g.add_edge(7,8)
    g.add_edge(7,9)
    g.label_components()
    print 'done 1'
    g.set_display_mode('pygame')
    g.label_components(display='pygame')
    print 'done 2'
    #g.set_display_mode('pygame')

