from abc import ABC, abstractmethod
import tkinter as tk

class BaseGame(ABC):
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, fill='both')

    @abstractmethod
    def play(self):
        """Initialize the game UI and start the game"""
        pass

    @abstractmethod
    def display(self):
        """Update the game display"""
        pass

    @abstractmethod
    def is_game_over(self):
        """Check if the game is over"""
        pass

    def restart(self):
        """Reset the game state to start a new game"""
        pass
