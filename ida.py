import copy

GOAL_STATE = [[1, 2, 3, 4], 
              [5, 6, 7, 8], 
              [9, 10, 11, 12], 
              [13, 14, 15, 0]]

DIRECTION = ['U', 'D', 'L', 'R']
MOVE_DELTA = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j

def move_tile(board, zero_pos, direction):
    zx, zy = zero_pos
    dx, dy = MOVE_DELTA[direction]
    new_x, new_y = zx + dx, zy + dy
    if 0 <= new_x < 4 and 0 <= new_y < 4:
        new_board = copy.deepcopy(board)
        new_board[zx][zy], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[zx][zy]
        return new_board, (new_x, new_y)
    return None, None

def manhattan_distance(board):
    distance = 0
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value != 0:
                goal_i, goal_j = (value - 1) // 4, (value - 1) % 4
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def ida_star(start_board):
    start = tuple(tuple(row) for row in start_board)
    goal = tuple(tuple(row) for row in GOAL_STATE)

    zero_pos = find_pos(start_board, 0)
    threshold = manhattan_distance(start_board)

    path = []
    visited = set()

    def dfs(board, zero_pos, g, threshold, path, prev_move):
        f = g + manhattan_distance(board)
        if f > threshold:
            return f
        if tuple(tuple(row) for row in board) == goal:
            return True
        
        min_cost = float('inf')
        for direction in DIRECTION:
            # Tránh quay ngược lại bước trước
            if (prev_move == 'U' and direction == 'D') or \
               (prev_move == 'D' and direction == 'U') or \
               (prev_move == 'L' and direction == 'R') or \
               (prev_move == 'R' and direction == 'L'):
                continue

            next_board, new_zero = move_tile(board, zero_pos, direction)
            if next_board is None:
                continue

            board_tuple = tuple(tuple(row) for row in next_board)
            if board_tuple in visited:
                continue

            visited.add(board_tuple)
            path.append(direction)
            result = dfs(next_board, new_zero, g + 1, threshold, path, direction)
            if result is True:
                return True
            if isinstance(result, int) and result < min_cost:
                min_cost = result
            path.pop()
            visited.remove(board_tuple)

        return min_cost

    while True:
        visited = {start}
        result = dfs(start_board, zero_pos, 0, threshold, path, "")
        if result is True:
            return path
        if result == float('inf'):
            return None
        threshold = result
