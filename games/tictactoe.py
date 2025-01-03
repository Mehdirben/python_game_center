from .base_game import BaseGame
import tkinter as tk
from tkinter import messagebox

class TicTacToe(BaseGame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Tic Tac Toe")
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

    def play(self):
        # Status label
        self.status = tk.Label(self.frame, text=f"Player {self.current_player}'s turn",
                             font=('Helvetica', 12))
        self.status.pack(pady=10)

        # Game board
        board_frame = tk.Frame(self.frame)
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text='',
                                             font=('Helvetica', 20),
                                             width=5, height=2,
                                             command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.is_game_over():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.master.destroy()
            elif self.is_game_over():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.master.destroy()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status.config(text=f"Player {self.current_player}'s turn")

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
