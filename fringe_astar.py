import copy
import itertools
import sys
import heapq

# Tìm vị trí (i, j) của giá trị 'target' trên bàn cờ
def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j
            
# Kiểm tra toàn bộ bàn cờ đã đúng với trạng thái goal hay chưa
def is_solved(board, goal):
    for i in range(4):
        for j in range(4):
            if board[i][j] != goal[i][j]:
                return False
    return True

# Kiểm tra hàng trên cùng đã đúng hay chưa
def is_solved_top_row(board, goal):
    for i in range(4):
        if board[0][i] != goal[0][i]:
            return False
    return True

# Kiểm tra cột bên trái đã đúng hay chưa
def is_solved_left_col(board, goal):
    for i in range(4):
        if board[i][0] != goal[i][0]:
            return False
    return True

# Kiểm tra hàng thứ 2 từ trên xuống đã đúng hay chưa
def is_solved_2_top_row(board, goal):
    for i in range(4):
        if board[1][i] != goal[1][i]:
            return False
    return True

# Thêm một nước đi vào bàn cờ và cập nhật vị trí ô trống
def add_move(board, solution, move):
    dy, dx = 0, 0
    if move == "R":
        dx = 1
    elif move == "L":
        dx = -1
    elif move == "U":
        dy = -1
    elif move == "D":
        dy = 1

    solution.append(move)
    zero_y, zero_x = find_pos(board, 0)
    # Thực hiện hoán đổi
    board[zero_y][zero_x], board[zero_y + dy][zero_x + dx] = board[zero_y + dy][zero_x + dx], board[zero_y][zero_x]

# Sinh ra tất cả các trạng thái có thể từ trạng thái hiện tại, giới hạn theo boundary
def get_next_states(curr_state, boundary_x, boundary_y):
    board, moves = curr_state
    next_states = []

    zero_y, zero_x = find_pos(board, 0)
    # Nếu là bước đầu tiên cho phép tất cả các hướng
    if len(moves) == 0:
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
        # Giới hạn các hướng đi để tránh đi lại
        last_move = moves[-1]
        if last_move == "R":
            next_moves = ["R", "U", "D"]
        elif last_move == "L":
            next_moves = ["L", "U", "D"]
        elif last_move == "U":
            next_moves = ["R", "L", "U"]
        elif last_move == "D":
            next_moves = ["R", "L", "D"]

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

# Chuyển bàn cờ thành dạng chuỗi để lưu vào tập visited
def compress_board(board):
    return " ".join(str(board[i][j]) for i in range(4) for j in range(4))

# Mã hóa bàn cờ theo 1,2,3,4 và 0 để tra bảng lookup
def encode1234_board(board):
    encode_list = ["x", "x", "x", "x", "x"]
    for i in range(4):
        for j in range(4):
            if board[i][j] in [1, 2, 3, 4, 0]:
                index = {1:0, 2:1, 3:2, 4:3, 0:4}[board[i][j]]
                encode_list[index] = "0123456789abcdef"[i * 4 + j]
    return "".join(encode_list)

# Mã hóa bàn cờ theo 5,9,13 và 0 để tra bảng lookup
def encode5913_board(board):
    encode_list = ["x", "x", "x", "x"]
    for i in range(4):
        for j in range(4):
            if board[i][j] in [5, 9, 13, 0]:
                index = {5:0, 9:1, 13:2, 0:3}[board[i][j]]
                encode_list[index] = "0123456789abcdef"[i * 4 + j]
    return "".join(encode_list)

# Tính heuristic Manhattan distance chỉ cho phần 3x3 cuối
def manhattan_distance(board, goal):
    distance = 0
    for i in range(2, 4):
        for j in range(2, 4):
            if board[i][j] != 0:
                gi, gj = find_pos(goal, board[i][j])
                distance += abs(i - gi) + abs(j - gj)
    return distance

