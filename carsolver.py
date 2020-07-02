# car solver

from copy import copy
from copy import deepcopy

BOARD_WIDTH = 6
BOARD_HEIGHT = 7

EMPTY = "."

class Board:

    def __init__(self):
        self.boardState = [["."] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]
        self.moveList = []
        self.parent = None

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

    def stringify(self):
        return "{}\n{}".format(",".join(self.moveList), self.boardString())

    def boardString(self):
        return "\n".join(["".join(x) for x in self.boardState])

def performMoves(board):
    carsChecked = []
    newBoards = []
    for j in range(BOARD_HEIGHT - 1):
        for i in range(BOARD_WIDTH - 1):
            carName = board.boardState[j][i]
            if carName is not EMPTY and carName not in carsChecked:
                carsChecked += carName
                carRearCoord = (i, j)
                carFrontCoord = None
                backCoord = None
                forwardCoord = None
                forwardMoveName = ""
                backMoveName = ""
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

                if forwardCoord[0] in range(BOARD_WIDTH) and forwardCoord[1] in range(BOARD_HEIGHT) and board.boardState[forwardCoord[1]][forwardCoord[0]] == EMPTY:
                    newBoard = copy(board)
                    newBoard.boardState[forwardCoord[1]][forwardCoord[0]] = carName # move the car into the new cell
                    newBoard.boardState[carRearCoord[1]][carRearCoord[0]] = EMPTY # remove it from it's back cell
                    newBoard.moveList.append("{0} {1}".format(carName, forwardMoveName))
                    newBoard.parent = board
                    newBoards.append(newBoard)

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

def placeCar(board, x, y, carName, length, movesHorizontally):
    if movesHorizontally:
        for dx in range(length):
            board.boardState[y][x+dx] = carName
    else:
        for dy in range(length):
            board.boardState[y+dy][x] = carName

    car_movement[carName] = movesHorizontally
    car_length[carName] = length

car_movement = {}
car_length = {}

board = Board()

goalCar = 'R'
placeCar(board, 1, 2, 'R', 2, True)
placeCar(board, 3, 0, 'A', 3, False)

unprocessedBoards = [board]
visitedBoards = []
solution = None

# perform BFS to explore board states until the solution is found
while len(unprocessedBoards) > 0:
    # pop a task off the queue
    exploreBoard = unprocessedBoards.pop()

    # 
    if exploreBoard.isSolved(goalCar):
        solution = exploreBoard
        break

    if exploreBoard in visitedBoards:
        continue

    visitedBoards.append(exploreBoard)

    adjancentBoards = performMoves(exploreBoard)
    for adjancentBoard in adjancentBoards:
        if (adjancentBoard in visitedBoards) or (adjancentBoard in unprocessedBoards):
            continue
        unprocessedBoards.append(adjancentBoard)


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
    print(board.boardString())
