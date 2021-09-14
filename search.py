# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    myStack = util.Stack()
    myStack.push( (problem.getStartState(), [], []) )

    while not myStack.isEmpty():
        node, actions, visited = myStack.pop()

        if problem.isGoalState(node):
            return path

        for new, action, cost in problem.getSuccessors(node):
            if not new in visited:                
                myStack.push((new, actions + [action] , visited + [node] ))
                path = actions + [action]
                         
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startingNode = problem.getStartState()
    if problem.isGoalState(startingNode):
        return []

    myQueue = util.Queue()
    visitedNodes = []
    # (node,actions)
    myQueue.push((startingNode, []))

    while not myQueue.isEmpty():
        currentNode, actions = myQueue.pop()
        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                newAction = actions + [action]
                myQueue.push((nextNode, newAction))
        
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    myQueue = util.PriorityQueue()
    Nodes = []
    myQueue.push((start, [],0),0)

    while not myQueue.isEmpty():
        current, actions, preCost = myQueue.pop()
        if current not in Nodes:
            Nodes.append(current)

            if problem.isGoalState(current):
                return actions

            for new, action, cost in problem.getSuccessors(current):
                newAction = actions + [action]
                priority=preCost + cost
                myQueue.push((new, newAction,priority),priority)
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    myQueue = util.PriorityQueue()
    Nodes = []
    myQueue.push((start, [],0),0)

    while not myQueue.isEmpty():
        current, actions, preCost = myQueue.pop()
        if current not in Nodes:
            Nodes.append(current)

            if problem.isGoalState(current):
                return actions

            for new, action, cost in problem.getSuccessors(current):
                newAction = actions + [action]
                CosttoNode = preCost + cost
                heuristicCost = CosttoNode + heuristic(new,problem)
                myQueue.push((new, newAction,CosttoNode),heuristicCost)
    util.raiseNotDefined()

#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE ***"
    myStack = util.Stack()
    limit = 1;

    while True: # repeat search with the depth increases until we find the goal
        visitedList = []
        #push the starting point into stack
        myStack.push((problem.getStartState(),[],0))
        #pop out the point
        (state,toDirection,toCost) = myStack.pop()
        #add the point to visited list
        visitedList.append(state)
        while not problem.isGoalState(state): #while we do not find the goal point
            successors = problem.getSuccessors(state) #get the point's succesors
            for son in successors:
                # add the points when it meets 1. not been visited 2. within the depth 
                if (not son[0] in visitedList) and (toCost + son[2] <= limit): 
                    myStack.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                    visitedList.append(son[0]) # add this point to visited list

            if myStack.isEmpty(): # if the no goal is found within the current depth, jump out and increase the depth
                break

            (state,toDirection,toCost) = myStack.pop()

        if problem.isGoalState(state):
            return toDirection

        limit += 1 # increase the depth
    
    while (not found):
        result = depthLimitedSearch(problem,iteration)
        if result != "cut": return result
        iteration+=1
    util.raiseNotDefined()

# Extension Q2e
def enforcedHillClimbing(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
ehc = enforcedHillClimbing
