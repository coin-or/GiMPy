GiMPy 1.3
=========

Graph Methods in Python (GiMPy) is a Python graph library containing pure
Python implementations of a variety of graph algorithms. The goal is clarity
in implementation rather than eficiency. Most methods have an accompanying
visualization and are thus appropriate for use in the classroom.

Documentation for the API is here:

http://pythonhosted.org/coinor.gimpy

Installation:

easy_install coinor.gimpy

##Installation Notes

GIMPy depends on [GiMPy](https://github.com/coin-or/GiMPy), which will be 
automatically installed as part of the setup. However, in order for GiMPy to
visualize the branch-and-bound tree, it's necessary to install 
[GraphViz](http://www.graphviz.org/Download.php) and choose one of these 
additional methods for display:
  * Recommanded: [xdot](https://pypi.python.org/pypi/xdot) along with 
    [PyGtk](http://www.pygtk.org/) and call `set_display_mode('xdot')`
  * [Python Imaging Library](http://www.pythonware.com/products/pil/) and 
    call `set_display_mode('PIL')`
  * [Pygame](pygame.org) and call `set_display_mode('pygame')`
  * Call `set_display_mode('file')` to just write files to disk that have to
    then be opened manually. 

##Examples

###Forestry Model
![Forestry](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/forestry.png)
###Display Window in XDot
![XDot](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/xdot.png)
###Lehigh ISE Prerequisite Graph
![ISE Prerequisites](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/ISERequirements.png)
###Graph of Actors Starring Together in Movies in IMDB
![Bacon](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/bacon.png)
###Branch and Bound Tree
![Branch and Bound](https://raw.githubusercontent.com/tkralphs/GrUMPy/master/images/BranchAndBound.png)
###SAT Game Tree
![SAT](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/Turing.png)
###Flow Problem
![Max Flow](https://raw.githubusercontent.com/tkralphs/GiMPy/master/images/maxflow.png)

