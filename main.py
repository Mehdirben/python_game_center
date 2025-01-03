import tkinter as tk
from tkinter import ttk
from games.tictactoe import TicTacToe
from games.snake import Snake
from games.game2048 import Game2048

class GameCenter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Game Center")
        self.root.geometry("400x500")
        
        self.games = {
            'Tic Tac Toe': TicTacToe,
            'Snake': Snake,
            '2048': Game2048,
        }
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Python Game Center", font=('Helvetica', 24))
        title.pack(pady=20)
        
        # Game buttons
        for game_name, game_class in self.games.items():
            btn = ttk.Button(self.root, text=game_name,
                           command=lambda g=game_class: self.start_game(g))
            btn.pack(pady=10, padx=50, fill=tk.X)
        
        # Quit button
        quit_btn = ttk.Button(self.root, text="Quit",
                            command=self.root.destroy)
        quit_btn.pack(pady=20)

    def start_game(self, game_class):
        game_window = tk.Toplevel(self.root)
        game = game_class(game_window)
        game.play()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game_center = GameCenter()
    game_center.run()
