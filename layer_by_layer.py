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

    # solve 5
    goal_y, goal_x = find_pos(GOAL_STATE, 5)
    cell_y, cell_x = find_pos(board, 5)
    zero_y, zero_x = find_pos(board, 0)

    if goal_y != cell_y or goal_x != cell_x:
        
        # move 0 to goal position
        if zero_y != goal_y:
            for _ in range(goal_y, zero_y):
                add_move(board, solution_steps, "U")
        
        if zero_x != goal_x:
            for _ in range(goal_x, zero_x):
                add_move(board, solution_steps, "L")

        # move 5 to goal position
        cell_y, cell_x = find_pos(board, 5)
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
            cell_y, cell_x = find_pos(board, 5)
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

    # solve 6
    goal_y, goal_x = find_pos(GOAL_STATE, 6)
    cell_y, cell_x = find_pos(board, 6)
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
            if zero_y != 2:
                for _ in range(1, zero_y):
                    add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "U")

        # move 6 to goal position
        cell_y, cell_x = find_pos(board, 6)
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
                cell_y, cell_x = find_pos(board, 6)
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
            sequence = ["D", "L", "D", "R", "R", "U", "U", "L"]

            sequence_index = 0
            prev_cell_y, prev_cell_x = cell_y, cell_x
            while cell_y != goal_y or cell_x != goal_x:
                add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                cell_y, cell_x = find_pos(board, 6)
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


    # solve 7 and 8
    if board[1][2] != 7 or board[1][3] != 8: # if 7 and 8 already solved then skip
        # put 8 to place of 7
        goal_y, goal_x = find_pos(GOAL_STATE, 7)
        cell_y, cell_x = find_pos(board, 8)
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

            # move 8 to goal position
            cell_y, cell_x = find_pos(board, 8)
            zero_y, zero_x = find_pos(board, 0)

            if cell_y >= goal_y and cell_x >= goal_x:
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
                    cell_y, cell_x = find_pos(board, 8)
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
            
                sequence.append("D")

                for _ in range(cell_x, goal_x + 1):
                    sequence.append("R")

                for _ in range(2):
                    sequence.append("U")
                sequence.append("L")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 8)
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

        # put 7 at the bottom of 8
        goal_y, goal_x = find_pos(GOAL_STATE, 11)
        cell_y, cell_x = find_pos(board, 7)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y != goal_y or cell_x != goal_x:

            # move 0 to the bottom of 8
            if zero_y == 1 and zero_x == 3: # top-right corner
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

            # now put 7 to the bottom of 8
            cell_y, cell_x = find_pos(board, 7)
            zero_y, zero_x = find_pos(board, 0)

            if cell_y == 1 and cell_x == 3: # 8 and 7 is in swap position
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
                    # count_D = 1
                    # if cell_y == 3:
                    #     count_D = 2
                    # for _ in range(count_D):
                    sequence.append("D")
                    for _ in range(abs(cell_x - goal_x)):
                        sequence.append("R")
                    # for _ in range(count_D):
                    sequence.append("U")

                    sequence_index = 0
                    prev_cell_y, prev_cell_x = cell_y, cell_x
                    while cell_y != goal_y or cell_x != goal_x:
                        add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                        cell_y, cell_x = find_pos(board, 7)
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
                    # count_D = 1
                    # if cell_y == 3:
                    #     count_D = 2
                    # for _ in range(count_D):
                    sequence.append("D")
                    sequence.append("R")
                    # for _ in range(count_D):
                    sequence.append("U")
                    sequence.append("L")

                    sequence_index = 0
                    prev_cell_y, prev_cell_x = cell_y, cell_x
                    while cell_y != goal_y or cell_x != goal_x:
                        add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                        cell_y, cell_x = find_pos(board, 7)
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

        # now solve 7 and 8
        # move 0 to top-right corner
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != 1 or zero_x != 3:

            if zero_y == 2 and zero_x <= 1:
                add_move(board, solution_steps, "D")
            
            zero_y, zero_x = find_pos(board, 0)
            for _ in range(3 - zero_x):
                add_move(board, solution_steps, "R")

            zero_y, zero_x = find_pos(board, 0)
            for _ in range(zero_y - 1):
                add_move(board, solution_steps, "U")

        # now solve 7 and 8
        add_move(board, solution_steps, "L")
        add_move(board, solution_steps, "D")



    # solve 9 and 13
    if board[2][0] != 9 or board[3][0] != 13:

        ## move 13 to position of 9
        # move 0 to position of 9
        goal_y, goal_x = find_pos(GOAL_STATE, 9)
        cell_y, cell_x = find_pos(board, 13)
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != goal_y or zero_x != goal_x:
            for _ in range(abs(zero_y - goal_y)):
                add_move(board, solution_steps, "U")
            for _ in range(abs(zero_x - goal_x)):
                add_move(board, solution_steps, "L")

        # move 13 to position of 9
        cell_y, cell_x = find_pos(board, 13)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y != goal_y or cell_x != goal_x:
            if cell_x == goal_x and cell_y == 3:
                add_move(board, solution_steps, "D")

            else:
                sequence = []
                for _ in range(abs(cell_x - goal_x)):
                    sequence.append("R")
                sequence.append("D")
                for _ in range(abs(cell_x - goal_x)):
                    sequence.append("L")
                sequence.append("U")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 13)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_x != cell_x and sequence.count("R") > 1:
                            sequence.remove("R")
                            sequence.remove("L")
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

        # move 0 next to 13
        goal_y, goal_x = find_pos(GOAL_STATE, 10)
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != goal_y or zero_x != goal_x:
            
            if zero_y == 3 and zero_x == 0:
                add_move(board, solution_steps, "R")
                add_move(board, solution_steps, "U")

            else:
                for _ in range(zero_x - goal_x):
                    add_move(board, solution_steps, "L")
                for _ in range(zero_y - goal_y):
                    add_move(board, solution_steps, "U")

        # solve 9 and 13
        goal_y, goal_x = find_pos(GOAL_STATE, 10)
        cell_y, cell_x = find_pos(board, 9)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y == 3 and cell_x == 0:
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "R")

        else:
            # put 9 next to 13
            if cell_y == 3 and cell_x == 1:
                add_move(board, solution_steps, "D")

            elif cell_x > goal_x:
                sequence = []
                for _ in range(cell_x - goal_x):
                    sequence.append("R")
                sequence.append("D")
                for _ in range(cell_x - goal_x):
                    sequence.append("L")
                sequence.append("U")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 9)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_x != cell_x and sequence.count("R") > 1:
                            sequence.remove("R")
                            sequence.remove("L")
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

            # move 0 to bottom-left corner
            goal_y, goal_x = find_pos(GOAL_STATE, 13)
            zero_y, zero_x = find_pos(board, 0)

            if zero_y == 2:
                add_move(board, solution_steps, "D")
            for _ in range(goal_x, zero_x):
                add_move(board, solution_steps, "L")

            # solve 9 and 13
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")

    
    # solve 10 and 14
    if board[2][1] != 10 or board[3][1] != 14:

        ## move 14 to position of 10
        # move 0 to position of 10
        goal_y, goal_x = find_pos(GOAL_STATE, 10)
        cell_y, cell_x = find_pos(board, 14)
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != goal_y or zero_x != goal_x:
            for _ in range(abs(zero_y - goal_y)):
                add_move(board, solution_steps, "U")
            for _ in range(abs(zero_x - goal_x)):
                add_move(board, solution_steps, "L")

        # move 14 to position of 10
        cell_y, cell_x = find_pos(board, 14)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y != goal_y or cell_x != goal_x:
            if cell_x == goal_x and cell_y == 3:
                add_move(board, solution_steps, "D")

            else:
                sequence = []
                for _ in range(abs(cell_x - goal_x)):
                    sequence.append("R")
                sequence.append("D")
                for _ in range(abs(cell_x - goal_x)):
                    sequence.append("L")
                sequence.append("U")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 14)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_x != cell_x and sequence.count("R") > 1:
                            sequence.remove("R")
                            sequence.remove("L")
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

        # move 0 next to 14
        goal_y, goal_x = find_pos(GOAL_STATE, 11)
        zero_y, zero_x = find_pos(board, 0)

        if zero_y != goal_y or zero_x != goal_x:
            
            if zero_y == 3 and zero_x == 1:
                add_move(board, solution_steps, "R")
                add_move(board, solution_steps, "U")

            else:
                for _ in range(zero_x - goal_x):
                    add_move(board, solution_steps, "L")
                for _ in range(zero_y - goal_y):
                    add_move(board, solution_steps, "U")

        # solve 10 and 14
        goal_y, goal_x = find_pos(GOAL_STATE, 11)
        cell_y, cell_x = find_pos(board, 10)
        zero_y, zero_x = find_pos(board, 0)

        if cell_y == 3 and cell_x == 1:
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "R")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "L")
            add_move(board, solution_steps, "D")
            add_move(board, solution_steps, "R")

        else:
            # put 10 next to 14
            if cell_y == 3 and cell_x == 2:
                add_move(board, solution_steps, "D")

            elif cell_x > goal_x:
                sequence = []
                for _ in range(cell_x - goal_x):
                    sequence.append("R")
                sequence.append("D")
                for _ in range(cell_x - goal_x):
                    sequence.append("L")
                sequence.append("U")

                sequence_index = 0
                prev_cell_y, prev_cell_x = cell_y, cell_x
                while cell_y != goal_y or cell_x != goal_x:
                    add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
                    cell_y, cell_x = find_pos(board, 10)
                    if (sequence_index + 1) % len(sequence) == 0:
                        if prev_cell_x != cell_x and sequence.count("R") > 1:
                            sequence.remove("R")
                            sequence.remove("L")
                        prev_cell_y, prev_cell_x = cell_y, cell_x
                        sequence_index = 0
                        continue
                    sequence_index += 1

            # move 0 to bottom-left corner
            goal_y, goal_x = find_pos(GOAL_STATE, 14)
            zero_y, zero_x = find_pos(board, 0)

            if zero_y == 2:
                add_move(board, solution_steps, "D")
            for _ in range(goal_x, zero_x):
                add_move(board, solution_steps, "L")

            # solve 10 and 14
            add_move(board, solution_steps, "U")
            add_move(board, solution_steps, "R")


    # solve last 3 pieces yayyyy
    sequence = ["D", "R", "U", "L"]
    sequence_index = 0

    zero_y, zero_x = find_pos(board, 0)

    if zero_y == 2 and zero_x == 2:
        sequence_index = 0
    elif zero_y == 2 and zero_x == 3:
        sequence_index = 3
    elif zero_y == 3 and zero_x == 2:
        sequence_index = 1
    else:
        sequence_index = 2

    while not is_solved(board, GOAL_STATE):
        add_move(board, solution_steps, sequence[sequence_index % len(sequence)])
        sequence_index += 1


    return solution_steps