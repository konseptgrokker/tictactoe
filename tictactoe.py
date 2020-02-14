from collections import namedtuple
from pymonad import *
from functools import reduce
_tempmap = map
map = lambda f, xs: list(_tempmap(f, xs))


### TYPES

# type Player = X | O
X, O = True, False
# type Slot = Maybe Player
Slot = Just
# type Board = [[Slot]]

# type Situation = Welcome | Win | InvalidSlot | Next
# type GameState = (Board, Player, Situation)
GameState = namedtuple("GameState", "board player situation")
# type Model = Game GameState | PlayAgainReprompt | Terminate
Model = namedtuple("Model", "type value")
# type Msg = SlotId Int | PlayAgain (Maybe Bool)
Msg = namedtuple("Msg", "type value")


### MODEL

initialGameState = GameState(
    [[Nothing] * 3 for _ in range(3)], X, "Next")
initialModel = Model("Game", initialGameState)


### HELPERS

def enumIndices(xs):
    return range(len(xs))

def concat(xs):
    return sum(xs, [])

def assignList(i, val, xs):
    assignedFragments = sequence([
        slicer(0,i)(xs),
        Just([val]),
        slicer(i + 1, None)(xs)
    ])
    return assignedFragments.fmap(concat)

def transpose(matrix):
    return map(
        lambda i: map(lambda row: row[i], matrix),
        enumIndices(matrix[0]))

def slicer(start, end):
    def getSlice(xs):
        if end == None or end < len(xs):
            return Just(xs[slice(start, end)])
        else:
            return Nothing
    return getSlice

def getIndex(i, xs):
    if i < len(xs):
        return Just(xs[i])
    else:
        return Nothing

def sequence(xs):
    def consf(start, x):
        return x.fmap(lambda a: lambda b: b + [a]).amap(start)
    return reduce(consf, xs, xs[0].unit([]))

def fromMaybe(f, x, may):
    if may == Nothing:
        return x
    else:
        return f(may.getValue())


### UPDATE

def hasWon(player, board):
    def playerHasAll(line):
        return all(
            map(lambda x: x == Slot(player), line)
        )
    checkRows = lambda board: any(
        map(playerHasAll, board))
    wonCols = checkRows(transpose(board))
    wonRows = checkRows(board)
  
    leftDiag = map(lambda i: board[i][i], enumIndices(board))
    rightDiag = map(lambda i: board[i][2-i], enumIndices(board))
    wonDiags = playerHasAll(leftDiag) or playerHasAll(rightDiag)
    return wonRows or wonCols or wonDiags


def makeMove(slotId, board, player):
    def slotIsValid(slotId, board):
        flatBoard = sum(board, [])
        return flatBoard[slotId - 1] == " "
    y = (slotId-1) // len(board[0])
    x = (slotId-1) % len(board[0])
    newBoardRow = getIndex(y, board).bind(
        lambda row: assignList(x, Slot(player), row))
    return newBoardRow.bind(lambda row: assignList(y, row, board))

def update(msg, model):
    def ifPlayAgainMsg():
        if msg.value.lower() in ["y", "yes"]:
            return initialModel
        elif msg.value.lower() in ["n", "no"]:
            return Model("Terminate", None)
        else:
            return Model("PlayAgainReprompt", None)

    def ifModelGame():
        board, player, state = model.value

        def ifSlotIdMsg():
            def ifValidInput(newBoard):
                return GameState(newBoard, player, "Win") if \
                    hasWon(player, newBoard) else \
                    GameState(newBoard, not player, "Next")
            maybeNewBoard = makeMove(msg.value, board, player)
            return Model(
                "Game",
                fromMaybe(
                    lambda newBoard: ifValidInput(newBoard),
                    GameState(board, player, "InvalidSlot"),
                    maybeNewBoard
                )
            )

        return {
            "SlotId": ifSlotIdMsg,
            "PlayAgain": ifPlayAgainMsg,
        }[msg.type]()
        
        
    def ifModelReprompt():
        return {
            "PlayAgain": ifPlayAgainMsg,
            "SlotId": lambda _: model #impossible state
        }[msg.type]()
    
    return {
        "Game": ifModelGame,
        "PlayAgainReprompt": ifModelReprompt,
    }[model.type]()


### VIEW

def getSymbol(player):
    return "X" if player == X else "O"

def showBoard(board):
    showSlot = lambda slot: f"[{fromMaybe(getSymbol, ' ', slot)}]"
    showRow = lambda row: " ".join(map(showSlot, row))
    return "\n".join(map(showRow, board))

def view(model):
    def ifGame():
        board, player, situation = model.value
        symbol = getSymbol(player)
        print("\nThis is the current board:\n")
        print(showBoard(board))
        def ifWin():
            print(f"Player {symbol} won!")
            return Msg(
                "PlayAgain",
                input("Would you like to play again? (y/n): ")
            )
        def ifInvalidSlot():
            return Msg(
                "SlotId",
                int(input("You must choose a slot between 1-9: "))
            )
        def ifNext():
            return Msg(
                "SlotId",
                int(input(f"\nPlayer {symbol}, choose a slot: "))
            )
        return {
            "Next": ifNext,
            "Win": ifWin,
            "InvalidSlot": ifInvalidSlot
        }[situation]()

    def ifPlayAgainReprompt():
        print("You must answer yes or no.")
        return Msg(
            "PlayAgain",
            input("Would you like to play again? (y/n): ")
        )
    
    def ifTerminate():
        print("Thanks for playing. See you next time!")

    return {
        "Game": ifGame,
        "PlayAgainReprompt": ifPlayAgainReprompt,
        "Terminate": ifTerminate
    }[model.type]()


### GAME

def game(init, update, view):
    model = init
    while True:
        userMsg = view(model)
        if model.type == "Terminate":
            break
        model = update(userMsg, model)


### MAIN

if __name__ == "__main__":
    game(initialModel, update, view)


