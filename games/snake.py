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
        
        # Initialize game state
        self.snake = [(5, 5)]
        self.direction = 'Right'
        self.food = None
        self.score = 0
        self.game_over_flag = False
        
        # Bind keys
        self.master.bind('<Left>', lambda e: self.change_direction('Left'))
        self.master.bind('<Right>', lambda e: self.change_direction('Right'))
        self.master.bind('<Up>', lambda e: self.change_direction('Up'))
        self.master.bind('<Down>', lambda e: self.change_direction('Down'))

    def play(self):
        # Create canvas
        self.canvas = tk.Canvas(self.frame, width=self.canvas_size, 
                              height=self.canvas_size, bg='black')
        self.canvas.pack(padx=10, pady=10)
        
        # Create score label
        self.score_label = tk.Label(self.frame, text=f"Score: {self.score}",
                                  font=('Helvetica', 16))
        self.score_label.pack()
        
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
        
        # Draw snake
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill='green', outline='darkgreen'
            )
        
        # Draw food
        if self.food:
            x, y = self.food
            self.canvas.create_oval(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill='red'
            )

    def game_over(self):
        self.game_over_flag = True
        self.canvas.create_text(
            self.canvas_size//2, self.canvas_size//2,
            text=f"Game Over!\nScore: {self.score}",
            fill='white', font=('Helvetica', 24),
            justify=tk.CENTER
        )

    def is_game_over(self):
        return self.game_over_flag
