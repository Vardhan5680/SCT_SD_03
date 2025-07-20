import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.geometry("460x520")
        self.master.resizable(False, False)

        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.canvas = tk.Canvas(self.master, width=460, height=460, bg='white')
        self.canvas.place(x=0, y=0)
        self.draw_grid()

        self.create_entries()

        self.solve_button = tk.Button(
            self.master, text="Solve", font=("Arial", 14),
            bg="green", fg="white", command=self.start_solving
        )
        self.solve_button.place(x=155, y=470, width=150, height=40)

    def draw_grid(self):
        cell_size = 50
        offset = 5

        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            # Vertical
            self.canvas.create_line(i * cell_size + offset, offset,
                                    i * cell_size + offset, 455, width=width)
            # Horizontal
            self.canvas.create_line(offset, i * cell_size + offset,
                                    455, i * cell_size + offset, width=width)

    def create_entries(self):
        offset = 5
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.master, font=('Arial', 18), justify='center')
                entry.place(x=j * 50 + offset + 2, y=i * 50 + offset + 2, width=45, height=45)
                self.entries[i][j] = entry

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get().strip()
                if val.isdigit():
                    n = int(val)
                    row.append(n if 1 <= n <= 9 else 0)
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def update_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(grid[i][j]))

    def start_solving(self):
        grid = self.get_grid()
        if not self.is_valid_start(grid):
            messagebox.showerror("Invalid Input", "The puzzle has conflicts in its initial state.")
            return
        if self.solve(grid):
            self.update_grid(grid)
            messagebox.showinfo("Solved", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("No Solution", "This Sudoku puzzle cannot be solved.")

    def is_valid_start(self, grid):
        for i in range(9):
            for j in range(9):
                num = grid[i][j]
                if num != 0:
                    grid[i][j] = 0  # Temporarily remove to test validity
                    if not self.is_valid(grid, num, (i, j)):
                        return False
                    grid[i][j] = num
        return True

    def solve(self, grid):
        empty = self.find_empty(grid)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(grid, num, (row, col)):
                grid[row][col] = num
                if self.solve(grid):
                    return True
                grid[row][col] = 0
        return False

    def is_valid(self, grid, num, pos):
        row, col = pos

        if any(grid[row][i] == num for i in range(9) if i != col):
            return False
        if any(grid[i][col] == num for i in range(9) if i != row):
            return False

        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
