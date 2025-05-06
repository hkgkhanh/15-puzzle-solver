import copy
from collections import deque

GOAL_STATE = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

def find_pos(board, value):
    for i in range(4):
        for j in range(4):
            if board[i][j] == value:
                return (i, j)

def is_solvable(board):
    flat = sum(board, [])
    inv_count = 0
    for i in range(16):
        for j in range(i + 1, 16):
            if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                inv_count += 1
    zero_row = find_pos(board, 0)[0]
    return (inv_count % 2 == 0) if zero_row % 2 == 1 else (inv_count % 2 == 1)

def get_neighbors(board):
    zero_y, zero_x = find_pos(board, 0)
    neighbors = []
    moves = [("U", -1, 0), ("D", 1, 0), ("L", 0, -1), ("R", 0, 1)]
    for move, dy, dx in moves:
        ny, nx = zero_y + dy, zero_x + dx
        if 0 <= ny < 4 and 0 <= nx < 4:
            new_board = copy.deepcopy(board)
            new_board[zero_y][zero_x], new_board[ny][nx] = new_board[ny][nx], new_board[zero_y][zero_x]
            neighbors.append((new_board, move))
    return neighbors

def bfs_solver(initial_board):
    if not is_solvable(initial_board):
        return "No solution"

    start = tuple(sum(initial_board, []))
    goal = tuple(sum(GOAL_STATE, []))
    queue = deque([(initial_board, [])])
    visited = {start}

    while queue:
        current_board, path = queue.popleft()
        current_tuple = tuple(sum(current_board, []))

        if current_tuple == goal:
            return "".join(path)

        for neighbor, move in get_neighbors(current_board):
            neighbor_tuple = tuple(sum(neighbor, []))
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                queue.append((neighbor, path + [move]))

    return "No solution"
