import copy
import tkinter as tk
import time

TILE_SIZE = 100  # Kích thước mỗi ô
GRID_SIZE = 4  # Kích thước bảng

def get_scram_string(board):
    output = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            output.append(str(board[i][j]))
        output.append("/")

    return " ".join(output)

class PuzzleSolverGUI:
    def __init__(self, root, initial_board, algorithms, all_solutions, all_times):
        """
        root: Tkinter root window
        initial_board: Trạng thái ban đầu của 15 puzzle
        algorithms: Danh sách tên thuật toán được sử dụng
        """
        self.root = root
        self.root.title("15 Puzzle Solver")

        # Label hiển thị scramble
        scramble = get_scram_string(initial_board)
        self.scramble_label = tk.Label(root, text=f"Scramble: {scramble}", font=("Arial", 12))
        self.scramble_label.pack(anchor="w", padx=10, pady=5)

        # Frame chính để chứa các ô puzzle
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=10)

        # Số lượng thuật toán
        self.num_algorithms = len(algorithms)

        # Danh sách chứa khung của các puzzle
        self.puzzle_frames = []
        self.puzzles = []
        self.algorithms = algorithms
        self.all_solutions = all_solutions
        self.all_times = all_times

        # Tạo khung hiển thị puzzle theo số thuật toán
        for i in range(self.num_algorithms):
            frame = tk.Frame(self.main_frame, width=200, height=200, highlightbackground="black", highlightthickness=2)
            frame.grid(row=0, column=i, padx=20)
            self.puzzle_frames.append(frame)

            # Tạo một đối tượng PuzzleGUI cho mỗi thuật toán
            new_board = copy.deepcopy(initial_board)
            puzzle = PuzzleGUI(frame, new_board)
            self.puzzles.append(puzzle)

            label1 = tk.Label(self.main_frame, text=algorithms[i], font=("Arial", 10, "bold"))
            label1.grid(row=1, column=i, pady=5)

            label2 = tk.Label(self.main_frame, text=f"Solution found in {self.all_times[i]:.5f} ms\nMove count: {len(self.all_solutions[i])}", font=("Arial", 10))
            label2.grid(row=2, column=i, pady=5)

    def update_puzzle(self, all_solutions):
        """
        Cập nhật tất cả puzzles theo danh sách các bước giải.
        all_solutions: List chứa danh sách bước giải của từng thuật toán
        """
        all_solved = False
        step_index = 0
        solved_puzzle = 0

        while not all_solved:
            time.sleep(0.1)

            for i, puzzle in enumerate(self.puzzles):
                if i < len(all_solutions):  # Đảm bảo không vượt quá số lượng thuật toán
                    # puzzle.animate_solution(all_solutions[i])
                    if step_index < len(all_solutions[i]):
                        puzzle.animate_move(all_solutions[i][step_index])

                    if step_index == len(all_solutions[i]):
                        solved_puzzle += 1
            
            if solved_puzzle == len(all_solutions):
                all_solved = True

            step_index += 1



class PuzzleGUI:
    def __init__(self, parent, initial_board):
        self.parent = parent
        self.board = initial_board  # Lưu trạng thái 15-puzzle
        self.size = 4  # 15-puzzle là 4x4

        self.canvas = tk.Canvas(parent, width=200, height=200, bg="white")
        self.canvas.pack()

        self.draw_board()

    def draw_board(self):
        """Vẽ trạng thái hiện tại của 15 puzzle lên canvas"""
        self.canvas.delete("all")
        tile_size = 50  # Kích thước mỗi ô vuông
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value != 0:  # Không vẽ ô trống
                    x1, y1 = j * tile_size, i * tile_size
                    x2, y2 = x1 + tile_size, y1 + tile_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
                    self.canvas.create_text(x1 + 25, y1 + 25, text=str(value), font=("Arial", 14, "bold"))

    def move_tile(self, move):
        """Thực hiện một bước di chuyển (L, R, U, D)"""
        zero_pos = [(i, row.index(0)) for i, row in enumerate(self.board) if 0 in row][0]
        i, j = zero_pos
        di, dj = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}[move]

        ni, nj = i + di, j + dj
        if 0 <= ni < self.size and 0 <= nj < self.size:
            self.board[i][j], self.board[ni][nj] = self.board[ni][nj], self.board[i][j]
            self.draw_board()

    def animate_solution(self, moves):
        """Di chuyển theo danh sách các bước moves"""
        for move in moves:
            self.move_tile(move)
            self.parent.update()  # Cập nhật giao diện
            time.sleep(0.1)

    def animate_move(self, move):
        self.move_tile(move)
        self.parent.update()  # Cập nhật giao diện
        # time.sleep(0.1)

