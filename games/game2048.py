from .base_game import BaseGame
import tkinter as tk
import random

class Game2048(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("2048")
        self.grid_size = 4
        self.cell_size = 100
        self.padding = 10
        
        # Center the window
        window_width = self.cell_size * self.grid_size + self.padding * (self.grid_size + 1) + 20
        window_height = window_width + 100  # Extra space for score
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over_flag = False
        
        # Colors for different numbers
        self.colors = {
            0: '#cdc1b4',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e'
        }
        
        # Bind arrow keys
        self.master.bind('<Left>', lambda e: self.move('left'))
        self.master.bind('<Right>', lambda e: self.move('right'))
        self.master.bind('<Up>', lambda e: self.move('up'))
        self.master.bind('<Down>', lambda e: self.move('down'))

    def play(self):
        # Create score label
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}",
                                  font=('Helvetica', 16))
        self.score_label.pack(pady=10)
        
        # Create game board
        self.canvas = tk.Canvas(self.frame,
                              width=self.cell_size * self.grid_size + self.padding * (self.grid_size + 1),
                              height=self.cell_size * self.grid_size + self.padding * (self.grid_size + 1),
                              bg='#bbada0')
        self.canvas.pack(padx=10, pady=10)
        
        # Initialize game
        self.add_new_tile()
        self.add_new_tile()
        self.display()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) 
                      for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        if self.game_over_flag:
            return

        original_grid = [row[:] for row in self.grid]
        shifted = False

        if direction in ['left', 'right']:
            for i in range(self.grid_size):
                line = self.grid[i][:]
                if direction == 'right':
                    line.reverse()
                new_line = self.merge_line(line)
                if direction == 'right':
                    new_line.reverse()
                if line != new_line:
                    shifted = True
                self.grid[i] = new_line

        else:  # up or down
            for j in range(self.grid_size):
                line = [self.grid[i][j] for i in range(self.grid_size)]
                if direction == 'down':
                    line.reverse()
                new_line = self.merge_line(line)
                if direction == 'down':
                    new_line.reverse()
                if line != new_line:
                    shifted = True
                for i in range(self.grid_size):
                    self.grid[i][j] = new_line[i]

        if shifted:
            self.add_new_tile()
            self.display()
            if self.is_game_over():
                self.game_over()

    def merge_line(self, line):
        # Remove zeros
        new_line = [x for x in line if x != 0]
        # Merge identical pairs
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1]:
                new_line[i] *= 2
                self.score += new_line[i]
                new_line.pop(i + 1)
                new_line.append(0)
        # Add zeros to maintain size
        while len(new_line) < self.grid_size:
            new_line.append(0)
        return new_line

    def display(self):
        self.canvas.delete('all')
        self.score_label.config(text=f"Score: {self.score}")
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size + (j + 1) * self.padding
                y1 = i * self.cell_size + (i + 1) * self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                value = self.grid[i][j]
                color = self.colors.get(value, '#ff0000')
                
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                          fill=color, width=0)
                if value != 0:
                    font_size = 36 if value < 100 else 32 if value < 1000 else 24
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                          text=str(value),
                                          font=('Helvetica', font_size, 'bold'),
                                          fill='#776e65' if value <= 4 else 'white')

    def is_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        
        # Check for possible merges
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True

    def game_over(self):
        self.game_over_flag = True
        self.canvas.create_rectangle(0, 0,
                                   self.canvas.winfo_width(),
                                   self.canvas.winfo_height(),
                                   fill='rgba(238,228,218,0.73)')
        self.canvas.create_text(self.canvas.winfo_width() / 2,
                              self.canvas.winfo_height() / 2,
                              text=f"Game Over!\nScore: {self.score}",
                              font=('Helvetica', 24, 'bold'),
                              fill='#776e65',
                              justify=tk.CENTER)
