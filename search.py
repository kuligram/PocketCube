from utils import PriorityQueue, is_in
from collections import deque
import time
import config
import pickle

class Problem(object):

    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions.
    https://github.com/aimacode/aima-python"""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

class Node:

    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class.
    https://github.com/aimacode/aima-python"""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        problem.nodes_expanded+=1
        return [self.child_node(problem, action)
                for action in problem.actions(self)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))
        return next_node
    
    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

# ______________________________________________________________________________



class PocketCubeProblem(Problem):
    """The cubelets in the 2x2x2 are numbered as follows if you look from above:
    top layer           bottom layer:  
    12                  78
    34                  56
    Axis X is along the "1-2" direction(to the right), Axis Y is along 4-2(away from you), axis Z is along 5-3 (up)
    
    Cubelet #1: 
    blue colored face is on the left, orthogonal to X axis, 
    red colored face is is orhogonal to Y axis.
    white colored face is looking up, orthogonal to Z axis.
    Thus, cubelet #1 is specified in the state as  ('b','r','w')
    
    2x2x2 cube is represented as a tuple of 7 such cubelet tuples (cubelet #1 is fixed in space)
    
    Action is a right hand rotation (as if closing a lid on a bottle with your right hand)
    Action 'R' rotates cubelets 2,4,6,8(right 4 cubelets) around the (negative)X direcion by quarter turn,
    Action 'F' rotates cubelets 3,4,5,6(front 4 cubelets) around the Y direcion by quarter turn,
    Action 'B' rotates cubelets 5,6,7,8(bottom 4 cubelets) around the Z direcion by quarter turn,
    Action R2 is a half turn rotation, action R\' is a counter-clockwise quarter turn etc.
    """
    
    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)
        #counting nodes expanded - add one each time the node is expanded
        self.nodes_expanded = 0
        self.states_explored=0

    def actions(self, node):
        #the largerst branching ratio but easier branch pruning via the set of explored states and depth checks
        return ['R','R2','R\'','F','F2','F\'','B','B2','B\'']
        
    def result(self, s, action):
        if action=='R\'':
            return (
                (s[6][0],s[6][2],s[6][1]),
                s[1],
                (s[0][0],s[0][2],s[0][1]),
                s[3],
                (s[2][0],s[2][2],s[2][1]),
                s[5],
                (s[4][0],s[4][2],s[4][1]))
        if action=='R2':
            return (s[4],s[1],s[6],s[3],s[0],s[5],s[2])
        if action=='R':
            return (
                (s[2][0],s[2][2],s[2][1]),
                s[1],
                (s[4][0],s[4][2],s[4][1]),
                s[3],
                (s[6][0],s[6][2],s[6][1]),
                s[5],
                (s[0][0],s[0][2],s[0][1]))
        if action=='F':
            return (
                s[0],
                (s[3][2],s[3][1],s[3][0]),
                (s[1][2],s[1][1],s[1][0]),
                (s[4][2],s[4][1],s[4][0]),
                (s[2][2],s[2][1],s[2][0]),
                s[5],s[6])
        if action=='F2':
            return (s[0],s[4],s[3],s[2],s[1],s[5],s[6])
        if action=='F\'':
            return (
                s[0],
                (s[2][2],s[2][1],s[2][0]),
                (s[4][2],s[4][1],s[4][0]),
                (s[1][2],s[1][1],s[1][0]),
                (s[3][2],s[3][1],s[3][0]),
                s[5],s[6])
        if action=='B':
            return (
                s[0],
                s[1],
                s[2],
                (s[5][1],s[5][0],s[5][2]),
                (s[3][1],s[3][0],s[3][2]),
                (s[6][1],s[6][0],s[6][2]),
                (s[4][1],s[4][0],s[4][2]))
        if action=='B2':
            return (s[0],s[1],s[2],s[6],s[5],s[4],s[3])
        if action=='B\'':
            return (
                s[0],
                s[1],
                s[2],
                (s[4][1],s[4][0],s[4][2]),
                (s[6][1],s[6][0],s[6][2]),
                (s[3][1],s[3][0],s[3][2]),
                (s[5][1],s[5][0],s[5][2]))

    def goal_test(self, state):
        return state == self.goal
    
      
