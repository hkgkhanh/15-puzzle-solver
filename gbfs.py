import copy
import heapq

GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


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


def get_neighbors(board):
    zero_pos = find_pos(board, 0)
    zx, zy = zero_pos
    neighbors = []
    moves = [
        ("U", (zx - 1, zy)),  
        ("D", (zx + 1, zy)),  
        ("L", (zx, zy - 1)),  
        ("R", (zx, zy + 1))  
    ]
   
    for move, (new_x, new_y) in moves:
        if 0 <= new_x < 4 and 0 <= new_y < 4:
            new_board = move_tile(board, zero_pos, (new_x, new_y))
            neighbors.append((new_board, move))
   
    return neighbors

def manhattan_distance(board):
    distance = 0
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value != 0:
                goal_pos = (value - 1) // 4, (value - 1) % 4
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance



def greedy_best_first_search(initial_board):
    start = tuple(tuple(row) for row in initial_board)
    goal = tuple(tuple(row) for row in GOAL_STATE)
    
    if start == goal:
        return []
    
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(initial_board), start, []))
    
    visited = set()
    
    while open_list:
        _, current_tuple, moves = heapq.heappop(open_list)
        
        if current_tuple == goal:
            return moves
        
        if current_tuple in visited:
            continue
        
        visited.add(current_tuple)
        current = [list(row) for row in current_tuple]
        
        for next_board, move in get_neighbors(current):
            next_tuple = tuple(tuple(row) for row in next_board)
            if next_tuple not in visited:
                new_moves = moves + [move]
                heapq.heappush(open_list, (manhattan_distance(next_board), next_tuple, new_moves))
    
    return None

def XYZ(matrix):
    steps = greedy_best_first_search(matrix)
    if steps is None:
        return "No solution"
    return "".join(steps)