import time


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




def solve_layer_by_layer(board, GOAL_STATE):
    # 1. Hoàn thành hàng đầu tiên (4 ô đầu tiên)
    # 2. Hoàn thành hàng thứ hai (4 ô tiếp theo)
    # 3. Giải 9 13 và 10 14
    # 4. Giải nốt 2x2 cuối cùng bằng cách cycle
    
    solution_steps = []
    
    # solve 1
    goal_y, goal_x = find_pos(GOAL_STATE, 1)
    cell_y, cell_x = find_pos(board, 1)
    zero_y, zero_x = find_pos(board, 0)

    if goal_y != cell_y or goal_x != cell_x:
        
        # move 0 to goal position
        if zero_y != goal_y:
            for _ in range(goal_y, zero_y):
                add_move(board, solution_steps, "U")
        
        if zero_x != goal_x:
            for _ in range(goal_x, zero_x):
                add_move(board, solution_steps, "L")

        # move 1 to goal position
        cell_y, cell_x = find_pos(board, 1)
        sequence = []

        if cell_y == goal_y and cell_x != goal_x:
            for _ in range(goal_x, cell_x):
                sequence.append("R")
            sequence.append("D")
            for _ in range(goal_x, cell_x):
                sequence.append("L")
            sequence.append("U")
        
        elif cell_y != goal_y and cell_x == goal_x:
            for _ in range(goal_y, cell_y):
                sequence.append("D")
            sequence.append("R")
            for _ in range(goal_y, cell_y):
                sequence.append("U")
            sequence.append("L")
        
        elif cell_y != goal_y and cell_x != goal_x:
            for _ in range(goal_x, cell_x):
                sequence.append("R")
            for _ in range(goal_y, cell_y):
                sequence.append("D")
            for _ in range(goal_x, cell_x):
                sequence.append("L")
            for _ in range(goal_y, cell_y):
                sequence.append("U")

        sequence_index = 0
        prev_cell_y, prev_cell_x = cell_y, cell_x
        while cell_y != goal_y or cell_x != goal_x:
            add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
            cell_y, cell_x = find_pos(board, 1)
            if (sequence_index + 1) % len(sequence) == 0:
                if prev_cell_x != cell_x and sequence.count("R") > 1:
                    sequence.remove("R")
                    sequence.remove("L")
                if prev_cell_y != cell_y and sequence.count("U") > 1:
                    sequence.remove("U")
                    sequence.remove("D")
                prev_cell_y, prev_cell_x = cell_y, cell_x
                sequence_index = 0
                continue
            # print(sequence)
            # print(sequence_index)
            # time.sleep(0.5)
            sequence_index += 1

    # return solution_steps
    # solve 2
    

    return solution_steps