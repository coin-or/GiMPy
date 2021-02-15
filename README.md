# GiMPy 2.1

[![DOI](https://zenodo.org/badge/18214894.svg)](https://zenodo.org/badge/latestdoi/18214894)

Graph Methods in Python (GiMPy) is a Python graph library containing pure
Python implementations of a variety of graph algorithms. The goal is clarity
in implementation rather than eficiency. Most methods have an accompanying
visualization and are thus appropriate for use in the classroom.

Documentation for the API is here:

https://coin-or.github.io/GiMPy

Pypi download page is here:

https://pypi.python.org/pypi/coinor.gimpy

## Installation Notes

To install, do
```
pip install coinor.gimpy
```

In order for GiMPy to visualize the graphs it produces, it's necessary to install 
  [GraphViz](http://www.graphviz.org/Download.php) (**Important**: after installing
  graphviz, you must add the graphviz `bin` directory, usually 
  `C:\Program Files (x86)\Graphviz2.38\bin`, to your `PATH`) 
  and choose one of these additional methods for display:
  * Recommended: [matplotlib](https://pypi.org/project/matplotlib/) and call
    `set_display_mode('matplotlib')
  * [Python Imaging Library](http://www.pythonware.com/products/pil/) and 
    call `set_display_mode('PIL')`
  * Call `set_display_mode('file')` to just write files to disk that have to
    then be opened manually. 

It is also possible to typeset labels in LaTex and to output the graph in 
LaTex format using `dot2tex`. After installing `dot2tex`, this can be done 
by simply calling the method `write(basename='fileName', format='dot')`, and 
then doing `dot2tex --tmath fileName.dot` or by calling 
`set_display_mode('dot2tex')` and then `display()` as usual. At the moment,
the latter only seems to work with version `2.9.0dev` available 
[here](https://github.com/Alwnikrotikz/dot2tex). For the former method, just 
using `easy_install dot2tex` should work fine.

# Additional Notes for Windows Installation

  * To install Graphviz, download the installer [here](http://www.graphviz.org/Download.php). **Important**: after installing, you must manually add the graphviz `bin` directory (usually `C:\Program Files (x86)\Graphviz2.38\bin`) to your `PATH` 
  * If you want to use `xdot`, there are some more requirements: 
     * Unfortunately, you must have a 32-bit version of Python 2.7
     * You must install the [PyGtk version 2.22.6](http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.22/pygtk-all-in-one-2.22.6.win32-py2.7.msi). Version 2.24 is buggy on Windows.
     * To install `gnuplot`, download the installer [here](https://sourceforge.net/projects/gnuplot/). Note that the CYGWIN version of gnuplot may not work when called from Python.  

# Additional Notes for Linux Installation

  * Graphviz can be installed as a package on most Linux distros, e.g., `sudo apt-get install graphviz`
  
# Additional Notes for OS X Users

  * The situation with Python on OS X is a bit of a mess. It is recommended to install python using [homebrew](http://brew.sh) with `brew install python`).
  * With homebbrew, one can also easily install graphviz (`brew install graphviz`).

## Examples

### Forestry Model
![Forestry](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/forestry.png)
### Display Window in XDot
![XDot](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/xdot.png)
### Lehigh ISE Prerequisite Graph
![ISE Prerequisites](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/ISERequirements.png)
### Graph of Actors Starring Together in Movies in IMDB
![Bacon](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/bacon.png)
### Branch and Bound Tree
![Branch and Bound](https://raw.githubusercontent.com/coin-or/GrUMPy/master/images/BranchAndBound.png)
### SAT Game Tree
![SAT](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/Turing.png)
### Flow Problem
![Max Flow](https://raw.githubusercontent.com/coin-or/GiMPy/master/images/maxflow.png)

