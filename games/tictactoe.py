from .base_game import BaseGame
import tkinter as tk
from tkinter import ttk

class TicTacToe(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Tic Tac Toe")
        # Center the window
        window_width = 300
        window_height = 400
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
        self.frame.pack_forget()  # Clear any existing widgets
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=20, pady=20)

        # Status label
        self.status = tk.Label(self.frame, text=f"Player {self.current_player}'s turn",
                             font=('Helvetica', 14))
        self.status.pack(pady=10)

        # Game board
        board_frame = tk.Frame(self.frame)
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text='',
                                             font=('Helvetica', 24, 'bold'),
                                             width=3, height=1,
                                             command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

        # Restart button
        self.restart_button = ttk.Button(self.frame, text="Restart Game",
                                       command=self.restart_game)
        self.restart_button.pack(pady=20)

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and self.game_active:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player,
                                        fg='blue' if self.current_player == 'X' else 'red')
            
            if self.check_winner():
                self.game_active = False
                self.status.config(text=f"Player {self.current_player} wins!",
                                 fg='green')
                self.highlight_winner()
            elif self.is_game_over():
                self.game_active = False
                self.status.config(text="It's a tie!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status.config(text=f"Player {self.current_player}'s turn")

    def highlight_winner(self):
        # Highlight the winning combination
        winning_combo = self.get_winning_combination()
        if winning_combo:
            for row, col in winning_combo:
                self.buttons[row][col].config(bg='lightgreen')

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
