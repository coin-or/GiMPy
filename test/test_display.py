# import classes
from gimpy import Graph, Tree, BinaryTree
# import dependency related globals. All these dependencies are optional.
# They all provide different display capabilities. If some of them are missing
# it means you only miss the display capability provided by it.
from gimpy import PYGAME_INSTALLED, DOT2TEX_INSTALLED, PIL_INSTALLED
from gimpy import XDOT_INSTALLED, ETREE_INSTALLED

if PYGAME_INSTALLED:
    print 'Pygame is installed.'
elif not PYGAME_INSTALLED:
    print 'Warning: Pygame can not found.'
if DOT2TEX_INSTALLED:
    print 'Dot2tex is installed.'
elif not DOT2TEX_INSTALLED:
    print 'Warning: Dot2tex can not found.'
if PIL_INSTALLED:
    print 'PIL (Python Imaging Library) is installed.'
elif not PIL_INSTALLED:
    print 'Warning: PIL (Python Imaging Library) can not found.'
if XDOT_INSTALLED:
    print 'Xdot is installed.'
elif not XDOT_INSTALLED:
    print 'Warning: Xdot can not found.'
if ETREE_INSTALLED:
    print 'Etree is installed.'
elif not ETREE_INSTALLED:
    print 'Warning: Etree can not found.'

if __name__=="__main__":
    g = Graph(display='off', layout='dot')
    g.random(numnodes= 20, density =0.2)
    # test pygame
    g.set_display_mode('pygame')
    g.display()
    # test xdot
    g.set_display_mode('xdot')
    g.display()
    # test file, layout dot
    g.set_display_mode('file')
    g.display(basename='test_graph')
    # test file, layout dot2tex
    g.set_display_mode('file')
    g.set_layout('dot2tex')
    g.display()
    # test PIL
    g.set_layout('dot')
    g.set_display_mode('PIL')
    g.display()
    # test svg
    g.set_display_mode('svg')
    g.display()

