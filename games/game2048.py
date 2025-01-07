from .base_game import BaseGame
import tkinter as tk
from tkinter import ttk
import random

class Game2048(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("2048")
        
        # Make cell size responsive to screen size
        screen_width = self.master.winfo_screenwidth()
        self.cell_size = min(100, screen_width // 16)  # Adjust cell size based on screen
        self.padding = self.cell_size // 10
        self.grid_size = 4

        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2f',            # Dark background
            'grid_bg': '#2a2a40',       # Grid background
            'text': '#ffffff',           # White text
            0: '#2a2a40',               # Empty cell
            2: '#50FA7B',               # Light green
            4: '#43B466',               # Darker green
            8: '#FF5555',               # Red
            16: '#FF6E6E',              # Lighter red
            32: '#BD93F9',              # Purple
            64: '#A571F4',              # Darker purple
            128: '#FFB86C',             # Orange
            256: '#FFA54D',             # Darker orange
            512: '#8BE9FD',             # Cyan
            1024: '#59C2E6',            # Darker cyan
            2048: '#F1FA8C'             # Yellow
        }

        # Set minimum window size
        min_window_width = self.cell_size * self.grid_size + self.padding * (self.grid_size + 1) + 40
        min_window_height = min_window_width + 150
        self.master.minsize(min_window_width, min_window_height)

        # Adjust window size
        window_width = max(min_window_width, screen_width // 4)
        window_height = window_width + 150  # Extra space for score and buttons
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.configure(bg=self.colors['bg'])

        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over_flag = False

        # Bind arrow keys
        self.master.bind('<Left>', lambda e: self.move('left'))
        self.master.bind('<Right>', lambda e: self.move('right'))
        self.master.bind('<Up>', lambda e: self.move('up'))
        self.master.bind('<Down>', lambda e: self.move('down'))

    def play(self):
        self.frame.configure(bg=self.colors['bg'])

        # Score label with responsive font size
        score_font_size = min(24, self.cell_size // 3)
        self.score_label = tk.Label(
            self.frame,
            text=f"Score: {self.score}",
            font=('Helvetica', score_font_size, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.score_label.pack(pady=self.padding * 2)

        # Modern canvas
        self.canvas = tk.Canvas(
            self.frame,
            width=self.cell_size * self.grid_size + self.padding * (self.grid_size + 1),
            height=self.cell_size * self.grid_size + self.padding * (self.grid_size + 1),
            bg=self.colors['grid_bg'],
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Responsive button size
        button_font_size = min(12, self.cell_size // 6)
        button_padding_x = self.cell_size // 4
        button_padding_y = self.cell_size // 8
        self.restart_button = tk.Button(
            self.frame,
            text="Restart Game",
            font=('Helvetica', button_font_size, 'bold'),
            bg=self.colors['grid_bg'],
            fg=self.colors['text'],
            activebackground='#3a3a5c',
            activeforeground=self.colors['text'],
            relief='flat',
            borderwidth=0,
            padx=button_padding_x,
            pady=button_padding_y,
            cursor='hand2',
            command=self.restart_game
        )
        self.restart_button.pack(pady=self.padding * 2)

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
        
        # Draw background grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size + (j + 1) * self.padding
                y1 = i * self.cell_size + (i + 1) * self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Draw empty cell background
                self.rounded_rect(x1, y1, x2, y2, 10, self.colors['grid_bg'])

        # Draw tiles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size + (j + 1) * self.padding
                y1 = i * self.cell_size + (i + 1) * self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                value = self.grid[i][j]
                if value != 0:  # Only draw non-empty cells
                    color = self.colors.get(value, self.colors[2048])
                    
                    # Create tile with rounded corners
                    self.rounded_rect(x1, y1, x2, y2, 10, color)
                    
                    # Adjust font sizes in tiles based on cell size
                    font_size = min(
                        36,
                        self.cell_size // 2 if value < 100 
                        else self.cell_size // 2.5 if value < 1000 
                        else self.cell_size // 3
                    )
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(value),
                        font=('Helvetica', font_size, 'bold'),
                        fill=self.colors['text']
                    )

    def rounded_rect(self, x1, y1, x2, y2, radius, color):
        # Draw rounded rectangle
        self.canvas.create_rectangle(
            x1 + radius, y1,
            x2 - radius, y2,
            fill=color,
            outline=""
        )
        self.canvas.create_rectangle(
            x1, y1 + radius,
            x2, y2 - radius,
            fill=color,
            outline=""
        )
        
        # Draw corners
        self.canvas.create_oval(
            x1, y1,
            x1 + 2*radius, y1 + 2*radius,
            fill=color,
            outline=""
        )
        self.canvas.create_oval(
            x2 - 2*radius, y1,
            x2, y1 + 2*radius,
            fill=color,
            outline=""
        )
        self.canvas.create_oval(
            x1, y2 - 2*radius,
            x1 + 2*radius, y2,
            fill=color,
            outline=""
        )
        self.canvas.create_oval(
            x2 - 2*radius, y2 - 2*radius,
            x2, y2,
            fill=color,
            outline=""
        )

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
        
        # Semi-transparent overlay
        self.canvas.create_rectangle(
            0, 0,
            self.canvas.winfo_width(),
            self.canvas.winfo_height(),
            fill='black',
            stipple='gray50'
        )
        
        # Game over text with shadow
        self.canvas.create_text(
            self.canvas.winfo_width() / 2 + 2,
            self.canvas.winfo_height() / 2 - 18,
            text=f"Game Over!\nScore: {self.score}",
            font=('Helvetica', 24, 'bold'),
            fill='black',
            justify=tk.CENTER
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2 - 20,
            text=f"Game Over!\nScore: {self.score}",
            font=('Helvetica', 24, 'bold'),
            fill=self.colors['text'],
            justify=tk.CENTER
        )

    def restart_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over_flag = False
        self.add_new_tile()
        self.add_new_tile()
        self.display()
