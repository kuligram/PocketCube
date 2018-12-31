import pickle
#from search import HprecomputeBFS, PocketCubeProblem
import os #only to clear screen on start

table={}
tableLoaded=0

def loadPatternDB():
    global table
    global tableLoaded
    print("Loading the pattern database heuristic")
    try:
        with open('states9.pickle', 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            table = pickle.load(f)
            tableLoaded=1
    except:
        print("states9.pickle file with the precomputed heuristic not found.")
        tableLoaded=0
        return 1
    return 0

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
            color=input("the face oriented front or back: ")
        cubie.append(color)
        color=0
        while color not in colors:
            color=input("the face oriented up or down: ")
        cubie.append(color)
     
        state.append(tuple(cubie))
    return tuple(state)
