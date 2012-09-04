import sys
sys.path.append('../../xdot')
sys.path.append('../../GrUMPy/trunk')
print sys.path
from xdot import DotWidget


#from graph_solution import BinaryTree
from baktree import BAKTree, parse_options

import gtk
#class BBVisual(BinaryTree, gtk.Window):
class BBVisual(BAKTree, gtk.Window):
    def __init__(self, filename = None, options = None, **attrs):
#        BinaryTree.__init__(self, **attrs)
        BAKTree.__init__(self, filename, options, **attrs)
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        # create vertical box, will keep drawing area
        vbox1 = gtk.VBox(False, 0)
        self.add(vbox1)

        # create horizontal box, will keep buttons
        hbox1 = gtk.HBox()
        # pack horizontal box to the top of vertical box
        vbox1.pack_start(hbox1, False, False, 0)
 
        # create and add show tree button
        show_tree_button = gtk.Button("show tree")
        hbox1.pack_start(show_tree_button, False, False, 0)
        # connect show tree button to its method
        show_tree_button.connect("clicked", self.set_dotcode, None)

        # create and add mark candidates button
        mark_candidates_button = gtk.Button("mark candidate nodes")
        hbox1.pack_start(mark_candidates_button, False, False, 0)
        # connect mark candidates button to its method
        mark_candidates_button.connect("clicked", self.mark_candidates, None)
 
        # create and add mark branched button
        mark_branched_button = gtk.Button("mark branched nodes")
        hbox1.pack_start(mark_branched_button, False, False, 0)
        # connect mark branched button to its method
        mark_branched_button.connect("clicked", self.mark_branched, None)

        # create and add mark pregnant button
        mark_pregnant_button = gtk.Button("mark pregnant nodes")
        hbox1.pack_start(mark_pregnant_button, False, False, 0)
        # connect mark pregnant button to its method
        mark_pregnant_button.connect("clicked", self.mark_pregnant, None)

        # create and add mark infeasible button
        mark_infeasible_button = gtk.Button("mark infeasible nodes")
        hbox1.pack_start(mark_infeasible_button, False, False, 0)
        # connect mark infeasible button to its method
        mark_infeasible_button.connect("clicked", self.mark_infeasible, None)

        # create and add mark fathomed button
        mark_fathomed_button = gtk.Button("mark fathomed nodes")
        hbox1.pack_start(mark_fathomed_button, False, False, 0)
        # connect mark fathomed button to its method
        mark_fathomed_button.connect("clicked", self.mark_fathomed, None)

        # create and add mark integer button
        mark_integer_button = gtk.Button("mark integer nodes")
        hbox1.pack_start(mark_integer_button, False, False, 0)
        # connect mark integer button to its method
        mark_integer_button.connect("clicked", self.mark_integer, None)

        # create and add mark all button
        mark_all_button = gtk.Button("mark all")
        hbox1.pack_start(mark_all_button, False, False, 0)
        # connect mark all button to its method
        mark_all_button.connect("clicked", self.mark_all, None)

        # create and add reset button
        reset_button = gtk.Button("reset")
        hbox1.pack_start(reset_button, False, False, 0)
        # connect reset button to its method
        reset_button.connect("clicked", self.reset, None)

        # create draw area widget
        self.draw_area_widget = DotWidget()
        # add draw area widget to vertical box
        vbox1.pack_start(self.draw_area_widget)

        self.set_focus(self.draw_area_widget)
        self.show_all()
        self.connect('destroy', gtk.main_quit)

    def set_dotcode(self, widget, data=None):
        self.draw_area_widget.set_dotcode(self.to_string())
        self.draw_area_widget.zoom_to_fit()

    def mark_candidates(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'candidate':
                self.set_node_attr(n, 'color', 'green')
        self.set_dotcode(None, None)

    def mark_branched(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'branched':
                self.set_node_attr(n, 'color', 'blue')
        self.set_dotcode(None, None)

    def mark_pregnant(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'pregnant':
                self.set_node_attr(n, 'color', 'yellow')
        self.set_dotcode(None, None)

    def mark_infeasible(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'infeasible':
                self.set_node_attr(n, 'color', 'pink')
        self.set_dotcode(None, None)

    def mark_fathomed(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'fathomed':
                self.set_node_attr(n, 'color', 'red')
        self.set_dotcode(None, None)

    def mark_integer(self, widget, data=None):
        for n in self.get_node_list():
            if self.get_node_attr(n, 'status') == 'integer':
                self.set_node_attr(n, 'color', 'yellowgreen')
        self.set_dotcode(None, None)

    def mark_all(self, widget, data=None):
        self.mark_candidates(None, None)
        self.mark_branched(None, None)
        self.mark_pregnant(None, None)
        self.mark_infeasible(None, None)
        self.mark_fathomed(None, None)
        self.mark_integer(None, None)


    def reset(self, widget, data=None):
        for n in self.get_node_list():
            self.set_node_attr(n, 'color', 'black')
        self.set_dotcode(None, None)
        
