from bbvisual import BBVisual
import gtk
import pdb
import sys
sys.path.append('../GrUMPy/trunk')
sys.path.append('../xdot')

from baktree import parse_options

if __name__ == '__main__':
    inputFile, options = parse_options()
    bt = BBVisual(inputFile, options)
    #bt.process_file()
    bt.set_layout('fdp')
    bt.add_root('0', status = 'branched', pos = '"2,0"')
    bt.add_left_child('1','0', status = 'branched', pos = '"1,0"')
    bt.add_right_child('2','0', status = 'branched', pos = '"0,0"')
    bt.add_left_child('3','1', status = 'candidate', pos = '"3,0"')
    bt.add_right_child('4','1', status = 'candidate', pos = '"4,0"')
    bt.add_left_child('5','2', status = 'fathomed', pos = '"5,0"')
    print bt.to_string()
    gtk.main()
