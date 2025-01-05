from .base_game import BaseGame
import tkinter as tk
import random

class Tetris(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Tetris")
        self.cell_size = 30
        self.cols = 10
        self.rows = 20
        self.game_over_flag = False
        self.score = 0
        self.speed = 500
        
        # Define tetromino shapes and colors
        self.shapes = {
            'I': [(0,0), (0,1), (0,2), (0,3)],
            'O': [(0,0), (0,1), (1,0), (1,1)],
            'T': [(0,1), (1,0), (1,1), (1,2)],
            'S': [(0,1), (0,2), (1,0), (1,1)],
            'Z': [(0,0), (0,1), (1,1), (1,2)],
            'J': [(0,0), (1,0), (1,1), (1,2)],
            'L': [(0,2), (1,0), (1,1), (1,2)]
        }
        self.colors = {
            'I': 'cyan',
            'O': 'yellow',
            'T': 'purple',
            'S': 'green',
            'Z': 'red',
            'J': 'blue',
            'L': 'orange'
        }
        
        # Initialize game state
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = None
        self.current_pos = None
        self.current_shape = None
        
        # Bind keys
        self.master.bind('<Left>', lambda e: self.move(-1, 0))
        self.master.bind('<Right>', lambda e: self.move(1, 0))
        self.master.bind('<Down>', lambda e: self.move(0, 1))
        self.master.bind('<Up>', lambda e: self.rotate())
        self.master.bind('<space>', lambda e: self.drop())

    def play(self):
        # Create instructions label
        instructions = (
            "Controls:\n"
            "← → : Move left/right\n"
            "↑ : Rotate\n"
            "↓ : Move down\n"
            "Space : Drop piece"
        )
        self.instructions_label = tk.Label(self.frame, text=instructions,
                                         font=('Helvetica', 12), justify=tk.LEFT)
        self.instructions_label.pack(pady=5)
        
        # Create score label
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}",
                                  font=('Helvetica', 16))
        self.score_label.pack(pady=10)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.frame,
            width=self.cell_size * self.cols,
            height=self.cell_size * self.rows,
            bg='black'
        )
        self.canvas.pack(padx=10, pady=10)
        
        self.spawn_piece()
        self.update()

    def spawn_piece(self):
        self.current_shape = random.choice(list(self.shapes.keys()))
        shape = self.shapes[self.current_shape]
        self.current_piece = [(x, y) for x, y in shape]
        self.current_pos = [0, self.cols//2 - 2]
        
        if not self.is_valid_move(0, 0):
            self.game_over()
            return False
        return True

    def move(self, dx, dy):
        if not self.game_over_flag and self.is_valid_move(dy, dx):
            self.current_pos[0] += dy
            self.current_pos[1] += dx
            self.display()
            return True
        return False

    def rotate(self):
        if self.game_over_flag:
            return
        
        old_piece = self.current_piece.copy()
        # Get center of rotation
        cx = sum(x for x, _ in self.current_piece) // len(self.current_piece)
        cy = sum(y for _, y in self.current_piece) // len(self.current_piece)
        
        # Rotate around center
        self.current_piece = [(-y + cx, x - cy) for x, y in self.current_piece]
        
        if not self.is_valid_move(0, 0):
            self.current_piece = old_piece
        else:
            self.display()

    def drop(self):
        while self.move(0, 1):
            pass

    def is_valid_move(self, dy, dx):
        for x, y in self.current_piece:
            new_y = self.current_pos[0] + x + dy
            new_x = self.current_pos[1] + y + dx
            
            if not (0 <= new_x < self.cols and new_y < self.rows):
                return False
            if new_y >= 0 and self.board[new_y][new_x]:
                return False
        return True

    def update(self):
        if not self.game_over_flag:
            if not self.move(0, 1):
                self.freeze_piece()
                self.clear_lines()
                if not self.spawn_piece():
                    return
            self.master.after(self.speed, self.update)

    def freeze_piece(self):
        for x, y in self.current_piece:
            if self.current_pos[0] + x >= 0:
                self.board[self.current_pos[0] + x][self.current_pos[1] + y] = self.current_shape

    def clear_lines(self):
        lines_cleared = 0
        y = self.rows - 1
        while y >= 0:
            if all(self.board[y]):
                lines_cleared += 1
                for ny in range(y, 0, -1):
                    self.board[ny] = self.board[ny-1][:]
                self.board[0] = [None] * self.cols
            else:
                y -= 1
        
        if lines_cleared:
            self.score += (100 * lines_cleared * lines_cleared)
            self.score_label.config(text=f"Score: {self.score}")

    def display(self):
        self.canvas.delete('all')
        
        # Draw fallen pieces
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.colors[self.board[y][x]])
        
        # Draw current piece
        if self.current_piece and not self.game_over_flag:
            for x, y in self.current_piece:
                if self.current_pos[0] + x >= 0:
                    self.draw_cell(
                        self.current_pos[1] + y,
                        self.current_pos[0] + x,
                        self.colors[self.current_shape]
                    )

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * self.cell_size,
            y * self.cell_size,
            (x + 1) * self.cell_size,
            (y + 1) * self.cell_size,
            fill=color,
            outline='gray'
        )

    def game_over(self):
        self.game_over_flag = True
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text=f"Game Over!\nScore: {self.score}",
            fill='white',
            font=('Helvetica', 24),
            justify=tk.CENTER
        )
        
        # Add restart button
        self.restart_button = tk.Button(
            self.frame,
            text="Restart Game",
            font=('Helvetica', 12),
            command=self.restart
        )
        self.restart_button.pack(pady=10)

    def restart(self):
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.score = 0
        self.game_over_flag = False
        self.score_label.config(text=f"Score: {self.score}")
        
        if hasattr(self, 'restart_button'):
            self.restart_button.destroy()
        
        if hasattr(self, 'instructions_label'):
            self.instructions_label.destroy()
        
        self.spawn_piece()
        self.display()
        self.update()

    def is_game_over(self):
        return self.game_over_flag
