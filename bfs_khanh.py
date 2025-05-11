import copy
import itertools


def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j
            
def is_solved(board, goal):
    for i in range(4):
        for j in range(4):
            if board[i][j] != goal[i][j]:
                return False
    return True

def is_solved_top_row(board, goal):
    for i in range(4):
        if board[0][i] != goal[0][i]:
            return False
    return True

def is_solved_left_col(board, goal):
    for i in range(4):
        if board[i][0] != goal[i][0]:
            return False
    return True

def is_solved_2_top_row(board, goal):
    for i in range(4):
        if board[1][i] != goal[1][i]:
            return False
    return True

def add_move(board, solution, move): # R = 0 to right, L = 0 to left, U = 0 to up, D = 0 to down
    dy, dx = 0, 0
    if move == "R":
        dx = 1
        dy = 0
    elif move == "L":
        dx = -1
        dy = 0
    elif move == "U":
        dx = 0
        dy = -1
    elif move == "D":
        dx = 0
        dy = 1

    solution.append(move)
    zero_y, zero_x = find_pos(board, 0)
    temp = board[zero_y][zero_x]
    board[zero_y][zero_x] = board[zero_y + dy][zero_x + dx]
    board[zero_y + dy][zero_x + dx] = temp


def get_next_states(curr_state, boundary_x, boundary_y):
    board, moves = curr_state

    next_states = []

    if len(moves) == 0:
        zero_y, zero_x = find_pos(board, 0)
        for move in ["R", "L", "U", "D"]:
            if (move == "R" and zero_x < 3) \
                or (move == "L" and zero_x > boundary_x) \
                or (move == "U" and zero_y > boundary_y) \
                or (move == "D" and zero_y < 3):
                next_board = copy.deepcopy(board)
                new_steps = copy.deepcopy(moves)
                add_move(next_board, new_steps, move)
                next_states.append((next_board, new_steps))

    else:
        last_move = moves[-1]
        if last_move == "R":
            next_moves = ["R", "U", "D"]
        elif last_move == "L":
            next_moves = ["L", "U", "D"]
        elif last_move == "U":
            next_moves = ["R", "L", "U"]
        elif last_move == "D":
            next_moves = ["R", "L", "D"]

        zero_y, zero_x = find_pos(board, 0)
        for move in next_moves:
            if (move == "R" and zero_x < 3) \
                or (move == "L" and zero_x > boundary_x) \
                or (move == "U" and zero_y > boundary_y) \
                or (move == "D" and zero_y < 3):
                next_board = copy.deepcopy(board)
                new_steps = copy.deepcopy(moves)
                add_move(next_board, new_steps, move)
                next_states.append((next_board, new_steps))

    return next_states

def compress_board(board):
    output = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            output.append(str(board[i][j]))

    return " ".join(output)


def bfs_khanh(board, GOAL_STATE):
    '''A state consists of the current board and set of moves to get to that board'''


    ### SOLVE TOP ROW ###
    fringe = [(copy.deepcopy(board), [])]
    visited = set()

    while len(fringe) > 0:
        curr_state = fringe.pop(0)
        board, _ = curr_state
        visited.add(compress_board(board))

        if is_solved_top_row(board, GOAL_STATE):
            solved_top_row_board, solve_top_row_steps = curr_state
            # return solution_steps
            break
        
        next_states = get_next_states(curr_state, 0, 0)
        if len(next_states) > 0:
            fringe.extend(next_states)

    ### SOLVE LEFT COLUMN ###
    fringe = [(copy.deepcopy(solved_top_row_board), [])]
    visited = set()

    while len(fringe) > 0:
        curr_state = fringe.pop(0)
        board, _ = curr_state
        visited.add(compress_board(board))

        if is_solved_left_col(board, GOAL_STATE):
            solved_left_col_board, solve_left_col_steps = curr_state
            # return list(itertools.chain(solve_top_row_steps, solve_left_col_steps))
            break
        
        next_states = get_next_states(curr_state, 0, 1)
        if len(next_states) > 0:
            fringe.extend(next_states)

    ### SOLVE SECOND TOP ROW ###
    fringe = [(copy.deepcopy(solved_left_col_board), [])]
    visited = set()

    while len(fringe) > 0:
        curr_state = fringe.pop(0)
        board, _ = curr_state
        visited.add(compress_board(board))

        if is_solved_2_top_row(board, GOAL_STATE):
            solved_2_top_row_board, solve_2_top_row_steps = curr_state
            # return list(itertools.chain(solve_top_row_steps, solve_left_col_steps, solve_2_top_row_steps))
            break
        
        next_states = get_next_states(curr_state, 1, 1)
        if len(next_states) > 0:
            fringe.extend(next_states)

    ### SOLVE LAST 6 PIECE ###
    fringe = [(copy.deepcopy(solved_2_top_row_board), [])]
    visited = set()

    while len(fringe) > 0:
        curr_state = fringe.pop(0)
        board, _ = curr_state
        visited.add(compress_board(board))

        if is_solved(board, GOAL_STATE):
            solved_last_6_board, solve_last_6_steps = curr_state
            return list(itertools.chain(solve_top_row_steps, solve_left_col_steps, solve_2_top_row_steps, solve_last_6_steps))
        
        next_states = get_next_states(curr_state, 1, 2)
        if len(next_states) > 0:
            fringe.extend(next_states)

    return None