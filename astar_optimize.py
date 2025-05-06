import heapq
import copy
from collections import deque

def solve_astar_optimized(initial_board, goal_state):
    """
    Giải 15-puzzle bằng A* tối ưu theo layer-by-layer
    Chiến lược: Giải hàng trên cùng, rồi cột trái cùng, sau đó thu nhỏ bài toán thành (n-1)x(n-1)
    """
    # Khởi tạo các thông số
    board = copy.deepcopy(initial_board)
    size = len(board)
    
    # Lưu chuỗi các bước di chuyển
    all_moves = []
    
    # Giải từng lớp một, bắt đầu từ kích thước ban đầu và giảm dần
    current_size = size
    while current_size > 2:
        # Đặt số 1,2,3,4 vào hàng đầu (trừ góc phải)
        moves = solve_first_row(board, current_size)
        all_moves.extend(moves)
        
        # Đặt số 5,9,13 vào cột đầu (trừ góc dưới)
        moves = solve_first_column(board, current_size)
        all_moves.extend(moves)
        
        # Giảm kích thước của bài toán
        current_size -= 1
    
    # Giải khối 2x2 còn lại
    moves = solve_2x2(board)
    all_moves.extend(moves)
    
    return all_moves

def manhattan_distance(board, target_pos):
    """Tính khoảng cách Manhattan giữa vị trí hiện tại của các ô và vị trí đích"""
    distance = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:  # Bỏ qua ô trống
                # Tìm vị trí đích của số hiện tại
                target_y, target_x = target_pos[board[i][j]]
                distance += abs(i - target_y) + abs(j - target_x)
    return distance

def get_target_positions(goal_state):
    """Tạo dictionary lưu vị trí đích cho mỗi số"""
    target_pos = {}
    for i in range(len(goal_state)):
        for j in range(len(goal_state[i])):
            target_pos[goal_state[i][j]] = (i, j)
    return target_pos

