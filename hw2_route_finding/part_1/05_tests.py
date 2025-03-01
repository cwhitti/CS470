# from scripts.searcherHelper import *
from classes.Search import Searcher
from classes.SearchNode import SearchNode
from scripts.hSLD import hSLD

seperator = "\n" + "=" * 100
seperator_2 = "\n" + "+" * 50
# Define Searcher, hSLD, SearchNode.
    # Searcher: in Searcher.py
    # hSLD, SearchNode: in searcherHelper.py

# (b) Show your program loading in the 30-node sample file. 
print( seperator )
print("\n(b) Show your program loading in the 30-node sample file. ")
s=Searcher("30node.txt", searchType="DEPTH", verbose=True)

# (c) Show you program setting start node=U and end node=T. 
print( seperator )
print("\n(c) Show you program setting start node=U and end node=T. ")
s.setStartGoal('U','T')

# myViz should be a DRDViz instance -> save map to file on disk.
print( seperator )
print("\n(c.1) save myViz, should be a DRDViz instance -> save map to file on disk.")
s.myViz.save("30node.png")

# (d) Show the one open node.
print( seperator )
print("\n(d) Show the one open node.")
[n.showBasic() for n in s.open]

# (e) Show successors of only open node.
print( seperator )
print("\n(e) Show successors of only open node.")
initial_children = s.successors( s.open.pop(0) )
[n.showBasic() for n in initial_children]

print( seperator )
new_node = initial_children[1]
# new_node = s.findNode( initial_children[1].label )
print(f"\n(e.2) Show successors of other node: {new_node.label}")
new_children = s.successors( new_node )
[n.showBasic() for n in new_children]

quit()

# # (f) Show three inserts: at the front, and the end, and "in order"
print( seperator )
print( "\n (f) Show three inserts: at the front, and the end, and \"in order\" ")
def reset_insert(where):

    print( seperator_2 )
    print(f"Insertion Method: {where}")

    s.verbose = False
    s.reset()
    initial_children = s.successors(s.open.pop(0))
    s.verbose = True
    insert_method = getattr(s, "insert_"+where)
    insert_method(initial_children)

    print("Ordered list:")
    return [n.showBasic() for n in s.open]

reset_insert("front")
reset_insert("end")
reset_insert("ordered")

# # (g) INSERT (K,500), (C,91) and (J,10) and show no duplicates.
print( seperator )
print("\n(g) INSERT (K,500), (C,91) and (J,10) and show no duplicates.")
newdata = (("K",500), ("C",91), ("J",10))
newlist = [SearchNode(label=label, pathcost=pathcost) for label, pathcost in newdata]
ignored = s.insert_ordered(newlist)
[n.showBasic() for n in s.open]



# 3. hSLD heuritic function being called on three nodes.
print( seperator )
print("\n(h) hSLD heuritic function being called on three nodes.")
[hSLD(x, s) for x in ("V", "AC", "J")]
