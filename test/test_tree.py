from gimpy import BinaryTree

if __name__=='__main__':
    t = BinaryTree()
    t.add_root(0)
    t.add_left_child(1,0)
    t.add_left_child(2,1)
    t.add_left_child(3,2)
    t.add_right_child(4,2)
    t.add_right_child(6,1)
    t.add_right_child(5,0)
    t.add_right_child(8,5)
    # test print_nodes()
    t.print_nodes()
    # test dfs
    t.dfs()
    # test bfs
    t.bfs()
    print 'off display done'
    # test print_nodes(display='pygame')
    t.print_nodes(display='pygame')
    # test dfs(display='pygame')
    t.dfs(display='pygame')
    # test bfs(display='pygame')
    t.bfs(display='pygame')



