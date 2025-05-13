import copy
import sys

MAX_STATES_COUNT = 524160

def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j
            
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

def encode_board(board):
    encode_list = ["x", "x", "x", "x", "x"]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                encode_list[0] = "0123456789abcdef"[i * 4 + j]
            elif board[i][j] == 2:
                encode_list[1] = "0123456789abcdef"[i * 4 + j]
            elif board[i][j] == 3:
                encode_list[2] = "0123456789abcdef"[i * 4 + j]
            elif board[i][j] == 4:
                encode_list[3] = "0123456789abcdef"[i * 4 + j]
            elif board[i][j] == 0:
                encode_list[4] = "0123456789abcdef"[i * 4 + j]

    encode_str = "".join(encode_list)
    return encode_str

def get_solu_str(moves):
    solu_str = []
    for move in reversed(moves):
        if move == "R":
            solu_str.append("L")
        if move == "L":
            solu_str.append("R")
        if move == "U":
            solu_str.append("D")
        if move == "D":
            solu_str.append("U")

    return "".join(solu_str)

if __name__ == "__main__":
    board = [
        [1,2,3,4],
        [0,-1,-1,-1],
        [-1,-1,-1,-1],
        [-1,-1,-1,-1]
    ]
    
    fringe = [(copy.deepcopy(board), [])]
    visited = set()
    states_covered = 0

    while len(fringe) > 0:
        curr_state = fringe.pop(0)
        board, moves = curr_state
        encode_str = encode_board(board)

        if encode_str not in visited:
            visited.add(encode_str)

            reversed_moves_str = get_solu_str(moves)

            with open("top_row/1234.txt", "a") as file:
                file.write(f"{encode_str}:{reversed_moves_str}\n")

            states_covered += 1
            sys.stdout.write('\r\033[K' + f"{states_covered}")

        if states_covered >= MAX_STATES_COUNT:
            # solved_top_row_board, solve_top_row_steps = curr_state
            # return solution_steps
            break
        
        next_states = get_next_states(curr_state, 0, 0)
        # if len(next_states) > 0:
        #     fringe.extend(next_states)
        for next_state in next_states:
            next_board, _ = next_state
            if encode_board(next_board) not in visited:
                fringe.append(next_state)
        