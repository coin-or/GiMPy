from gimpy import Graph

if __name__=="__main__":
    g = Graph(display='pygame', layout='dot')
    g.random(numnodes= 20, density =0.2)
    # test pygame
    g.display()
    # test xdot
    g.set_display_mode('xdot')
    g.display()
    # test file, layout dot
    g.set_display_mode('file')
    g.display(basename='test')
    # test file, layout dot2tex
    g.set_display_mode('file')
    g.set_layout('dot2tex')
    g.display()
    # test PIL
    g.set_layout('dot')
    g.set_display_mode('PIL')
    g.display()

