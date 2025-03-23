from layer_by_layer import solve_layer_by_layer
import os
import platform
import time
import copy
import tkinter as tk

from plot_board import  PuzzleSolverGUI
from scramble import scramble

def cancel_moves(moves):
    opposite = {"L": "R", "R": "L", "U": "D", "D": "U"}
    stack = []

    for move in moves:
        if stack and stack[-1] == opposite.get(move):
            stack.pop()
        else:
            stack.append(move)

    return stack

def compress_solution(moves):

    if len(moves) == 0:
        return ""

    compressed = []
    count = 1

    for i in range(1, len(moves)):
        if moves[i] == moves[i - 1]:
            count += 1
        else:
            compressed.append(moves[i - 1] + (str(count) if count > 1 else ""))
            count = 1

    compressed.append(moves[-1] + (str(count) if count > 1 else ""))  # Xử lý ký tự cuối cùng
    return " ".join(compressed)

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def find_pos(board, target):
    for i in range(4):
        for j in range(4):
            if board[i][j] == target:
                return i, j

def do_move(board, move): # R = 0 to right, L = 0 to left, U = 0 to up, D = 0 to down
    dy, dx = 0, 0
    if move == "R":
        dx = 1
        dy = 0
    elif move == "L":
        dx = -1
        dy = 0
    elif move == "U":
        dx = 0
        dy = -1
    elif move == "D":
        dx = 0
        dy = 1

    zero_y, zero_x = find_pos(board, 0)
    temp = board[zero_y][zero_x]
    board[zero_y][zero_x] = board[zero_y + dy][zero_x + dx]
    board[zero_y + dy][zero_x + dx] = temp

# Trạng thái đã hoàn thành
GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


if __name__ == "__main__":
    initial_board = [
        [11,8,13,3],
        [12,1,7,5],
        [0,6,15,4],
        [9,10,2,14]
    ]

    initial_board = scramble()
    algorithm_names = ["Layer by Layer", "IDA*", "A*"]
    all_solutions = []
    all_times = []

    # for y in range(4):
    #     for x in range(4):
    #         if initial_board[y][x] == 0:
    #             print("\t", end="")
    #         else:
    #             print(initial_board[y][x], "\t", end="")
    #     print("\n")

    running_board = copy.deepcopy(initial_board)

    start_time = time.perf_counter()

    lbl_steps = solve_layer_by_layer(initial_board, GOAL_STATE)

    lbl_steps = cancel_moves(lbl_steps)

    end_time = time.perf_counter()

    all_times.append((end_time - start_time) * 1000)

    ida_steps = ["R", "R", "D"]
    astar_steps = ["R", "R", "D", "L"]

    all_solutions.append(lbl_steps)
    all_solutions.append(ida_steps)
    all_solutions.append(astar_steps)

    all_times.append(0)
    all_times.append(100)


    # Tạo cửa sổ Tkinter
    root = tk.Tk()
    root.title("15 Puzzle Solver")
    app = PuzzleSolverGUI(root, running_board, algorithm_names, all_solutions, all_times)
    root.after(2000, lambda: app.update_puzzle(all_solutions))
    root.mainloop()



    # clear_terminal()
    # print("Solution:", compress_solution(steps))
    # print("Solution found in", (end_time - start_time) * 1000, "ms")
    # for y in range(4):
    #     for x in range(4):
    #         if running_board[y][x] == 0:
    #             print("\t", end="")
    #         else:
    #             print(running_board[y][x], "\t", end="")
    #     print("\n")
    # print("move count: 0")

    # for i, move in enumerate(steps):
    #     clear_terminal()
    #     print("Solution:", compress_solution(steps))
    #     print("Solution found in", (end_time - start_time) * 1000, "ms")
    #     do_move(running_board, move)
    #     for y in range(4):
    #         for x in range(4):
    #             if running_board[y][x] == 0:
    #                 print("\t", end="")
    #             else:
    #                 print(running_board[y][x], "\t", end="")
    #         print("\n")
    #     print("Move count:", i + 1)
    #     time.sleep(0.08)