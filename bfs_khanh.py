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
    # fringe = [(copy.deepcopy(board), [])]
    # visited = set()

    # while len(fringe) > 0:
    #     curr_state = fringe.pop(0)
    #     board, _ = curr_state
    #     visited.add(compress_board(board))

    #     if is_solved_top_row(board, GOAL_STATE):
    #         solved_top_row_board, solve_top_row_steps = curr_state
    #         # return solution_steps
    #         break
        
    #     next_states = get_next_states(curr_state, 0, 0)
    #     # if len(next_states) > 0:
    #     #     fringe.extend(next_states)
    #     for next_state in next_states:
    #         next_board, _ = next_state
    #         if compress_board(next_board) not in visited:
    #             fringe.append(next_state)

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
            sequence_index += 1

    # return solution_steps
    # solve 2
    goal_y, goal_x = find_pos(GOAL_STATE, 2)
    cell_y, cell_x = find_pos(board, 2)
    zero_y, zero_x = find_pos(board, 0)

    if cell_y != goal_y or cell_x != goal_x:

        # move 0 to goal position
        if zero_x != 0:
            if zero_y != goal_y:
                for _ in range(goal_y, zero_y):
                    add_move(board, solution_steps, "U")
            
            if zero_x != goal_x:
                for _ in range(goal_x, zero_x):
                    add_move(board, solution_steps, "L")

        else:
            if zero_y != 1:
                for _ in range(1, zero_y):
                    add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "U")

        # move 2 to goal position
        cell_y, cell_x = find_pos(board, 2)
        zero_y, zero_x = find_pos(board, 0)

        if cell_x != 0:
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
                cell_y, cell_x = find_pos(board, 2)
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
                sequence_index += 1

        else:
            sequence = ["D", "L"]
            depth = cell_y
            if depth == 1:
                depth += 1
            
            for _ in range(depth - 1):
                sequence.append("D")
            sequence.append("R")
            sequence.append("R")
            for _ in range(depth):
                sequence.append("U")
            sequence.append("L")

            sequence_index = 0
            prev_cell_y, prev_cell_x = cell_y, cell_x
            while cell_y != goal_y or cell_x != goal_x:
                add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                cell_y, cell_x = find_pos(board, 2)
                if (sequence_index + 1) % len(sequence) == 0:
                    if prev_cell_y != cell_y and sequence.count("D") > 2:
                        sequence.reverse()
                        sequence.remove("U")
                        sequence.remove("D")
                        sequence.reverse()
                    prev_cell_y, prev_cell_x = cell_y, cell_x
                    sequence_index = 0
                    continue
                sequence_index += 1

    # return solution_steps

    if board[0][2] != 3 or board[0][3] != 4: # if 3 and 4 already solved then skip
        # put 4 to place of 3
        goal_y, goal_x = find_pos(GOAL_STATE, 3)
        cell_y, cell_x = find_pos(board, 4)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y != goal_y or cell_x != goal_x:

            # move 0 to goal position
            if zero_x != goal_x:
                if zero_x > goal_x:
                    for _ in range(goal_x, zero_x):
                        add_move(board, solution_steps, "L")
                if zero_x < goal_x:
                    for _ in range(zero_x, goal_x):
                        add_move(board, solution_steps, "R")

                if zero_y != goal_y:
                    for _ in range(goal_y, zero_y):
                        add_move(board, solution_steps, "U")

            # return solution_steps

            # move 4 to goal position
            cell_y, cell_x = find_pos(board, 4)
            zero_y, zero_x = find_pos(board, 0)

            if cell_y >= goal_y and cell_x >= goal_x:
                sequence = []
                count_D = 1
                if cell_y > 0:
                    count_D = cell_y
                
                for _ in range(count_D):
                    sequence.append("D")
                sequence.append("R")
                for _ in range(count_D):
                    sequence.append("U")
                sequence.append("L")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 4)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_y != cell_y and sequence.count("U") > 1:
                            sequence.remove("U")
                            sequence.remove("D")
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

            if cell_x < goal_x:
                sequence = ["D"]
                for _ in range(cell_x, goal_x):
                    sequence.append("L")
                
                count_D = 1
                if cell_y == 3:
                    count_D = 2
                for _ in range(count_D):
                    sequence.append("D")

                for _ in range(cell_x, goal_x + 1):
                    sequence.append("R")

                for _ in range(count_D + 1):
                    sequence.append("U")
                sequence.append("L")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 4)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_x != cell_x and sequence.count("R") > 2:
                            sequence.remove("R")
                            sequence.remove("L")
                        if prev_cell_y != cell_y and sequence.count("U") > 2:
                            sequence.reverse()
                            sequence.remove("U")
                            sequence.remove("D")
                            sequence.reverse()
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

        # return solution_steps

        # put 3 at the bottom of 4
        goal_y, goal_x = find_pos(GOAL_STATE, 7)
        cell_y, cell_x = find_pos(board, 3)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y != goal_y or cell_x != goal_x:

            # move 0 to the bottom of 4
            if zero_y == 0 and zero_x == 3: # top-right corner
                add_move(board, solution_steps, "D")
                add_move(board, solution_steps, "L")

            elif zero_y != goal_y or zero_x != goal_x:
                if zero_x > goal_x:
                    add_move(board, solution_steps, "L")
                else:
                    for _ in range(abs(zero_x - goal_x)):
                        add_move(board, solution_steps, "R")

                if zero_y > goal_y:
                    for _ in range(abs(zero_y - goal_y)):
                        add_move(board, solution_steps, "U")

            # now put 3 to the bottom of 4
            cell_y, cell_x = find_pos(board, 3)
            zero_y, zero_x = find_pos(board, 0)

            if cell_y == 0 and cell_x == 3: # 4 and 3 is in swap position
                add_move(board, solution_steps, "R")
                add_move(board, solution_steps, "U")
                add_move(board, solution_steps, "L")
                add_move(board, solution_steps, "D")
                add_move(board, solution_steps, "D")
                add_move(board, solution_steps, "R")
                add_move(board, solution_steps, "U")
                add_move(board, solution_steps, "L")
                add_move(board, solution_steps, "U")
                add_move(board, solution_steps, "R")
                add_move(board, solution_steps, "D")
                add_move(board, solution_steps, "D")
                add_move(board, solution_steps, "L")
                add_move(board, solution_steps, "U")
                add_move(board, solution_steps, "R")

            else:
                if cell_x < goal_x:
                    sequence = []
                    for _ in range(abs(cell_x - goal_x)):
                        sequence.append("L")
                    count_D = 1
                    if cell_y == 3:
                        count_D = 2
                    for _ in range(count_D):
                        sequence.append("D")
                    for _ in range(abs(cell_x - goal_x)):
                        sequence.append("R")
                    for _ in range(count_D):
                        sequence.append("U")

                    sequence_index = 0
                    prev_cell_y, prev_cell_x = cell_y, cell_x
                    while cell_y != goal_y or cell_x != goal_x:
                        add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                        cell_y, cell_x = find_pos(board, 3)
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
                        sequence_index += 1

                else:
                    sequence = []
                    count_D = 1
                    if cell_y == 3:
                        count_D = 2
                    for _ in range(count_D):
                        sequence.append("D")
                    sequence.append("R")
                    for _ in range(count_D):
                        sequence.append("U")
                    sequence.append("L")

                    sequence_index = 0
                    prev_cell_y, prev_cell_x = cell_y, cell_x
                    while cell_y != goal_y or cell_x != goal_x:
                        add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                        cell_y, cell_x = find_pos(board, 3)
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
                        sequence_index += 1

        # now solve 3 and 4
        # move 0 to top-right corner
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != 0 or zero_x != 3:

            if zero_y == 1 and zero_x <= 1:
                add_move(board, solution_steps, "D")
            
            zero_y, zero_x = find_pos(board, 0)
            for _ in range(3 - zero_x):
                add_move(board, solution_steps, "R")

            zero_y, zero_x = find_pos(board, 0)
            for _ in range(zero_y):
                add_move(board, solution_steps, "U")

        # now solve 3 and 4
        add_move(board, solution_steps, "L")
        add_move(board, solution_steps, "D")

    solved_top_row_board = board
    solve_top_row_steps = solution_steps

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
        # if len(next_states) > 0:
        #     fringe.extend(next_states)
        for next_state in next_states:
            next_board, _ = next_state
            if compress_board(next_board) not in visited:
                fringe.append(next_state)

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
        # if len(next_states) > 0:
        #     fringe.extend(next_states)
        for next_state in next_states:
            next_board, _ = next_state
            if compress_board(next_board) not in visited:
                fringe.append(next_state)

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
        # if len(next_states) > 0:
        #     fringe.extend(next_states)
        for next_state in next_states:
            next_board, _ = next_state
            if compress_board(next_board) not in visited:
                fringe.append(next_state)

    return None