# import classes
from coinor.gimpy import Graph, Tree, BinaryTree
# import dependency related globals. All these dependencies are optional.
# They all provide different display capabilities. If some of them are missing
# it means you only miss the display capability provided by it.
from coinor.gimpy import DOT2TEX_INSTALLED, PIL_INSTALLED
from coinor.gimpy import XDOT_INSTALLED, MATPLOTLIB_INSTALLED

if DOT2TEX_INSTALLED:
    print('Dot2tex is installed.')
elif not DOT2TEX_INSTALLED:
    print('Dot2tex not installed.')
if PIL_INSTALLED:
    print('PIL (Python Imaging Library) is installed.')
elif not PIL_INSTALLED:
    print('PIL (Python Imaging Library) not installed.')
if XDOT_INSTALLED:
    print('Xdot is installed.')
elif not XDOT_INSTALLED:
    print('Xdot not installed.')
if MATPLOTLIB_INSTALLED:
    print('Matplotlib is installed.')
elif not MATPLOTLIB_INSTALLED:
    print('Matplotlib not installed.')

if __name__=="__main__":
    g = Graph(display='off', layout='dot')
    g.random(numnodes= 20, density =0.2)
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
    # test mtaplotlib
    g.set_display_mode('matplotlib')
    g.display()