def find_pos(board, target):
    """Tìm vị trí của số target trên bảng"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == target:
                return i, j
    return -1, -1

def get_valid_moves(board, zero_y, zero_x, fixed_positions=None):
    """Trả về các nước đi hợp lệ từ vị trí hiện tại, không di chuyển các ô đã cố định"""
    moves = []
    directions = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]
    
    for move, dy, dx in directions:
        new_y, new_x = zero_y + dy, zero_x + dx
        
        # Kiểm tra nước đi có hợp lệ không
        if 0 <= new_y < len(board) and 0 <= new_x < len(board[0]):
            # Nếu có danh sách vị trí cố định, kiểm tra xem ô đó có được phép di chuyển không
            if fixed_positions is None or (new_y, new_x) not in fixed_positions:
                moves.append(move)
    
    return moves

def apply_move(board, move):
    """Áp dụng nước đi vào bảng hiện tại và trả về bảng mới"""
    zero_y, zero_x = find_pos(board, 0)
    new_board = copy.deepcopy(board)
    
    if move == 'U' and zero_y > 0:
        new_board[zero_y][zero_x], new_board[zero_y-1][zero_x] = new_board[zero_y-1][zero_x], new_board[zero_y][zero_x]
    elif move == 'D' and zero_y < len(board) - 1:
        new_board[zero_y][zero_x], new_board[zero_y+1][zero_x] = new_board[zero_y+1][zero_x], new_board[zero_y][zero_x]
    elif move == 'L' and zero_x > 0:
        new_board[zero_y][zero_x], new_board[zero_y][zero_x-1] = new_board[zero_y][zero_x-1], new_board[zero_y][zero_x]
    elif move == 'R' and zero_x < len(board[0]) - 1:
        new_board[zero_y][zero_x], new_board[zero_y][zero_x+1] = new_board[zero_y][zero_x+1], new_board[zero_y][zero_x]
    
    return new_board

def board_to_tuple(board):
    """Chuyển đổi bảng thành tuple để có thể sử dụng làm key trong dictionary"""
    return tuple(tuple(row) for row in board)

def solve_specific_position(board, target_number, target_y, target_x, fixed_positions=None):
    """
    Sử dụng A* để đặt một số cụ thể vào vị trí mục tiêu
    """
    # Tìm vị trí hiện tại của số cần di chuyển và ô trống
    current_y, current_x = find_pos(board, target_number)
    zero_y, zero_x = find_pos(board, 0)
    
    # Nếu số đã ở đúng vị trí, không cần làm gì
    if current_y == target_y and current_x == target_x:
        return []
    
    # Khởi tạo A*
    open_set = []
    closed_set = set()
    
    # g: chi phí từ trạng thái ban đầu đến trạng thái hiện tại
    # h: ước lượng chi phí từ trạng thái hiện tại đến mục tiêu
    # f = g + h
    start_h = abs(current_y - target_y) + abs(current_x - target_x) + abs(zero_y - current_y) + abs(zero_x - current_x)
    
    # (f, heuristic, board_tuple, moves, zero_position)
    heapq.heappush(open_set, (start_h, start_h, board_to_tuple(board), [], (zero_y, zero_x)))
    
    while open_set:
        _, h, current_board_tuple, moves, (zero_y, zero_x) = heapq.heappop(open_set)
        current_board = [list(row) for row in current_board_tuple]
        
        # Nếu đã xét trạng thái này, bỏ qua
        if current_board_tuple in closed_set:
            continue
        
        # Thêm trạng thái vào closed set
        closed_set.add(current_board_tuple)
        
        # Kiểm tra xem số đã ở đúng vị trí chưa
        current_y, current_x = find_pos(current_board, target_number)
        if current_y == target_y and current_x == target_x:
            return moves
        
        # Xem xét các nước đi hợp lệ
        valid_moves = get_valid_moves(current_board, zero_y, zero_x, fixed_positions)
        
        for move in valid_moves:
            new_board = apply_move(current_board, move)
            new_zero_y, new_zero_x = find_pos(new_board, 0)
            
            # Tìm vị trí mới của số cần di chuyển
            new_target_y, new_target_x = find_pos(new_board, target_number)
            
            # Tính h mới
            new_h = abs(new_target_y - target_y) + abs(new_target_x - target_x)
            new_h += abs(new_zero_y - new_target_y) + abs(new_zero_x - new_target_x)
            
            # Kiểm tra xem trạng thái mới đã được xét chưa
            new_board_tuple = board_to_tuple(new_board)
            if new_board_tuple not in closed_set:
                # f = g + h, với g là độ dài đường đi hiện tại (len(moves) + 1)
                f = len(moves) + 1 + new_h
                heapq.heappush(open_set, (f, new_h, new_board_tuple, moves + [move], (new_zero_y, new_zero_x)))
    
    # Nếu không tìm được giải pháp
    return []

def solve_first_row(board, size):
    """Giải hàng đầu tiên của puzzle"""
    moves = []
    
    # Danh sách các vị trí đã cố định, ban đầu rỗng
    fixed_positions = set()
    
    # Giải các số từ 1 đến size-1 vào hàng đầu
    for target_num in range(1, size):
        target_y, target_x = 0, target_num - 1
        
        # Tìm đường đi để đặt số vào vị trí đúng
        solution_moves = solve_specific_position(board, target_num, target_y, target_x, fixed_positions)
        
        # Áp dụng các nước đi
        for move in solution_moves:
            board = apply_move(board, move)
            moves.append(move)
        
        # Đánh dấu vị trí này đã cố định
        fixed_positions.add((target_y, target_x))
    
    # Giải số cuối cùng của hàng đầu (size)
    target_num = size
    target_y, target_x = 0, size - 1
    
    # Chiến lược đặc biệt để đặt số cuối cùng của hàng
    current_y, current_x = find_pos(board, target_num)
    zero_y, zero_x = find_pos(board, 0)
    
    # Nếu số chưa ở đúng vị trí
    if current_y != target_y or current_x != target_x:
        # Cần xử lý đặc biệt cho góc trên phải
        # Đưa số về vị trí (1, size-1) (ngay dưới vị trí đích)
        solution_moves = solve_specific_position(board, target_num, 1, size-1, fixed_positions)
        
        # Áp dụng các nước đi
        for move in solution_moves:
            board = apply_move(board, move)
            moves.append(move)
        
        # Đưa ô trống lên trên góc phải
        zero_y, zero_x = find_pos(board, 0)
        if zero_y != 0 or zero_x != size-1:
            solution_moves = solve_specific_position(board, 0, 0, size-1, fixed_positions - {(1, size-1)})
            
            for move in solution_moves:
                board = apply_move(board, move)
                moves.append(move)
        
        # Thực hiện chuỗi di chuyển UR-DL để đặt số vào vị trí
        moves.extend(['D', 'L', 'U', 'R'])
        board = apply_move(apply_move(apply_move(apply_move(board, 'D'), 'L'), 'U'), 'R')
    
    # Cập nhật danh sách các vị trí đã cố định
    for x in range(size):
        fixed_positions.add((0, x))
    
    return moves

def solve_first_column(board, size):
    """Giải cột đầu tiên của puzzle"""
    moves = []
    
    # Danh sách các vị trí đã cố định
    fixed_positions = set()
    for x in range(size):
        fixed_positions.add((0, x))  # Hàng đầu đã cố định
    
    # Giải các số từ size+1 đến (size-1)*size+1 vào cột đầu (bỏ qua góc dưới cùng)
    for i in range(1, size-1):
        target_num = i * size + 1
        target_y, target_x = i, 0
        
        # Tìm đường đi để đặt số vào vị trí đúng
        solution_moves = solve_specific_position(board, target_num, target_y, target_x, fixed_positions)
        
        # Áp dụng các nước đi
        for move in solution_moves:
            board = apply_move(board, move)
            moves.append(move)
        
        # Đánh dấu vị trí này đã cố định
        fixed_positions.add((target_y, target_x))
    
    # Giải số cuối cùng của cột đầu
    target_num = (size-1) * size + 1
    target_y, target_x = size-1, 0
    
    # Chiến lược đặc biệt để đặt số cuối cùng của cột
    current_y, current_x = find_pos(board, target_num)
    zero_y, zero_x = find_pos(board, 0)
    
    # Nếu số chưa ở đúng vị trí
    if current_y != target_y or current_x != target_x:
        # Đưa số về vị trí (size-1, 1) (bên phải vị trí đích)
        solution_moves = solve_specific_position(board, target_num, size-1, 1, fixed_positions)
        
        # Áp dụng các nước đi
        for move in solution_moves:
            board = apply_move(board, move)
            moves.append(move)
        
        # Đưa ô trống đến góc dưới trái
        zero_y, zero_x = find_pos(board, 0)
        if zero_y != size-1 or zero_x != 0:
            solution_moves = solve_specific_position(board, 0, size-1, 0, fixed_positions - {(size-1, 1)})
            
            for move in solution_moves:
                board = apply_move(board, move)
                moves.append(move)
        
        # Thực hiện chuỗi di chuyển DR-UL để đặt số vào vị trí
        moves.extend(['R', 'U', 'L', 'D'])
        board = apply_move(apply_move(apply_move(apply_move(board, 'R'), 'U'), 'L'), 'D')
    
    # Cập nhật danh sách các vị trí đã cố định
    for y in range(size):
        fixed_positions.add((y, 0))
    
    return moves

def solve_2x2(board):
    """Giải khối 2x2 cuối cùng bằng cách xoay vòng"""
    # Góc dưới phải luôn là ô trống (0)
    size = len(board)
    target_y, target_x = size-1, size-1
    zero_y, zero_x = find_pos(board, 0)
    
    moves = []
    
    # Nếu ô trống chưa ở góc dưới phải, di chuyển nó về đó
    if zero_y != target_y or zero_x != target_x:
        # Tìm đường đi để đưa ô trống về góc dưới phải
        fixed_positions = set()
        for y in range(size):
            for x in range(size):
                if y < size-2 or x < size-2:
                    fixed_positions.add((y, x))
        
        solution_moves = solve_specific_position(board, 0, target_y, target_x, fixed_positions)
        
        # Áp dụng các nước đi
        for move in solution_moves:
            board = apply_move(board, move)
            moves.append(move)
    
    # Kiểm tra xem 2x2 đã giải chưa
    expected_values = [
        (size-2) * size + (size-1),
        (size-2) * size + size,
        (size-1) * size + (size-1),
        0
    ]
    
    current_values = [
        board[size-2][size-2], board[size-2][size-1],
        board[size-1][size-2], board[size-1][size-1]
    ]
    
    # Nếu đã giải, không cần làm gì thêm
    if current_values == expected_values:
        return moves
    
    # Nếu chưa giải, thực hiện xoay vòng (cycle) để giải 2x2
    # Chu kỳ: LURD
    cycle_moves = ['L', 'U', 'R', 'D']
    
    # Thực hiện xoay vòng tối đa 3 lần
    for _ in range(3):
        for move in cycle_moves:
            board = apply_move(board, move)
            moves.append(move)
        
        # Kiểm tra lại sau mỗi vòng xoay
        current_values = [
            board[size-2][size-2], board[size-2][size-1],
            board[size-1][size-2], board[size-1][size-1]
        ]
        
        if current_values == expected_values:
            return moves
    
    return moves