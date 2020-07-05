# car solver

from copy import copy
from copy import deepcopy
from queue import PriorityQueue

BOARD_WIDTH = 6
BOARD_HEIGHT = 7

EMPTY = "."

"""
Represents a unique board state
Overloads certain python operators for this object to work within common python colletions
"""
class Board:

    def __init__(self):
        self.boardState = [["."] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]
        self.moveList = []
        self.parent = None

    def priorityWeight(self):
        return len(self.moveList)

    def __copy__(self):
        newBoard = Board()
        newBoard.boardState = deepcopy(self.boardState)
        newBoard.moveList = copy(self.moveList)
        return newBoard

    def isSolved(self, carName):
        return self.boardState[2][BOARD_WIDTH-1] is carName

    def moveCount(self):
        return len(self.moveList)

    def __eq__(self, other):
        return self.boardState == other.boardState

    def __lt__(self, other):
        return self.priorityWeight() < other.priorityWeight()

    def stringify(self):
        return "{}\n{}".format(",".join(self.moveList), self.boardString())

    def boardString(self):
        return "\n".join(["".join(x) for x in self.boardState])

"""
Accepts a board state and attempts to find all possible boards that can be transitioned to.
Currently, this only checks one cell moves.
"""
def performMoves(board):
    carsChecked = []
    newBoards = []
    for j in range(BOARD_HEIGHT - 1):
        for i in range(BOARD_WIDTH - 1):
            carName = board.boardState[j][i]
            if carName is not EMPTY and carName not in carsChecked:
                carsChecked += carName
                carRearCoord = (i, j) # the back coordinate of the car
                carFrontCoord = None # the front coordinate of the car
                backCoord = None # the immediate coordinate behind the car
                forwardCoord = None # the immediate coordinate in front the car
                forwardMoveName = ""
                backMoveName = ""

                # if the car is defined to move horizontally
                if carMovesHorizontally(carName):
                    forwardCoord = (i + carLength(carName), j)
                    carFrontCoord = (i + carLength(carName) - 1, j)
                    backCoord = (i - 1, j)
                    forwardMoveName = "Right"
                    backMoveName = "Left"
                else:
                    forwardCoord = (i, j + carLength(carName))
                    carFrontCoord = (i, j + carLength(carName) - 1)
                    backCoord = (i, j - 1)
                    forwardMoveName = "Down"
                    backMoveName = "Up"

                # if there is space in front of the car that is not occupied nor off the board
                if forwardCoord[0] in range(BOARD_WIDTH) and forwardCoord[1] in range(BOARD_HEIGHT) and board.boardState[forwardCoord[1]][forwardCoord[0]] == EMPTY:
                    newBoard = copy(board)
                    newBoard.boardState[forwardCoord[1]][forwardCoord[0]] = carName # move the car into the new cell
                    newBoard.boardState[carRearCoord[1]][carRearCoord[0]] = EMPTY # remove it from it's back cell
                    newBoard.moveList.append("{0} {1}".format(carName, forwardMoveName))
                    newBoard.parent = board
                    newBoards.append(newBoard)

                # if there is space in behind of the car that is not occupied nor off the board
                if backCoord[0] in range(BOARD_WIDTH) and backCoord[1] in range(BOARD_HEIGHT) and board.boardState[backCoord[1]][backCoord[0]] == EMPTY:
                    newBoard = copy(board)
                    newBoard.boardState[backCoord[1]][backCoord[0]] = carName # move the car into the new cell
                    newBoard.boardState[carFrontCoord[1]][carFrontCoord[0]] = EMPTY # remove it from it's back cell
                    newBoard.moveList.append("{0} {1}".format(carName, backMoveName))
                    newBoard.parent = board
                    newBoards.append(newBoard)

    return newBoards

def carMovesHorizontally(carName):
    return car_movement[carName]

def carLength(carName):
    return car_length[carName]

"""
A helper method that ensures all needed data is placed in the correct data structures for future reference
"""
def placeCar(board, x, y, carName, length, movesHorizontally):
    if movesHorizontally:
        for dx in range(length):
            board.boardState[y][x+dx] = carName
    else:
        for dy in range(length):
            board.boardState[y+dy][x] = carName

    car_movement[carName] = movesHorizontally
    car_length[carName] = length

def solve(initialBoard):

    measurements = {
        "processed": 0,
        "seen": 1 # starts at one since there is the initial board
    }

    # create a priority queue
    unprocessedBoards = PriorityQueue()
    # add the initial state
    unprocessedBoards.put((initialBoard.priorityWeight(), initialBoard))

    # create a list for storing the visited boards
    visitedBoards = []

    # perform BFS to explore board states until the solution is found
    while not unprocessedBoards.empty():
        # pop a task off the queue
        exploreBoard = unprocessedBoards.get()[1]
        measurements["processed"] += 1

        # if the board demonstrates a solved position
        if exploreBoard.isSolved(goalCar):
            return (exploreBoard, measurements) # return it immedaitely. we have found a solution

        # if the board has already been processed then move onto the next board state in the queue
        if exploreBoard in visitedBoards:
            continue
        
        # mark the board as visited
        visitedBoards.append(exploreBoard)

        # calculate all boards that can be reached from the current board
        adjancentBoards = performMoves(exploreBoard)
        for adjancentBoard in adjancentBoards:
            # if we have already visited and processed a board then we do not need to add it again
            if (adjancentBoard in visitedBoards): # or (adjancentBoard in unprocessedBoards):
                continue

            # otherwise, we need to process this adjacent state. add it to the queue
            unprocessedBoards.put((adjancentBoard.priorityWeight(), adjancentBoard))
            measurements["seen"] += 1

    return (None, measurements) 

def printSolution(initialBoard, solution):
    if solution is not None:

        final_solution = []
        while solution is not None:
            final_solution.append(solution)
            solution = solution.parent

        final_solution.reverse()
        print("=== Start ")
        print(final_solution[0].boardString())

        for step in final_solution:
            if len(step.moveList) > 0:
                print(">>> Move {}".format(step.moveList[-1]))
                print()
            if step.isSolved(goalCar):
                print("=== Solved !!!")
                print(step.boardString())
            else:
                print("=== Current board")
                print(step.boardString())

        print("=== All Moves ===")
        for move in final_solution[-1].moveList:
            print(move)

    else:
        print("There is no solution for the board")
        print(initialBoard.boardString())


car_movement = {}  # mapping of car names to whether they move horizontally or not
car_length = {}  # mapping of car names to the size of the car

"""
...A..
...A..
.RRA..
...BBB
......
......
......
"""
# initialBoard = Board()
# goalCar = 'R'
# placeCar(initialBoard, 1, 2, 'R', 2, True)
# placeCar(initialBoard, 3, 0, 'A', 3, False)
# placeCar(initialBoard, 3, 3, 'B', 3, True)


"""
...A..
...A.D
.RRA.D
..EBBB
..E..C
.FF..C
.....C
"""
initialBoard = Board()
goalCar = 'R'
placeCar(initialBoard, 1, 2, 'R', 2, True)
placeCar(initialBoard, 3, 0, 'A', 3, False)
placeCar(initialBoard, 3, 3, 'B', 3, True)
placeCar(initialBoard, 5, 4, 'C', 3, False)
placeCar(initialBoard, 5, 1, 'D', 2, False)
placeCar(initialBoard, 2, 3, 'E', 2, False)
placeCar(initialBoard, 1, 5, 'F', 2, True)

(solution, measurements) = solve(initialBoard)
printSolution(initialBoard, solution)

print(measurements)
