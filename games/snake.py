from .base_game import BaseGame
import tkinter as tk
import random

class Snake(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Snake")
        self.canvas_size = 400
        self.cell_size = 20
        self.speed = 100
        
        # Modern color scheme
        self.colors = {
            'bg': '#1E1E2E',
            'snake_head': '#50FA7B',
            'snake_body': '#43B466',
            'food': '#FF5555',
            'grid': '#2A2A3C',
            'text': '#F8F8F2'
        }
        
        # Center the window and set theme
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.canvas_size + 40
        window_height = self.canvas_size + 150  # Increased from 100 to 150 for better button visibility
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.master.minsize(window_width, window_height)  # Add minimum size constraint
        self.master.configure(bg=self.colors['bg'])
        
        # Update frame background to match theme
        self.frame.configure(bg=self.colors['bg'])
        
        # Initialize game state
        self.snake = [(5, 5)]
        self.direction = 'Right'
        self.food = None
        self.score = 0
        self.game_over_flag = False
        self.restart_button = None
        
        # Bind keys
        self.master.bind('<Left>', lambda e: self.change_direction('Left'))
        self.master.bind('<Right>', lambda e: self.change_direction('Right'))
        self.master.bind('<Up>', lambda e: self.change_direction('Up'))
        self.master.bind('<Down>', lambda e: self.change_direction('Down'))

    def play(self):
        # Create canvas with modern background
        self.canvas = tk.Canvas(
            self.frame, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)
        
        # Modern score label with themed background
        self.score_label = tk.Label(
            self.frame,
            text=f"Score: {self.score}",
            font=('Helvetica', 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.score_label.pack()
        
        # Draw grid lines
        for i in range(0, self.canvas_size, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_size,
                fill=self.colors['grid'], width=1
            )
            self.canvas.create_line(
                0, i, self.canvas_size, i,
                fill=self.colors['grid'], width=1
            )
        
        self.spawn_food()
        self.update()

    def change_direction(self, new_direction):
        opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if opposites[new_direction] != self.direction:
            self.direction = new_direction

    def spawn_food(self):
        while True:
            x = random.randint(0, (self.canvas_size//self.cell_size)-1)
            y = random.randint(0, (self.canvas_size//self.cell_size)-1)
            self.food = (x, y)
            if self.food not in self.snake:
                break

    def update(self):
        if not self.game_over_flag:
            # Move snake
            head = self.snake[0]
            if self.direction == 'Left':
                new_head = (head[0]-1, head[1])
            elif self.direction == 'Right':
                new_head = (head[0]+1, head[1])
            elif self.direction == 'Up':
                new_head = (head[0], head[1]-1)
            else:  # Down
                new_head = (head[0], head[1]+1)
            
            # Check collision with walls
            if (new_head[0] < 0 or new_head[0] >= self.canvas_size//self.cell_size or
                new_head[1] < 0 or new_head[1] >= self.canvas_size//self.cell_size or
                new_head in self.snake):
                self.game_over()
                return
            
            self.snake.insert(0, new_head)
            
            # Check food collision
            if new_head == self.food:
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                self.spawn_food()
            else:
                self.snake.pop()
            
            self.display()
            self.master.after(self.speed, self.update)

    def display(self):
        self.canvas.delete('all')
        
        # Draw grid
        for i in range(0, self.canvas_size, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_size,
                fill=self.colors['grid'], width=1
            )
            self.canvas.create_line(
                0, i, self.canvas_size, i,
                fill=self.colors['grid'], width=1
            )
        
        # Draw snake with rounded corners
        for i, segment in enumerate(self.snake):
            x, y = segment
            color = self.colors['snake_head'] if i == 0 else self.colors['snake_body']
            
            # Create rounded rectangle
            x1 = x * self.cell_size + 2
            y1 = y * self.cell_size + 2
            x2 = (x + 1) * self.cell_size - 2
            y2 = (y + 1) * self.cell_size - 2
            
            self.canvas.create_oval(
                x1, y1, x2, y2,
                fill=color, outline=''
            )
        
        # Draw modern food
        if self.food:
            x, y = self.food
            x1 = x * self.cell_size + 2
            y1 = y * self.cell_size + 2
            x2 = (x + 1) * self.cell_size - 2
            y2 = (y + 1) * self.cell_size - 2
            
            # Create star-like shape for food
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            size = self.cell_size * 0.4
            
            self.canvas.create_oval(
                center_x - size, center_y - size,
                center_x + size, center_y + size,
                fill=self.colors['food'],
                outline='white',
                width=2
            )

    def game_over(self):
        self.game_over_flag = True
        
        # Semi-transparent overlay
        self.canvas.create_rectangle(
            0, 0, self.canvas_size, self.canvas_size,
            fill='black', stipple='gray50'
        )
        
        # Game over text with shadow
        self.canvas.create_text(
            self.canvas_size//2 + 2, self.canvas_size//2 - 18,
            text=f"Game Over!\nScore: {self.score}",
            fill='black', font=('Helvetica', 24, 'bold'),
            justify=tk.CENTER
        )
        self.canvas.create_text(
            self.canvas_size//2, self.canvas_size//2 - 20,
            text=f"Game Over!\nScore: {self.score}",
            fill=self.colors['text'],
            font=('Helvetica', 24, 'bold'),
            justify=tk.CENTER
        )
        
        # Modern restart button with updated colors
        self.restart_button = tk.Button(
            self.frame,
            text="Restart Game",
            font=('Helvetica', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['grid'],  # Using grid color for button
            activebackground=self.colors['snake_head'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.restart
        )
        self.restart_button.pack(pady=10)

    def restart(self):
        # Reset game state
        self.snake = [(5, 5)]
        self.direction = 'Right'
        self.food = None
        self.score = 0
        self.game_over_flag = False
        
        # Update score display
        self.score_label.config(text=f"Score: {self.score}")
        
        # Remove restart button if it exists
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None
            
        # Clear canvas and restart game
        self.canvas.delete('all')
        self.spawn_food()
        self.update()

    def is_game_over(self):
        return self.game_over_flag
