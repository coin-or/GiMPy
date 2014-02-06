'''
This file has global constants required for GIMPy.
'''

import re     # for compile()

class MultipleNodeException(Exception):
    pass

class MultipleEdgeException(Exception):
    pass

GRAPH_ATTRIBUTES = set( ['Damping', 'K', 'URL', 'aspect', 'bb', 'bgcolor',
    'center', 'charset', 'clusterrank', 'colorscheme', 'comment', 'compound',
    'concentrate', 'defaultdist', 'dim', 'dimen', 'diredgeconstraints',
    'dpi', 'epsilon', 'esep', 'fontcolor', 'fontname', 'fontnames',
    'fontpath', 'fontsize', 'id', 'label', 'labeljust', 'labelloc',
    'landscape', 'layers', 'layersep', 'layout', 'levels', 'levelsgap',
    'lheight', 'lp', 'lwidth', 'margin', 'maxiter', 'mclimit', 'mindist',
    'mode', 'model', 'mosek', 'nodesep', 'nojustify', 'normalize', 'nslimit',
    'nslimit1', 'ordering', 'orientation', 'outputorder', 'overlap',
    'overlap_scaling', 'pack', 'packmode', 'pad', 'page', 'pagedir',
    'quadtree', 'quantum', 'rankdir', 'ranksep', 'ratio', 'remincross',
    'repulsiveforce', 'resolution', 'root', 'rotate', 'searchsize', 'sep',
    'showboxes', 'size', 'smoothing', 'sortv', 'splines', 'start',
    'stylesheet', 'target', 'truecolor', 'viewport', 'voro_margin',
    'd2tgraphstyle',
    # for subgraphs
    'rank'])
DEFAULT_GRAPH_ATTRIBUTES = {}
EDGE_ATTRIBUTES = set( ['URL', 'arrowhead', 'arrowsize', 'arrowtail',
    'color', 'colorscheme', 'comment', 'constraint', 'decorate', 'dir',
    'edgeURL', 'edgehref', 'edgetarget', 'edgetooltip', 'fontcolor',
    'fontname', 'fontsize', 'headURL', 'headclip', 'headhref', 'headlabel',
    'headport', 'headtarget', 'headtooltip', 'href', 'id', 'label',
    'labelURL', 'labelangle', 'labeldistance', 'labelfloat', 'labelfontcolor',
    'labelfontname', 'labelfontsize', 'labelhref', 'labeltarget',
    'labeltooltip', 'layer', 'len', 'lhead', 'lp', 'ltail', 'minlen',
    'nojustify', 'penwidth', 'pos', 'samehead', 'sametail', 'showboxes',
    'style', 'tailURL', 'tailclip', 'tailhref', 'taillabel', 'tailport',
    'tailtarget', 'tailtooltip', 'target', 'tooltip', 'weight',
    'rank' ] )
DEFAULT_EDGE_ATTRIBUTES = {}
NODE_ATTRIBUTES = set( ['URL', 'color', 'colorscheme', 'comment',
    'distortion', 'fillcolor', 'fixedsize', 'fontcolor', 'fontname',
    'fontsize', 'group', 'height', 'id', 'image', 'imagescale', 'label',
    'labelloc', 'layer', 'margin', 'nojustify', 'orientation', 'penwidth',
    'peripheries', 'pin', 'pos', 'rects', 'regular', 'root', 'samplepoints',
    'shape', 'shapefile', 'showboxes', 'sides', 'skew', 'sortv', 'style',
    'target', 'tooltip', 'vertices', 'width', 'z',
    # The following are attributes dot2tex
    'texlbl',  'texmode' ] )
DEFAULT_NODE_ATTRIBUTES = {}
CLUSTER_ATTRIBUTES = set( ['K', 'URL', 'bgcolor', 'color', 'colorscheme',
    'fillcolor', 'fontcolor', 'fontname', 'fontsize', 'label', 'labeljust',
    'labelloc', 'lheight', 'lp', 'lwidth', 'nojustify', 'pencolor',
    'penwidth', 'peripheries', 'sortv', 'style', 'target', 'tooltip'] )
DIRECTED_GRAPH = 'digraph'
UNDIRECTED_GRAPH = 'graph'
#DEFAULT_ATTR = {'strict':None, 'name':'graph'}
EDGE_CONNECT_SYMBOL = {DIRECTED_GRAPH:' -> ', UNDIRECTED_GRAPH:' -- '}
PYGAME_INSTALLED = None # it wil be set when we try to import pygame
DOT2TEX_INSTALLED = None # it wil be set when we try to import
PIL_INSTALLED = None
XDOT_INSTALLED = None
ETREE_INSTALLED = None
INF = 10000

