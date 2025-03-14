from layer_by_layer import solve_layer_by_layer
from plot_board import animate_solution

# Hàm kiểm tra trạng thái đã hoàn thành
GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


if __name__ == "__main__":
    initial_board = [
        [2, 12, 8, 11],
        [3, 6, 10, 4],
        [7, 15, 5, 9],
        [13, 14, 0, 1]
    ]

    steps = solve_layer_by_layer(initial_board, GOAL_STATE)
    print("Solution:", " ".join(steps))
    animate_solution(initial_board, steps)
