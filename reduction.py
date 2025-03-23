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




def solve_reduction(board, GOAL_STATE):
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


    # solve 9 and 13
    if board[2][0] != 9 or board[3][0] != 13:

        ## move 13 to position of 9
        # move 0 to position of 9
        goal_y, goal_x = find_pos(GOAL_STATE, 9)
        cell_y, cell_x = find_pos(board, 13)
        zero_y, zero_x = find_pos(board, 0)

        

    
    


    return solution_steps