DOT2TEX_TEMPLATE = r'''
\documentclass[landscape]{article}
\usepackage[x11names, rgb]{xcolor}
\usepackage[<<textencoding>>]{inputenc}
\usepackage{tikz}
\usetikzlibrary{snakes,arrows,shapes}
\usepackage{amsmath}
\usepackage[margin=2cm,nohead]{geometry}%
<<startpreprocsection>>%
\usepackage[active,auctex]{preview}
<<endpreprocsection>>%
<<gvcols>>%
<<cropcode>>%
<<docpreamble>>%

\begin{document}
\pagestyle{empty}
%
<<startpreprocsection>>%
<<preproccode>>
<<endpreprocsection>>%
%
<<startoutputsection>>
\enlargethispage{100cm}
% Start of code
% \begin{tikzpicture}[anchor=mid,>=latex',join=bevel,<<graphstyle>>]
\resizebox{\textwidth}{!}{
\begin{tikzpicture}[>=latex',join=bevel,<<graphstyle>>]
\pgfsetlinewidth{1bp}
<<figpreamble>>%
<<drawcommands>>
<<figpostamble>>%
\end{tikzpicture}
% End of code
}
<<endoutputsection>>
%
\end{document}
%
<<startfigonlysection>>
\begin{tikzpicture}[>=latex,join=bevel,<<graphstyle>>]
\pgfsetlinewidth{1bp}
<<figpreamble>>%
<<drawcommands>>
<<figpostamble>>%
\end{tikzpicture}
<<endfigonlysection>>
'''

# following globals and two methods are from pydot
DOT_KEYWORDS = ['graph', 'subgraph', 'digraph', 'node', 'edge', 'strict']
ID_RE_ALPHA_NUMS = re.compile('^[_a-zA-Z][a-zA-Z0-9_,]*$', re.UNICODE)
ID_RE_ALPHA_NUMS_WITH_PORTS = re.compile('^[_a-zA-Z][a-zA-Z0-9_,:\"]*[a-zA-Z0-9_,\"]+$', re.UNICODE)
ID_RE_NUM = re.compile('^[0-9,]+$', re.UNICODE)
ID_RE_WITH_PORT = re.compile('^([^:]*):([^:]*)$', re.UNICODE)
ID_RE_DBL_QUOTED = re.compile('^\".*\"$', re.S|re.UNICODE)
ID_RE_HTML = re.compile('^<.*>$', re.S|re.UNICODE)

def quote_if_necessary(s):
    if isinstance(s, bool):
        if s is True:
            return 'True'
        return 'False'
    if not isinstance(s, basestring):
        return s
    if not s:
        return s
    if needs_quotes(s):
        replace = {'"'  : r'\"',
                   "\n" : r'\n',
                   "\r" : r'\r',
                   "\\ " : r'\\ '}
        for (a,b) in replace.items():
            s = s.replace(a, b)
        return '"' + s + '"'
    return s

def needs_quotes(s):
    """Checks whether a string is a dot language ID.
    It will check whether the string is solely composed
    by the characters allowed in an ID or not.
    If the string is one of the reserved keywords it will
    need quotes too but the user will need to add them
    manually.
    """
    # If the name is a reserved keyword it will need quotes but pydot
    # can't tell when it's being used as a keyword or when it's simply
    # a name. Hence the user needs to supply the quotes when an element
    # would use a reserved keyword as name. This function will return
    # false indicating that a keyword string, if provided as-is, won't
    # need quotes.
    if s in DOT_KEYWORDS:
        return False
    chars = [ord(c) for c in s if ord(c)>0x7f or ord(c)==0]
    if chars and not ID_RE_DBL_QUOTED.match(s) and not ID_RE_HTML.match(s):
        return True
    for test_re in [ID_RE_ALPHA_NUMS, ID_RE_NUM, ID_RE_DBL_QUOTED, ID_RE_HTML, ID_RE_ALPHA_NUMS_WITH_PORTS]:
        if test_re.match(s):
            return False
    m = ID_RE_WITH_PORT.match(s)
    if m:
        return needs_quotes(m.group(1)) or needs_quotes(m.group(2))
    return True
