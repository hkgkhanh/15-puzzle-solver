import copy
from collections import deque
import threading
import time

def find_pos(board, value):
    """Find the (row, col) position of a given value in the 4x4 board."""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == value:
                return (i, j)
    return None

def is_solvable(board):
    """Check if a given 15-puzzle board is solvable."""
    flat_board = sum(board, [])
    inv_count = 0

    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] and flat_board[j] and flat_board[i] > flat_board[j]:
                inv_count += 1

    zero_row = find_pos(board, 0)[0]  # Get row of blank (0)
    return (inv_count % 2 == 0) if zero_row % 2 == 1 else (inv_count % 2 == 1)

def solve_bfs(initial_board, goal_state):
    """Giải bài toán 15-puzzle bằng BFS và trả về danh sách các bước di chuyển."""
    
    def get_neighbors(board):
        """Sinh các trạng thái bảng kế tiếp bằng cách di chuyển ô trống."""
        zero_y, zero_x = find_pos(board, 0)
        neighbors = []
        possible_moves = ["U", "D", "L", "R"]
        move_offsets = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        
        for move in possible_moves:
            dy, dx = move_offsets[move]
            new_y, new_x = zero_y + dy, zero_x + dx
            
            if 0 <= new_y < 4 and 0 <= new_x < 4:
                new_board = copy.deepcopy(board)
                new_board[zero_y][zero_x], new_board[new_y][new_x] = (
                    new_board[new_y][new_x],
                    new_board[zero_y][zero_x],
                )
                neighbors.append((new_board, move))  # Lưu trạng thái và bước đi
        return neighbors
    
    def board_to_tuple(board):
        """Chuyển đổi bảng thành tuple để dùng làm khóa trong tập visited."""
        return tuple(sum(board, []))

    if not is_solvable(initial_board):
        return []  # Trả về danh sách rỗng nếu trạng thái không giải được

    initial_state = (initial_board, [])  # (bảng, đường đi đến đây)
    queue = deque([initial_state])
    visited = {board_to_tuple(initial_board)}
    goal_tuple = board_to_tuple(goal_state)
    
    while queue:
        current_board, path = queue.popleft()
        if board_to_tuple(current_board) == goal_tuple:
            return path  # Trả về đường đi nếu tìm thấy lời giải

        for neighbor_board, move in get_neighbors(current_board):
            neighbor_tuple = board_to_tuple(neighbor_board)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                queue.append((neighbor_board, path + [move]))
    
    return []  # Trả về danh sách rỗng nếu không có lời giải
