import heapq
from utils import find_position, get_neighbors

GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

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