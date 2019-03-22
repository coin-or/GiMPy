from __future__ import print_function
try:
    from src.gimpy import Graph
except ImportError:
    from coinor.gimpy import Graph

if __name__ == '__main__':
    G = Graph(graph_type = 'digraph', splines = 'true', layout = 'dot2tex', 
              display = 'pygame', rankdir = 'LR', fontsize = '44', 
              d2tgraphstyle = 'every text node part/.style={align=left}',
              )
    node_format = {
#                   'height':1.0,
#                   'width':2.0,
#                   'fixedsize':'true',
#                   'fontsize':'36',
#                   'fontcolor':'red',
                    'shape':'rect',
                   }

    G.add_node('0', label = r'C_1 = x_1 \mid x_2$ \\ $C_2 = x_2 \mid x_3', **node_format)
    G.add_node('1', label = r'C_1 = \text{TRUE}$ \\ $C_2 = x_2 \mid x_3', **node_format)
    G.add_node('2', label = r'C_1 = x_2$ \\ $C_2 = x_2 \mid x_3', **node_format)
    G.add_node('3', label = r'C_1 = \text{TRUE}$ \\ $C_2 = \text{TRUE}', color = 'green', **node_format)
    G.add_node('4', label = r'C_1 = \text{TRUE}$ \\ $C_2 = x_3', **node_format)
    G.add_node('5', label = r'C_1 = \text{TRUE}$ \\ $C_2 = \text{TRUE}', color = 'green', **node_format)
    G.add_node('6', label = r'C_1 = \text{FALSE}$ \\ $C_2 = x_3', color = 'red', **node_format)
    G.add_node('9', label = r'C_1 = \text{TRUE}$ \\ $C_2 = \text{TRUE}', color = 'green', **node_format)
    G.add_node('10', label = r'C_1 = \text{FALSE}$ \\ $C_2 = \text{FALSE}', color = 'red', **node_format)
    G.add_edge('0', '1', label = r'x_1 = \text{TRUE}')
    G.add_edge('0', '2', label = r'x_1 = \text{FALSE}')
    G.add_edge('1', '3', label = r'x_2 = \text{TRUE}')
    G.add_edge('1', '4', label = r'x_2 = \text{FALSE}')
    G.add_edge('2', '5', label = r'x_2 = \text{TRUE}')
    G.add_edge('2', '6', label = r'x_2 = \text{FALSE}')
    G.add_edge('4', '9', label = r'x_3 = \text{TRUE}')
    G.add_edge('4', '10', label = r'x_3 = \text{FALSE}')
    
    G.set_display_mode('xdot')

    print(G)

    G.display(basename='Turing')
