from gimpy import Graph, DIRECTED_GRAPH

if __name__=='__main__':
    #g = Graph(type=DIRECTED_GRAPH)
    g = Graph()
    g.add_edge(0,1,label='aykut')
    g.add_edge(1,2,label='bulut')
    g.get_node(0).set_attr('label', 'ie')
    g.display()
    #f = open('dot_file.txt', 'w')
    #f.write(g.to_string())
    #print g.to_string()
    #cProfile.run('life(int(sys.argv[1]), int(sys.argv[2]))', 'cprof.out')
    #p = pstats.Stats('cprof.out')
    #p.sort_stats('cumulative').print_stats(10)
