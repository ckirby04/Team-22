import tkinter as tk
import pygame
from database import Database
from game_state import GameState
from network import NetworkManager
from music_manager import MusicManager
from splash_screen import SplashScreen
from player_entry_screen import PlayerEntryScreen
from play_action_screen import PlayActionScreen


class PhotonApp:
    def __init__(self):
        # Initialize pygame for audio
        pygame.init()
        pygame.mixer.init()

        # Create root window
        self.root = tk.Tk()
        self.root.title("Photon Laser Tag")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self._quit())

        # Initialize subsystems
        self.database = Database()
        self.game_state = GameState()
        self.network = NetworkManager(self.root)
        self.music_manager = MusicManager()

        self._current_screen = None

        # Start with splash screen
        self.show_splash()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    def show_splash(self):
        self._clear_screen()
        self._current_screen = SplashScreen(self.root, self.show_player_entry)

    def show_player_entry(self):
        self._clear_screen()
        self.game_state.reset()
        self._current_screen = PlayerEntryScreen(
            self.root, self.game_state, self.database,
            self.network, self.show_play_action,
        )

    def show_play_action(self):
        self._clear_screen()
        self._current_screen = PlayActionScreen(
            self.root, self.game_state, self.network,
            self.music_manager, self.show_player_entry,
        )

    def _clear_screen(self):
        if self._current_screen:
            self._current_screen.destroy()
            self._current_screen = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def _quit(self):
        self.network.shutdown()
        self.database.close()
        pygame.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PhotonApp()
    app.run()
