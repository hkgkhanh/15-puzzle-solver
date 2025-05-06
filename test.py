import heapq
from copy import deepcopy

# Các hướng di chuyển
directions = {(0, 1): "R", (0, -1): "L", (1, 0): "D", (-1, 0): "U"}

# Hàm tính Manhattan distance
def manhattan_distance(board, goal):
    size = len(board)
    distance = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                continue
            goal_x, goal_y = divmod(goal.index(board[i][j]), size)
            distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

# Tạo các trạng thái láng giềng
def get_neighbors(board):
    size = len(board)
    neighbors = []
    zero_pos = [(i, row.index(0)) for i, row in enumerate(board) if 0 in row][0]
    x, y = zero_pos
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            new_board = deepcopy(board)
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append((new_board, (nx, ny), directions[(dx, dy)]))
    
    return neighbors

# Hàm xây dựng lại đường đi từ trạng thái cuối
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current, move = came_from[current]
        path.append(move)
    path.reverse()
    return ''.join(path)  # Trả về chuỗi di chuyển như 'RUDL'

# Thuật toán A*
def solve_astar(initial_board, goal_state):
    size = len(initial_board)
    goal_list = sum(goal_state, [])
    
    open_set = []
    heapq.heappush(open_set, (0, initial_board))
    
    came_from = {}
    g_score = {tuple(map(tuple, initial_board)): 0}
    f_score = {tuple(map(tuple, initial_board)): manhattan_distance(initial_board, goal_list)}
    
    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal_state:
            return reconstruct_path(came_from, tuple(map(tuple, current)))

        closed_set.add(tuple(map(tuple, current)))

        for neighbor, _, move in get_neighbors(current):
            neighbor_tuple = tuple(map(tuple, neighbor))
            if neighbor_tuple in closed_set:
                continue

            tentative_g_score = g_score[tuple(map(tuple, current))] + 1
            
            if neighbor_tuple not in g_score or tentative_g_score < g_score[neighbor_tuple]:
                came_from[neighbor_tuple] = (tuple(map(tuple, current)), move)
                g_score[neighbor_tuple] = tentative_g_score
                f_score[neighbor_tuple] = tentative_g_score + manhattan_distance(neighbor, goal_list)
                heapq.heappush(open_set, (f_score[neighbor_tuple], neighbor))
    
    return None

# Ví dụ sử dụng
initial_board = [
    [0, 10, 7, 11],
    [5, 6, 2, 13],
    [3, 9, 12, 14],
    [8, 1, 15, 4]
]

goal_state = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

solution = solve_astar(initial_board, goal_state)
print(f"Solution: {solution}")
