from classes.CONSTANTS import DFS_str
from classes.Search import Searcher

# x=Searcher("10test.txt", searchType=DFS_str, verbose=True)
# x.setStartGoal('h','k')
# x.search()

x=Searcher("50test.txt", searchType="DEPTH", verbose=False)
x.setStartGoal('s','c')
x.search()