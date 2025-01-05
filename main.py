import tkinter as tk
from tkinter import ttk
from games.tictactoe import TicTacToe
from games.snake import Snake
from games.game2048 import Game2048
from games.tetris import Tetris

class GameCenter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Game Center")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e2f')  # Dark background for modern look
        
        self.games = {
            'Tic Tac Toe': {
                'class': TicTacToe,
                'description': 'Classic X and O game',
                'icon': '❌'
            },
            'Snake': {
                'class': Snake,
                'description': 'Classic snake game',
                'icon': '🐍'
            },
            '2048': {
                'class': Game2048,
                'description': 'Merge numbers puzzle',
                'icon': '🎲'
            },
            'Tetris': {
                'class': Tetris,
                'description': 'Classic block stacking game',
                'icon': '🟦'
            }
        }
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
        
        # Title style
        style.configure('Title.TLabel', 
                       font=('Helvetica', 32, 'bold'),
                       background='#1e1e2f',
                       foreground='#ffffff')
        
        # Game card style
        style.configure('Game.TFrame',
                       background='#2a2a40',
                       relief='flat',
                       borderwidth=0,
                       bordercolor='#3a3a5c',
                       padding=20)
        
        # Game title style
        style.configure('GameTitle.TLabel',
                       font=('Helvetica', 18, 'bold'),
                       background='#2a2a40',
                       foreground='#ffffff')
        
        # Game description style
        style.configure('GameDescription.TLabel',
                       font=('Helvetica', 12),
                       background='#2a2a40',
                       foreground='#a0a0c0',
                       wraplength=200)
        
        # Modern button style
        style.configure('Modern.TButton',
                       font=('Helvetica', 12, 'bold'),
                       background='#3a3a5c',
                       foreground='#ffffff',
                       borderwidth=0,
                       padding=10,
                       focuscolor='none')
        style.map('Modern.TButton',
                 background=[('active', '#4a4a6c'), ('pressed', '#2a2a40')],
                 foreground=[('active', '#ffffff')])
        
        # Quit button style
        style.configure('Quit.TButton',
                       font=('Helvetica', 12, 'bold'),
                       background='#ff4d4d',
                       foreground='#ffffff',
                       borderwidth=0,
                       padding=10,
                       focuscolor='none')
        style.map('Quit.TButton',
                 background=[('active', '#ff6666'), ('pressed', '#cc3d3d')],
                 foreground=[('active', '#ffffff')])

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Python Game Center", style='Title.TLabel')
        title.pack(pady=30)
        
        # Games container
        container = ttk.Frame(self.root, padding=20)
        container.pack(expand=True, fill='both')
        
        # Create game cards in a grid
        row = 0
        col = 0
        for game_name, game_info in self.games.items():
            card = ttk.Frame(container, style='Game.TFrame', padding=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Game icon
            icon = ttk.Label(card, text=game_info['icon'], font=('Helvetica', 48), background='#2a2a40', foreground='#ffffff')
            icon.pack(pady=(0, 10))
            
            # Game title
            title = ttk.Label(card, text=game_name, style='GameTitle.TLabel')
            title.pack()
            
            # Game description
            desc = ttk.Label(card, text=game_info['description'], 
                           style='GameDescription.TLabel', wraplength=200)
            desc.pack(pady=(5, 15))
            
            # Play button
            play_btn = ttk.Button(card, text="Play Now",
                                style='Modern.TButton',
                                command=lambda g=game_info['class']: self.start_game(g))
            play_btn.pack()
            
            # Grid positioning
            col += 1
            if col > 1:
                col = 0
                row += 1
            
            # Make columns and rows expand equally
            container.grid_columnconfigure(0, weight=1)
            container.grid_columnconfigure(1, weight=1)
        
        # Quit button
        quit_btn = ttk.Button(self.root, text="Exit Game Center",
                            style='Quit.TButton',
                            command=self.root.destroy)
        quit_btn.pack(pady=20)

    def start_game(self, game_class):
        game_window = tk.Toplevel(self.root)
        game_window.focus_force()  # Force focus to the new window
        game_window.lift()         # Bring window to front
        game = game_class(game_window)
        game.play()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game_center = GameCenter()
    game_center.run()