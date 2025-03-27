from classes.CONSTANTS import BestFS_str
from classes.Search import Searcher

x=Searcher("10test.txt", searchType=BestFS_str, verbose=True)
x.setStartGoal('h','k')
x.search()