def depth_first_graph_search(problem, max_depth=10):
    """Search the deepest nodes in the search tree first, limited by max_depth.
        Search through the successors of a problem to find a goal.
        Does not get trapped by loops.
        If two paths reach a state, only use the first one. [Figure 3.7] of AIMA book"""
    
    node=Node(problem.initial)
    frontier = [(node)]  # Stack
    explored = {}
    explored[node.state]=node.depth
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            problem.states_explored=len(explored)
            return node
        #max_depth of the node to which we expand. Expanding means generating the successor nodes
        if node.depth<max_depth:
            for child in node.expand(problem):
                #DFS should expand the currently considered node (child) if 
                # 1) it's not in explored dict
                # 3) it's in explored but depth is smaller than previous node
                if child.state not in explored or child.depth<explored[child.state]:
                    frontier.append(child)
                    explored[child.state]=child.depth
                
    problem.states_explored=len(explored)
    return None


def breadth_first_graph_search(problem, max_depth=10):
    """[Figure 3.11] of AIMA book  """
    current_depth=0
    explored = set()
    node = Node(problem.initial)
    frontier = deque([node])
    explored.add(node.state)
    
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            problem.states_explored=len(explored)
            return node
        if node.depth>current_depth:
            current_depth=node.depth
            print("BFS is working through solutions of length= ", current_depth)
        if node.depth<max_depth:
            for child in node.expand(problem):
                if child.state not in explored:
                    frontier.append(child)
                    explored.add(child.state)
                    
    problem.states_explored=len(explored)
    return None


def HprecomputeBFS(problem, max_depth=10):
    """Precomputes the number of moves needed to solve every state reachable from the goal 
    to depth max_depth by BFS and returns the dictionary of all those states  """
    current_depth=0
    statesAtDepth=1
    explored = {}
    node = Node(problem.initial)
    frontier = deque([node])
    explored[node.state]=node.depth
    
    while frontier:
        node = frontier.popleft()
        
        if node.depth<max_depth:
            for child in node.expand(problem):
                if child.depth>current_depth:
                        print("States explored at depth ",current_depth, " : ",statesAtDepth)
                        statesAtDepth=0
                        current_depth+=1
                        print("BFS is enumerating states at depth= ", current_depth)

                if child.state not in explored:
                    frontier.append(child)
                    explored[child.state]=child.depth
                    statesAtDepth+=1
                    
        
    print("States explored at depth ",current_depth, " : ",statesAtDepth)
    problem.states_explored=len(explored)
    return explored

def computePatternDB():
    print("generating the pattern database heuristic")
    GoalState=(('g','r','w'),('b','o','w'),('g','o','w'),('b','o','y'),('g','o','y'),('b','r','y'),('g','r','y'))
    newProblem=PocketCubeProblem(GoalState, GoalState)
    start = time.time()

    config.table=HprecomputeBFS(newProblem, max_depth=9)
    config.tableLoaded=1
    end = time.time()
    print("Total states enumerated: ", newProblem.states_explored, " in ", end-start, " s")
    with open('states9.pickle', 'wb') as f:
       # Pickle the 'data' dictionary using the highest protocol available.
        print("saving the precomputed heuristic to file 'states9.pickle")
        pickle.dump(config.table, f, pickle.HIGHEST_PROTOCOL)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def simpleHeuristic(node, problem):
    """number of misplaced cubelets heuristic"""
    value=0
    for index, cubelet in enumerate(problem.goal):
        if not all(color in node.state[index] for color in cubelet):
            value+=1
    return value/4

