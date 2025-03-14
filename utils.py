import copy

def find_position(board, value):
    for i in range(4):
        for j in range(4):
            if board[i][j] == value:
                return (i, j)
    return None

def move_tile(board, zero_pos, tile_pos):
    new_board = copy.deepcopy(board)
    zx, zy = zero_pos
    tx, ty = tile_pos
    new_board[zx][zy], new_board[tx][ty] = new_board[tx][ty], new_board[zx][zy]
    return new_board

def move_sequence(board, target_pos, zero_pos):
    """ Dịch chuyển ô trống đến vị trí cần thiết trước khi di chuyển một ô khác """
    path = []
    zx, zy = zero_pos
    tx, ty = target_pos
    
    while zx != tx or zy != ty:
        if zx < tx:
            zx += 1
            path.append("↑")  # Ô trống di chuyển xuống -> số di chuyển lên
        elif zx > tx:
            zx -= 1
            path.append("↓")  # Ô trống di chuyển lên -> số di chuyển xuống
        elif zy < ty:
            zy += 1
            path.append("←")  # Ô trống di chuyển phải -> số di chuyển trái
        elif zy > ty:
            zy -= 1
            path.append("→")  # Ô trống di chuyển trái -> số di chuyển phải
    return path