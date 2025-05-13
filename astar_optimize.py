import copy
import heapq

GOAL_STATE = [[1, 2, 3, 4], 
              [5, 6, 7, 8], 
              [9, 10, 11, 12], 
              [13, 14, 15, 0]]

# -----------------------
# Utility Functions
# -----------------------

def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j

def move_tile(board, zero_pos, tile_pos):
    new_board = copy.deepcopy(board)
    zx, zy = zero_pos
    tx, ty = tile_pos
    new_board[zx][zy], new_board[tx][ty] = new_board[tx][ty], new_board[zx][zy]
    return new_board

def manhattan_distance(board):
    distance = 0
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // 4, (value - 1) % 4
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

# -----------------------
# A* with Locked Tiles
# -----------------------

def get_neighbors_with_lock(board, locked_set):
    zero_pos = find_pos(board, 0)
    zx, zy = zero_pos
    neighbors = []
    moves = [("U", (zx - 1, zy)), ("D", (zx + 1, zy)), ("L", (zx, zy - 1)), ("R", (zx, zy + 1))]
    for move, (nx, ny) in moves:
        if 0 <= nx < 4 and 0 <= ny < 4:
            if (nx, ny) in locked_set:
                continue
            new_board = move_tile(board, zero_pos, (nx, ny))
            neighbors.append((new_board, move))
    return neighbors

def a_star_with_lock(start_board, goal_board, locked_set):
    start = tuple(tuple(row) for row in start_board)
    goal = tuple(tuple(row) for row in goal_board)

    if start == goal:
        return []

    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start_board), 0, start, []))
    visited = {}

    while open_list:
        f, g, current_tuple, path = heapq.heappop(open_list)

        if current_tuple == goal:
            return path

        if current_tuple in visited and visited[current_tuple] <= g:
            continue

        visited[current_tuple] = g
        current = [list(row) for row in current_tuple]

        for next_board, move in get_neighbors_with_lock(current, locked_set):
            next_tuple = tuple(tuple(row) for row in next_board)
            new_g = g + 1
            h = manhattan_distance(next_board)
            heapq.heappush(open_list, (new_g + h, new_g, next_tuple, path + [move]))

    return None

# -----------------------
# Step-by-step Solver
# -----------------------

def solve_partial(initial, targets, locked_set):
    """Giải một phần của board sao cho các giá trị trong 'targets' vào đúng vị trí."""
    goal = copy.deepcopy(initial)
    for i in range(4):
        for j in range(4):
            goal[i][j] = initial[i][j]
    for val in targets:
        gx, gy = find_pos(GOAL_STATE, val)
        goal[gx][gy] = val
    path = a_star_with_lock(initial, goal, locked_set)
    board = initial
    for move in path:
        board = apply_move(board, move)
    return board, path

def apply_move(board, move):
    zx, zy = find_pos(board, 0)
    dx = {"U": -1, "D": 1, "L": 0, "R": 0}
    dy = {"U": 0, "D": 0, "L": -1, "R": 1}
    nx, ny = zx + dx[move], zy + dy[move]
    return move_tile(board, (zx, zy), (nx, ny))

def layered_solver(initial_board):
    board = initial_board
    total_path = []
    locked = set()

    # Step 1: Solve top row (1, 2, 3, 4)
    board, path = solve_partial(board, [1, 2, 3, 4], locked)
    total_path += path
    for i in range(4):
        locked.add((0, i))

    # Step 2: Solve left column (5, 9, 13)
    board, path = solve_partial(board, [5, 9, 13], locked)
    total_path += path
    for i in range(1, 4):
        locked.add((i, 0))

    # Step 3: Solve second row (6, 7, 8)
    board, path = solve_partial(board, [6, 7, 8], locked)
    total_path += path
    for i in range(1, 4):
        locked.add((1, i))

    # Step 4: Solve second column (10, 14)
    board, path = solve_partial(board, [10, 14], locked)
    total_path += path
    for i in range(2, 4):
        locked.add((i, 1))

    # Step 5: Solve last 2x2 (11, 12, 15, 0)
    # Assume already solvable in this state — apply A* normally
    final_goal = GOAL_STATE
    path = a_star_with_lock(board, final_goal, locked)
    total_path += path

    return total_path

# -----------------------
# Example usage
# -----------------------

if __name__ == "__main__":
    initial = [
        [5, 1, 2, 4],
        [0, 6, 3, 8],
        [9, 10, 7, 12],
        [13, 14, 11, 15]
    ]
    steps = layered_solver(initial)
    print("Steps to solve:", "".join(steps))