# Tính thêm heuristic linear conflict
def linear_conflicts(board, goal):
    conflicts = 0
    # Kiểm tra theo hàng
    for i in range(2, 4):
        for j in range(2, 4):
            if board[i][j] == 0:
                continue
            gi, gj = find_pos(goal, board[i][j])
            if gi == i:
                for k in range(j+1, 4):
                    if board[i][k] == 0:
                        continue
                    gki, gkj = find_pos(goal, board[i][k])
                    if gki == i and gkj < gj:
                        conflicts += 1
    # Kiểm tra theo cột
    for j in range(2, 4):
        for i in range(2, 4):
            if board[i][j] == 0:
                continue
            gi, gj = find_pos(goal, board[i][j])
            if gj == j:
                for k in range(i+1, 4):
                    if board[k][j] == 0:
                        continue
                    gki, gkj = find_pos(goal, board[k][j])
                    if gkj == j and gki < gi:
                        conflicts += 1
    return conflicts * 2

# Tổng hợp heuristic
def heuristic(board, goal):
    return manhattan_distance(board, goal) + linear_conflicts(board, goal)

# Hàm chính fringe_astar, kết hợp lookup table và A*
def fringe_astar(board, GOAL_STATE):
    # Giải hàng trên cùng bằng lookup table
    lookup1234 = {}
    init_board = copy.deepcopy(board)
    case1234 = encode1234_board(init_board)

    with open("top_row/1234.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            lookup1234[key] = list(value)
    
    moves_to_do = lookup1234[case1234]
    solution_steps = []
    for move in moves_to_do:
        add_move(init_board, solution_steps, move)

    solved_top_row_board = copy.deepcopy(init_board)
    solve_top_row_steps = copy.deepcopy(solution_steps)

    # Giải cột bên trái bằng lookup table
    lookup5913 = {}
    init_board = copy.deepcopy(solved_top_row_board)
    case5913 = encode5913_board(init_board)

    with open("left_col/5913.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            lookup5913[key] = list(value)
    
    moves_to_do = lookup5913[case5913]
    solution_steps = []
    for move in moves_to_do:
        add_move(init_board, solution_steps, move)

    solved_left_col_board = init_board
    solve_left_col_steps = copy.deepcopy(solution_steps)

    # Giải hàng thứ 2 bằng A*
    pq = [(heuristic(solved_left_col_board, GOAL_STATE), 0, compress_board(solved_left_col_board), (copy.deepcopy(solved_left_col_board), []))]
    heapq.heapify(pq)
    visited = set()
    visited.add(compress_board(solved_left_col_board))

    while pq:
        _, _, _, curr_state = heapq.heappop(pq)
        board, curr_moves = curr_state

        sys.stdout.write('\r\033[K' + " ".join(curr_moves))
        sys.stdout.flush()

        if is_solved_2_top_row(board, GOAL_STATE):
            solved_2_top_row_board, solve_2_top_row_steps = curr_state
            break
        
        next_states = get_next_states(curr_state, 1, 1)
        for next_state in next_states:
            next_board, next_moves = next_state
            board_str = compress_board(next_board)
            if board_str not in visited:
                visited.add(board_str)
                heapq.heappush(pq, (len(next_moves) + heuristic(next_board, GOAL_STATE), len(next_moves), board_str, next_state))

    # Giải 3x3 cuối cùng bằng A*
    pq = [(heuristic(solved_2_top_row_board, GOAL_STATE), 0, compress_board(solved_2_top_row_board), (copy.deepcopy(solved_2_top_row_board), []))]
    heapq.heapify(pq)
    visited = set()
    visited.add(compress_board(solved_2_top_row_board))

    while pq:
        _, _, _, curr_state = heapq.heappop(pq)
        board, curr_moves = curr_state

        sys.stdout.write('\r\033[K' + " ".join(solve_2_top_row_steps + curr_moves))
        sys.stdout.flush()

        if is_solved(board, GOAL_STATE):
            solved_last_6_board, solve_last_6_steps = curr_state
            return list(itertools.chain(solve_top_row_steps, solve_left_col_steps, solve_2_top_row_steps, solve_last_6_steps))
        
        next_states = get_next_states(curr_state, 1, 2)
        for next_state in next_states:
            next_board, next_moves = next_state
            board_str = compress_board(next_board)
            if board_str not in visited:
                visited.add(board_str)
                heapq.heappush(pq, (len(next_moves) + heuristic(next_board, GOAL_STATE), len(next_moves), board_str, next_state))

    return None
