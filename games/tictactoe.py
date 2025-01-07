from .base_game import BaseGame
import tkinter as tk
from tkinter import ttk

class TicTacToe(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Tic Tac Toe")
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2f',
            'button': '#2a2a40',
            'button_hover': '#3a3a5c',
            'x_color': '#00bcd4',
            'o_color': '#ff4081',
            'text': '#ffffff',
            'win': '#4caf50',
            'tie': '#ffd700'
        }
        
        self.master.configure(bg=self.colors['bg'])
        # Center window
        window_width = 400
        window_height = 500
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        self.initialize_game()

    def initialize_game(self):
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_active = True

    def play(self):
        self.frame.pack_forget()
        self.frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.frame.pack(expand=True, padx=20, pady=20)

        # Status label with modern font and colors
        self.status = tk.Label(self.frame, 
                             text=f"Player {self.current_player}'s turn",
                             font=('Helvetica Neue', 16, 'bold'),
                             bg=self.colors['bg'],
                             fg=self.colors['text'])
        self.status.pack(pady=20)

        # Game board
        board_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text='',
                                             font=('Helvetica Neue', 28, 'bold'),
                                             width=3, height=1,
                                             bg=self.colors['button'],
                                             fg=self.colors['text'],
                                             activebackground=self.colors['button_hover'],
                                             activeforeground=self.colors['text'],
                                             relief='flat',
                                             borderwidth=0,
                                             command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=4, pady=4)
                
                # Bind hover events
                self.buttons[i][j].bind('<Enter>', 
                    lambda e, btn=self.buttons[i][j]: btn.configure(bg=self.colors['button_hover']))
                self.buttons[i][j].bind('<Leave>', 
                    lambda e, btn=self.buttons[i][j]: btn.configure(bg=self.colors['button']))

        # Modern restart button
        self.restart_button = tk.Button(self.frame, 
                                      text="Restart Game",
                                      font=('Helvetica Neue', 12, 'bold'),
                                      bg=self.colors['button'],
                                      fg=self.colors['text'],
                                      activebackground=self.colors['button_hover'],
                                      activeforeground=self.colors['text'],
                                      relief='flat',
                                      borderwidth=0,
                                      padx=20,
                                      pady=10,
                                      command=self.restart_game)
        self.restart_button.pack(pady=30)
        
        # Bind hover events for restart button
        self.restart_button.bind('<Enter>', 
            lambda e: self.restart_button.configure(bg=self.colors['button_hover']))
        self.restart_button.bind('<Leave>', 
            lambda e: self.restart_button.configure(bg=self.colors['button']))

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and self.game_active:
            self.board[row][col] = self.current_player
            color = self.colors['x_color'] if self.current_player == 'X' else self.colors['o_color']
            self.buttons[row][col].configure(text=self.current_player,
                                           fg=color,
                                           bg=self.colors['button'])
            
            if self.check_winner():
                self.game_active = False
                self.status.configure(text=f"Player {self.current_player} wins!",
                                    fg=self.colors['win'])
                self.highlight_winner()
            elif self.is_game_over():
                self.game_active = False
                self.status.configure(text="It's a tie!",
                                    fg=self.colors['tie'])
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                color = self.colors['x_color'] if self.current_player == 'X' else self.colors['o_color']
                self.status.configure(text=f"Player {self.current_player}'s turn",
                                    fg=color)

    def highlight_winner(self):
        winning_combo = self.get_winning_combination()
        if winning_combo:
            for row, col in winning_combo:
                self.buttons[row][col].configure(bg=self.colors['win'])

    def get_winning_combination(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return [(i,0), (i,1), (i,2)]
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return [(0,i), (1,i), (2,i)]
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return [(0,0), (1,1), (2,2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return [(0,2), (1,1), (2,0)]
        return None

    def restart_game(self):
        self.initialize_game()
        self.play()

    def display(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])

    def check_winner(self):
        # Check rows, columns and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def is_game_over(self):
        if self.check_winner():
            return True
        return all(cell != ' ' for row in self.board for cell in row)
