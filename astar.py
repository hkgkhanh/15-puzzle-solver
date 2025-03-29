import heapq
from copy import deepcopy

directions = {(0, 1): "R", (0, -1): "L", (1, 0): "D", (-1, 0): "U"}

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

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current, move = came_from[current]
        path.append(move)
    path.reverse()
    return path

def solve_astar(initial_board, goal_state):
    size = len(initial_board)
    goal_list = sum(goal_state, [])
    print(initial_board);
    print(goal_state);
    open_set = []
    heapq.heappush(open_set, (0, initial_board))
    came_from = {}
    g_score = {str(initial_board): 0}
    f_score = {str(initial_board): manhattan_distance(initial_board, goal_list)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal_state:
            return reconstruct_path(came_from, str(current))
        
        for neighbor, _, move in get_neighbors(current):
            tentative_g_score = g_score[str(current)] + 1
            neighbor_str = str(neighbor)
            
            if neighbor_str not in g_score or tentative_g_score < g_score[neighbor_str]:
                came_from[neighbor_str] = (str(current), move)
                g_score[neighbor_str] = tentative_g_score
                f_score[neighbor_str] = tentative_g_score + manhattan_distance(neighbor, goal_list)
                heapq.heappush(open_set, (f_score[neighbor_str], neighbor))
    
    return None


# if __name__ == "__main__":
#     initial_board = [
#         [3, 15, 7, 8],
#         [12, 0, 5, 10],
#         [2, 1, 13, 14],
#         [6, 9, 4, 11]
#     ]
    
#     goal_state = [
#         [1, 2, 3, 4],
#         [5, 6, 7, 8],
#         [9, 10, 11, 12],
#         [13, 14, 15, 0]
#     ]
#     solution = solve_astar(initial_board,goal_state);
#     print(solution)
    