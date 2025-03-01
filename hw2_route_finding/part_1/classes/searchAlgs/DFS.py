from classes.Frontier import Frontier
'''
DFS Algorithm
'''
class DFS( Frontier ):

    def __init__(self, verbose, nodeGraph) -> None:
        self.open = []
        self.name = "DFS"
        self.verbose = verbose
        self.nodeGraph = nodeGraph

        # initialize helper class
        Frontier.__init__( self, nodeGraph )

    def start( self, start_node, goal_node ):

        # initialize variables
        path = []
        prune_nodes = []

        # add start node to open
        self.open.append( start_node )

        # get path
        path = self._DFS_Helper( start_node, goal_node, path, prune_nodes )

        return self.prune_path( path, prune_nodes)
    
    def _DFS_Helper(self, node, goal_node, path, prune_nodes=[]):
        # Pop from open list
        self.open.pop(self.open.index(node))

        # Check if already visited
        if node in self.visited:
            return None

        # Visit the node
        print("~" * 100)
        print(f"Exploring node: {node.label}")
        path.append(node)
        self.visited.add(node)

        # Check if it's the goal node
        if node.label == goal_node.label:
            print("!!! We found the goal node :D !!!")
            return path  # Return the path to the goal

        # Expand children and add to open list
        successors = self.successors(node)
        self.insert_front(successors)  # Add to the front to prioritize deeper search first

        # check if this is a prune node
        if goal_node.label in [child.label for child in successors]:
            prune_nodes.append( node )

        # Debug: Print open list
        if self.verbose:
            print("Open list:", [child.label for child in self.open])

        # Recursively visit next nodes in the open list
        for child in self.open:
            result = self._DFS_Helper(child, goal_node, path, prune_nodes)
            if result:
                return result  # Goal found
        
        # If no solution is found, backtrack
        path.pop()  # Backtrack by popping the current node
        return None
    
    # def _DFS_Helper(self, node, goal_node, path ):

    #     # Pop from open list
    #     self.open.pop( self.open.index(node) )

    #     # Check if already visited
    #     if node in self.visited:
    #         return None

    #     # Visit the node
    #     print("=" * 100)
    #     print(f"Exploring node: {node.label}")
    #     path.append(node)
    #     self.visited.add(node)

    #     # Check if it's the goal node
    #     if node.label == goal_node.label:
            
    #         path_labels = [ node.label for node in path ]
    #         print(f"Success! Reached goal node {goal_node.label} with path: {path_labels}")
    #         return path  # Return the path to the goal
        
    #     # Expand children and add to open list
    #     successors = self.successors( node )
        
    #     # print(f"Successors: {[child.label for child in successors]}")
    #     self.insert_front( successors )

    #     # Debug: Print open list
    #     if self.verbose:
    #         print("Open list:", [child.label for child in self.open])

    #     # Recursively visit next nodes in the open list
    #     while self.open:
    #         child = self.open[0]  # Peek at the next node to explore
    #         result = self._DFS_Helper(child, goal_node, path )
    #         if result:
    #             return result  # Goal found
        
    #     # If no solution is found, backtrack
    #     path.pop()
    #     return None


       