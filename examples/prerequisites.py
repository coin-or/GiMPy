try:
    from src.gimpy import Graph
except:
    from coinor.gimpy import Graph

if __name__ == '__main__':
    G = Graph(type = 'digraph', splines = 'true', layout = 'dot',
              display = 'xdot', rankdir = 'LR', label = 'ISE Prerequisite Map',
              fontsize = '80', labelloc = 't', size = "7.5,10.0!", ratio = 'fill',
              esep = '10', ranksep = '1.8',
              )
    node_format = {
#                   'height':1.0,
#                   'width':2.0,
#                   'fixedsize':'true',
                   'fontsize': '36',
#                   'fontcolor':'red',
                    'shape': 'ellipse',
                    'style': 'bold',
                    'fontname': 'Times-Bold' 
                   }

    cluster_attrs = {'name':'Computing', 'label':'Computing Requirements              ', 'fontsize':'36'}
    G.add_node('CSE 2*', label = 'CSE 2', **node_format)
    G.add_node('Eng 10', **node_format)
    G.add_node('ISE 112', **node_format)
    G.add_edge('Eng 10', 'CSE 2*')
    G.add_edge('CSE 2*', 'ISE 112', style = 'invisible', arrowhead = 'none')
    G.create_cluster(['CSE 2*', 'Eng 10', 'ISE 112'], cluster_attrs)
    cluster_attrs = {'name' : 'Tracks', 'label' : 'Choose at Least One',
                     'fontsize' : '36'}    
    G.add_node('ISE 172', **node_format)
    G.add_node('ISE 215/216', **node_format)
    G.create_cluster(['ISE 172', 'ISE 215/216'])
    G.add_node('CSE 17*', label = 'CSE 17', **node_format)
    G.add_edge('CSE 2*', 'CSE 17*')
    G.add_node('Mat 33', **node_format)
    G.add_edge('CSE 17*', 'ISE 172')
    G.add_edge('Mat 33', 'ISE 215/216')
    G.add_node('ISE 305', **node_format)
    cluster_attrs = {'name':'English', 'label':'English Requirements', 'fontsize':'36'}
    G.add_node('Engl 1', **node_format)
    G.add_node('Engl 2', **node_format)
    G.add_edge('Engl 1', 'Engl 2')
    G.create_cluster(['Engl 1', 'Engl 2'], cluster_attrs)
    G.add_node('Math 21', **node_format)
    G.add_node('Physics 11/12', **node_format)
    G.add_edge('Math 21', 'Physics 11/12')
    G.add_node('Math 22', **node_format)
    G.add_edge('Math 21', 'Math 22')
    G.add_node('Physics 21/22', **node_format)
    G.add_edge('Physics 11/12', 'Physics 21/22')
    G.add_node('Math 23', **node_format)
    G.add_edge('Math 23', 'Physics 21/22', style = 'dashed')
    G.add_edge('Math 22', 'Math 23')
    G.add_node('ISE 111', **node_format)
    G.add_edge('Math 22', 'ISE 111')
    G.add_node('Math 205', **node_format)
    G.add_edge('Math 22', 'Math 205')
    G.add_node('ISE 121', **node_format)
    G.add_edge('ISE 111', 'ISE 121')
    cluster_attrs = {'label':'Engineering Electives \n Choose At Least Four', 
                     'name':'Eng', 'fontsize':'36'}
    G.add_node('CSE 2', **node_format)
    G.add_node('Mech 2/3', **node_format)
    G.add_node('ME 104', **node_format)
    G.add_node('ECE 83/81', **node_format)
    G.add_node('CEE 170', **node_format)
    G.add_node('Chem 44', **node_format)
    G.add_node('CSE 17', **node_format)
    G.add_node('Mat 33*', label = 'Mat 33', **node_format)
    G.add_edge('Physics 21/22', 'ECE 83/81', style = 'dashed')
    G.add_edge('CSE 2', 'CSE 17')
    G.create_cluster(['Mech 2/3', 'ME 104', 'ECE 83/81', 'CEE 170', 'Chem 44', 
                      'CSE 17', 'Mat 33*'], cluster_attrs)
    G.add_edge('Math 22', 'Mech 2/3', stlye = 'dashed')
    G.add_edge('Math 23', 'ME 104', style = 'dashed')
    G.add_edge('Physics 11/12', 'ME 104', style = 'dashed')
    G.add_node('ISE 240', **node_format)
    G.add_edge('Math 205', 'ISE 240')
    G.add_node('ISE 230', **node_format)
    G.add_edge('ISE 111', 'ISE 230')
    G.add_node('ISE 131/132', **node_format)
    G.add_edge('ISE 111', 'ISE 131/132', style = 'dashed')
    G.add_node('ISE 224', **node_format)
    G.add_edge('ISE 121', 'ISE 305')
    G.add_node('ISE 226', **node_format)
    G.add_edge('ISE 111', 'ISE 226')
    G.add_node('ISE 251', **node_format)
    G.add_edge('ISE 121', 'ISE 251')
    G.add_edge('ISE 240', 'ISE 251')
    G.add_edge('ISE 230', 'ISE 251')
    cluster_attrs = {'name':'Isolated', 'label':'Other \n Requirements', 'fontsize':'36'}
    G.add_node('Eng 5', **node_format)
    G.add_node('Chem 30', **node_format)
    G.add_node('Eco 1', **node_format)
    G.add_node('Acct 108', **node_format)
    G.add_node('ISE 154', **node_format)
    G.add_edge('ISE 305', 'Eng 5', style = 'invisible', arrowhead = 'none')
    G.add_edge('ME 104', 'Chem 30', style = 'invisible', arrowhead = 'none')
    G.add_edge('ME 104', 'Eco 1', style = 'invisible', arrowhead = 'none')
    G.add_edge('ME 104', 'Acct 108', style = 'invisible', arrowhead = 'none')
    G.add_edge('ME 104', 'ISE 154', style = 'invisible', arrowhead = 'none')
    G.create_cluster(['Eng 5', 'Chem 30', 'Eco 1', 'Acct 108', 'ISE 154'], cluster_attrs)
    cluster_attrs = {'name':'TE', 'label':'Technical Electives \n Chose at Least 4 \n (at Least 2 ISE)', 
                     'fontsize':'36'}
    G.add_node('ISE 339', **node_format)
    G.add_edge('ISE 230', 'ISE 339')
    G.add_node('ISE 316', **node_format)
    G.add_edge('ISE 240', 'ISE 316')
    G.add_node('ISE 347', **node_format)
    G.add_edge('ISE 316', 'ISE 347')
    G.add_node('ISE 275', **node_format)
    G.add_edge('ISE 224', 'ISE 275')
    G.add_node('ISE 372', **node_format)
    G.add_edge('ISE 275', 'ISE 372')
    G.add_node('ISE 358', **node_format)
    G.add_node('ISE 324', **node_format)
    G.add_edge('Math 205', 'ISE 324')
    G.add_node('ISE 332', **node_format)
    G.add_edge('ISE 121', 'ISE 332')
    G.add_node('ISE 362', **node_format)
    G.add_edge('ISE 230', 'ISE 362')
    G.add_edge('ISE 240', 'ISE 362')
    G.add_node('ISE 341', **node_format)
    G.add_edge('ISE 230', 'ISE 341')
    G.add_edge('ISE 224', 'ISE 341')
    G.add_edge('ISE 240', 'ISE 341')
    G.add_node('ISE 356', **node_format)
    G.add_edge('ISE 230', 'ISE 356')
    G.add_edge('ISE 240', 'ISE 356')
    G.add_node('ISE 355', **node_format)
    G.add_edge('ISE 240', 'ISE 355')
    G.add_node('ISE 321', **node_format)
    G.add_node('ISE 345', **node_format)
    G.add_edge('ISE 275', 'ISE 345')
    G.add_node('ISE 382', **node_format)
    G.add_node('ISE 334', **node_format)
    G.add_edge('ISE 240', 'ISE 372')
    G.add_edge('ISE 230', 'ISE 372')
    G.add_node('ISE 319', **node_format)
    G.add_edge('ISE 131/132', 'ISE 319')
    G.add_node('ISE 340', **node_format)
    G.add_edge('ISE 215/216', 'ISE 340')
    G.add_node('ISE 344', **node_format)
    G.add_edge('ISE 215/216', 'ISE 344')
    G.add_node('CSE 2xx', label = 'CSE 2xx \n except \n 241/252', **node_format)
    G.add_node('CSE 3xx', **node_format)
    G.add_node('BIS 3xx', **node_format)
    G.add_node('Math 230', **node_format)
    G.add_node('Math 251', **node_format)
    G.add_edge('ISE 362', 'CSE 2xx', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'CSE 3xx', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'BIS 3xx', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'Math 230', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'Math 251', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'ISE 334', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'ISE 382', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'ISE 321', style = 'invisible', arrowhead = 'none')
    G.add_edge('ISE 362', 'ISE 358', style = 'invisible', arrowhead = 'none')
    cluster = ['ISE 339', 'ISE 316', 'ISE 347', 'ISE 275', 'ISE 358', 'ISE 324', 
               'ISE 332', 'ISE 362', 'ISE 341', 'ISE 356', 'ISE 355', 'ISE 321', 
               'ISE 345', 'ISE 382', 'ISE 334', 'ISE 372', 'ISE 319', 'ISE 340', 
               'ISE 344', 'CSE 2xx', 'Math 251', 'BIS 3xx', 'CSE 3xx', 'Math 230']
    G.create_cluster(cluster, cluster_attrs)

    G.set_display_mode('file')

    G.display(basename = 'ISERequirements', format = 'pdf')