###############################

# import copy
# import tkinter as tk
# import time
# import threading

# TILE_SIZE = 50  # Adjusted tile size for better display
# GRID_SIZE = 4

# def get_scram_string(board):
#     """Convert board state into a readable scramble string."""
#     return " / ".join(" ".join(map(str, row)) for row in board)

# class PuzzleSolverGUI:
#     def __init__(self, root, initial_board, algorithms, all_solutions, all_times):
#         self.root = root
#         self.root.title("15 Puzzle Solver")

#         # Display scramble state
#         self.scramble_label = tk.Label(root, text=f"Scramble: {get_scram_string(initial_board)}", font=("Arial", 12))
#         self.scramble_label.pack(anchor="w", padx=10, pady=5)

#         self.log_label = tk.Label(root, text="Starting BFS...", font=("Arial", 10))
#         self.log_label.pack(anchor="w", padx=10, pady=5)

#         # Create frame for puzzle display
#         self.main_frame = tk.Frame(root)
#         self.main_frame.pack(pady=10)

#         self.puzzle = PuzzleGUI(self.main_frame, copy.deepcopy(initial_board))
#         self.puzzle.canvas.pack()

#         self.root.after(100, self.start_bfs, initial_board, all_solutions)

#     def start_bfs(self, board, all_solutions):
#         """Start BFS in a separate thread."""
#         threading.Thread(target=self.run_bfs, args=(board, all_solutions), daemon=True).start()

#     def run_bfs(self, board, all_solutions):
#         """Execute BFS and update GUI dynamically."""
#         for move in all_solutions[0]:  # Assuming only BFS solution for now
#             time.sleep(0.1)  # Add delay for animation
#             self.puzzle.animate_move(move)
#         self.update_log("✅ BFS Finished!")

#     def update_log(self, message):
#         self.log_label.config(text=message)
#         self.root.update()

# class PuzzleGUI:
#     def __init__(self, parent, initial_board):
#         self.parent = parent
#         self.board = initial_board
#         self.size = 4
#         self.canvas = tk.Canvas(parent, width=200, height=200, bg="white")
#         self.canvas.pack()
#         self.draw_board()

#     def draw_board(self):
#         """Draws the puzzle board."""
#         self.canvas.delete("all")
#         for i in range(self.size):
#             for j in range(self.size):
#                 value = self.board[i][j]
#                 if value != 0:
#                     x1, y1 = j * TILE_SIZE, i * TILE_SIZE
#                     x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
#                     self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
#                     self.canvas.create_text(x1 + TILE_SIZE // 2, y1 + TILE_SIZE // 2, text=str(value), font=("Arial", 14, "bold"))

#     def move_tile(self, move):
#         """Move a tile based on the given direction."""
#         zero_pos = [(i, row.index(0)) for i, row in enumerate(self.board) if 0 in row][0]
#         i, j = zero_pos
#         di, dj = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}[move]
#         ni, nj = i + di, j + dj
#         if 0 <= ni < self.size and 0 <= nj < self.size:
#             self.board[i][j], self.board[ni][nj] = self.board[ni][nj], self.board[i][j]
#             self.draw_board()

#     def animate_move(self, move):
#         """Animate a single move."""
#         self.move_tile(move)
#         self.parent.update()
