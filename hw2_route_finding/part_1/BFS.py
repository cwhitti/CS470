from classes.CONSTANTS import BFS_str
from classes.Search import Searcher

x=Searcher("10test.txt", searchType=BFS_str, verbose=False)
x.setStartGoal('h','k')
x.search()