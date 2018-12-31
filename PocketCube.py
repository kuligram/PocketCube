import time 
from search import PocketCubeProblem, iterativeDeepeningA, MDHeuristic
import os #only to clear screen on start

def enterCubeState():
    colors=['g','r','w','b','o','y']
    state=[]
    
    #clear screen:
    os.system('cls')  # For Windows
    os.system('clear')  # For Linux/OS X

    print("In a 2x2x2 cube, the cubie positions are numbered as follows:")
    print("top layer           bottom layer:")  
    print("     12                  78")
    print("     34                  56")
    print("take the 2x2x2 cube such that the cubie colored white,blue,red is in position #1")
    print("Please enter colors of faces of other cubies as follows:")
    line="'r' for red, 'b' for blue, 'g' for green, 'o' for orange, 'y' for yellow, 'w' for white"
    print(line)
    for i in range(7):
        print("Cubie #",i+2)
        cubie=[]
        color=0
        while color not in colors:
            color=input("the face oriented left or right: ")
        cubie.append(color)
        color=0
        while color not in colors:
            color=input("the face oriented away or towards you: ")
        cubie.append(color)
        color=0
        while color not in colors:
            color=input("the face oriented up or down: ")
        cubie.append(color)
     
        state.append(tuple(cubie))
    return tuple(state)

    
if __name__ == '__main__':
    
    InitialState=enterCubeState() 
    
    print("You have entered the initial state as :")
    print(InitialState)
    print("if solution is not found in a couple of minutes, check for errors in your input, press ctrl+c")

    GoalState=(('g','r','w'),('b','o','w'),('g','o','w'),('b','o','y'),('g','o','y'),('b','r','y'),('g','r','y'))
    print("the goal state is:")
    print(GoalState)
    #1st sample initial state (that I got after futile attempts to solve it by hand):
    #InitialState=(('g','r','w'),('b','o','w'),('g','o','w'),('b','y','r'),('g','o','y'),('o','b','y'),('y','g','r'))
    #other sample initial states:
    #InitialState=(('w','o','g'),('r','y','b'),('g','y','o'),('r','y','g'),('b','y','o'),('w','b','o'),('g','w','r'))
    #InitialState=(('r','y','b'),('w','b','o'),('g','r','y'),('o','y','b'),('g','r','w'),('o','g','w'),('y','o','g'))
    #InitialState=(('b','r','y'),('r','w','g'),('y','g','r'),('w','o','b'),('b','y','o'),('w','o','g'),('o','g','y'))
    #InitialState=(('g','w','o'),('y','o','b'),('w','o','b'),('r','b','y'),('y','r','g'),('w','g','r'),('y','o','g'))
    #InitialState=(('b','o','w'),('o','g','w'),('r','g','w'),('g','y','o'),('g','y','r'),('b','y','o'),('b','y','r'))
    newProblem=PocketCubeProblem(InitialState, GoalState)
    start = time.time()
    #DFS can find longer solutions faster than A* or BFS find optimal (the shortest) solutions
    #A* finds the optimal solution faster than BFS

    #sol=iterativeDeepeningDFS(newProblem, max_depth=15)
    sol=iterativeDeepeningA(newProblem, max_depth=16, heuristic=MDHeuristic)
    #sol=depth_first_graph_search(newProblem, max_depth=10)
    #sol=breadth_first_graph_search(newProblem, max_depth=10)
    #sol=aStarSearchPruning(newProblem, max_depth=10,heuristic=MDHeuristic)
    end = time.time()
    if sol is not None:
        print()
        print("Here is the shortest possible solution: ")
        print(sol.solution())
        print("Here is how to solve the cube.")
        print("Rotation here is like you close a cap on a bottle with your right hand.")
        print("For each 'X' rotate the right half of the cube (cubies 2,4,6,8) by a quarter turn")
        print("For each 'Y' rotate the front half of the cube (cubies 3,4,5,6) by a quarter turn")
        print("For each 'Z' rotate the bottom half of the cube (cubies 5,6,7,8) by a quarter turn")
        print("top layer           bottom layer:")  
        print("     12                  78")
        print("     34                  56")
        
        
        #print(" solution depth: ", sol.depth)
        #print("Nodes expanded: ",newProblem.nodes_expanded," states explored: ",newProblem.states_explored, " in ", end-start, " seconds")
    else: 
        print("No solution found. Nodes expanded: ",newProblem.nodes_expanded," states explored: ",newProblem.states_explored, " in ", end-start, " seconds")

    
   