def MDHeuristic(node, problem):
    """manhattan distance heuristic - the number of translations and rotations needed for each cubelet
     summed over all cubelets    http://www.aaai.org/Papers/AAAI/1997/AAAI97-109.pdf"""
    def getNumber(cubie):
        if 'b' in cubie:
            if 'o' in cubie:
                if 'w' in cubie:
                    return 3
                else:
                    return 5
            else:
                return 7
        elif 'w' in cubie:
            if 'r' in cubie:
                return 2
            else:
                return 4
        elif 'r' in cubie:
            return 8
        else:
            return 6
        return None
    
    def getTranslationMD(cubeletNumber, position):
        table=[[0,2,1,3,2,2,1],[2,0,1,1,2,2,3],[1,1,0,2,1,3,2],[3,1,2,0,1,1,2],[2,2,1,1,0,2,1],[2,2,3,1,2,0,1],[1,3,2,2,1,1,0]]   
        return table[cubeletNumber-2][position-2]         
    
    def getRotationMD(cubie, goalCubie):
        value=0
        for i in range(3):
            if cubie[i]!=goalCubie[i]:
                value+=1
        if value==0:
            return value
        else:
            return value-1
        return None

    #for each cubie in node.state find its number, 
    # from number an its index in node.state find translations MD
    # from cubies colors find rotation MD
    #Since our step cost is 1, heuristic change on each action must be smaller than 1 for consistency
    value=0
    for index, cubelet in enumerate(node.state):
        cubeletNumber=getNumber(cubelet)
        translationMD=getTranslationMD(cubeletNumber,index+2)
        rotationMD=getRotationMD(cubelet,problem.goal[cubeletNumber-2])
        #the next line is to help understand how this heuristic computes:
        #print("cubie: ", cubelet, ' cubelet number: ', cubeletNumber, ' translation MD: ', translationMD, ' rotationMD: ', rotationMD)
        value+=translationMD+rotationMD
    return int(value/ 8)+(value % 8 > 0) #rounding up and dividing by 8 to make it consistent

def PatterndDBHeuristic(node, problem):
    if config.tableLoaded==1:
        if node.state in config.table:
            return config.table[node.state]
        else:
            return MDHeuristic(node, problem)
    else:
        return MDHeuristic(node, problem)

def aStarSearch(problem, max_depth=10, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #initialize search tree:
    node = Node(problem.initial)
    frontier=PriorityQueue()
    frontier.push(node,0+heuristic(node, problem))
    explored={}
    explored[node.state]=node.depth

    if problem.goal_test(node.state):
        return node
    
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.goal_test(node.state):
            problem.states_explored=len(explored)
            return node
        #max_depth of the node to which we expand. Expanding means generating the successors
        if node.depth<max_depth:
        #expanding the current node
            for child in node.expand(problem):
                #DF-like search should expand the currently considered node (child) if 
                # 1) it's not in explored dict
                # 2) it's in explored but depth is smaller than previous node - for rubik's cube type of problem
                if child.state not in explored or child.depth<explored[child.state]:
                        path_f=child.path_cost+heuristic(child, problem)
                        #for heuristic to be consistent, f(child.state )>=f(child.parent.state):
                        #MDheuristic is consistent if it's divided by 8 (see def).
                        #optional consistency check, next 3 lines

                        #ancestor_f=node.path_cost+heuristic(node, problem)
                        #if ancestor_f>path_f: 
                        #    print("must be f(state)<=f(next expanded state). f(state) and f(next) are ", ancestor_f, path_f)
                        
                        frontier.push(child,path_f)
                        explored[child.state]=child.depth
    
    problem.states_explored=len(explored)
    return  None

def aStarSearchPruning(problem, max_depth=10, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    Prune the branch if its herustic cost is larger than search depth limit"""
    node = Node(problem.initial)
    frontier=PriorityQueue()
    frontier.push(node,0+heuristic(node, problem))
    explored={}
    explored[node.state]=node.depth

    if problem.goal_test(node.state):
        return node
    
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.goal_test(node.state):
            problem.states_explored=len(explored)
            return node
        if node.depth<max_depth:
            for child in node.expand(problem):                
                if child.state not in explored or child.depth<explored[child.state]:
                    h=heuristic(child, problem)
                    if (child.depth+h)<=max_depth:
                        path_f=child.path_cost+h
                        frontier.push(child,path_f)
                    explored[child.state]=child.depth
                    
    problem.states_explored=len(explored)
    return  None

def iterativeDeepeningDFS(problem, max_depth):
    for d in range(max_depth+1):
        print("DFS is working through solutions of up to ", d, " steps long")
        sol=depth_first_graph_search(problem, max_depth=d)
        if sol is not None:
            return sol
    return None

def iterativeDeepeningA(problem, max_depth, heuristic):
    for d in range(max_depth+1):
        print("A* is working through solutions of up to ", d, " steps long")
        sol=aStarSearchPruning(problem, max_depth=d,heuristic=heuristic)
        if sol is not None:
            return sol
    return None
