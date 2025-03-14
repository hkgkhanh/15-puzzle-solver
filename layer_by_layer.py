from utils import find_position, move_tile, move_sequence

def solve_layer_by_layer(board, GOAL_STATE):
    # 1. Hoàn thành hàng đầu tiên (4 ô đầu tiên)
    # 2. Hoàn thành hàng thứ hai (4 ô tiếp theo)
    # 3. Sắp xếp cột trái
    # 4. Giải nốt 2x3 cuối cùng bằng cách hoán đổi cục bộ
    
    solution_steps = []
    
    # (1) Hoàn thành hàng đầu tiên
    for target in range(1, 5):
        pos = find_position(board, target)
        goal_pos = find_position(GOAL_STATE, target)
        if pos != goal_pos:
            zero_pos = find_position(board, 0)
            path = move_sequence(board, goal_pos, zero_pos)
            solution_steps.extend(path)
    
    # (2) Hoàn thành hàng thứ hai
    for target in range(5, 9):
        pos = find_position(board, target)
        goal_pos = find_position(GOAL_STATE, target)
        if pos != goal_pos:
            zero_pos = find_position(board, 0)
            path = move_sequence(board, goal_pos, zero_pos)
            solution_steps.extend(path)
    
    # (3) Sắp xếp hai cột trái
    for target in [9, 13, 10, 14]:
        pos = find_position(board, target)
        goal_pos = find_position(GOAL_STATE, target)
        if pos != goal_pos:
            zero_pos = find_position(board, 0)
            path = move_sequence(board, goal_pos, zero_pos)
            solution_steps.extend(path)
    
    # (4) Giải nốt 2x2 cuối cùng bằng phương pháp hoán đổi cục bộ
    zero_pos = find_position(board, 0)
    eleven_pos = find_position(board, 11)
    
    if zero_pos == (2, 2) and eleven_pos == (2, 3):
        solution_steps.extend(["←", "↑"])

    elif zero_pos == (2, 2) and eleven_pos == (3, 2):
        solution_steps.extend(["↑", "←"])

    elif zero_pos == (3, 2) and eleven_pos == (2, 2):
        solution_steps.extend(["←"])

    elif zero_pos == (3, 2) and eleven_pos == (2, 3):
        solution_steps.extend(["↓", "←", "↑"])

    elif zero_pos == (3, 2) and eleven_pos == (3, 3):
        solution_steps.extend(["←", "↓", "→", "↑", "←"])

    elif zero_pos == (2, 3) and eleven_pos == (2, 2):
        solution_steps.extend(["↑"])

    elif zero_pos == (2, 3) and eleven_pos == (3, 2):
        solution_steps.extend(["→", "↑", "←"])

    elif zero_pos == (2, 3) and eleven_pos == (3, 3):
        solution_steps.extend(["↑", "←", "↓", "→", "↑", "←"])

    elif zero_pos == (3, 3) and eleven_pos == (3, 2):
        solution_steps.extend(["↓", "→", "↑", "←"])

    elif zero_pos == (3, 3) and eleven_pos == (2, 3):
        solution_steps.extend(["→", "↓", "←", "↑"])
    
    return solution_steps