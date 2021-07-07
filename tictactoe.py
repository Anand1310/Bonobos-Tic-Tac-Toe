import math
import random
from typing import no_type_check

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = o = 0
    for i in board:
        for q in i:
            if q == X:
                x += 1
            elif q == O:
                o += 1
    
    if x > o:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty = []
    for i in range(3): # y-axis
        for j in range(3): #x-axis
            if board[i][j] == None:
                empty.append((i, j))
                
    return empty

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    from copy import deepcopy
    (i, j) = action
    if i > 2 or j > 2 or i < 0 or j < 0:
        raise IndexError
    p = player(board)
    newboard = deepcopy(board)
    newboard[i][j] = p
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3): # check horizontal
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board [1][1] == board[2][0]:
        return board[1][1]
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or actions(board) == []:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win != None:
        if win == X:
            return 1
        else:
            return -1
    return 0

board = initial_state()
def move(action):
    global board
    board = result(board, action)
    return board

def random_action(board):
    while True:
        move = (random.randrange(0, 2), random.randrange(0, 2))
        if move not in actions(board):
            return move
    
def minimax(board):
    """
    Returns the optimal action for the 'current' player on the board.
    """
    if terminal(board):
        return None
    move = 1
    if player(board) == X:
        """
        X win = 1 so X need to max the score
        """
        v = -math.inf
        for action in actions(board):
            f = Min_Value(result(board, action))
            if v < f:
                v = f
                move = action
    else: 
        """
        Need different because O is -1, so O need to minize the score to win
        """
        v = math.inf
        for action in actions(board):
            f = Max_Value(result(board, action))
            if v > f:
                v = f
                move = action
    return move

def Max_Value(state):
    if terminal(state):
      return utility(state)

    v = -math.inf    

    for action in actions(state):
        v = max(v, Min_Value(result(state, action)))
        if v == 1:
            break
    return v

def Min_Value(state):
    if terminal(state):
        return utility(state)

    v = math.inf

    for action in actions(state):
        v = min(v, Max_Value(result(state, action)))
        if v == -1:
            break
    return v

def cheat_move(board):
    # TODO https://github.com/Anand1310/Bonobos-Tic-Tac-Toe/projects/1#card-64544661
    pass