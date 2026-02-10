import tkinter as tk
import pygame
from PIL import Image, ImageTk
from screens.countdown_display import CountdownDisplay
from core.scoring_engine import ScoringEngine
from core.music_manager import MUSIC_END_EVENT
from settings import (
    GAME_DURATION_SECONDS, GAME_START_CODE, GAME_END_CODE,
    TEAM_RED, TEAM_GREEN, BASE_ICON_PATH,
)


class PlayActionScreen:
    def __init__(self, root, game_state, network, music_manager, on_back):
        self.root = root
        self.game_state = game_state
        self.network = network
        self.music_manager = music_manager
        self.on_back = on_back
        self.scoring_engine = ScoringEngine(game_state)

        self._time_remaining = GAME_DURATION_SECONDS
        self._timer_id = None
        self._pygame_poll_id = None
        self._flash_state = True
        self._flash_id = None
        self._game_running = False

        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load base icon
        self._base_icon = None
        try:
            img = Image.open(BASE_ICON_PATH)
            img = img.resize((20, 20), Image.LANCZOS)
            self._base_icon = ImageTk.PhotoImage(img)
        except Exception:
            pass

        self._build_ui()

        # Reset scores for new game
        self.game_state.reset_scores()

        # Start with countdown overlay
        self._countdown = CountdownDisplay(root, self._on_countdown_complete)

    def _build_ui(self):
        # Timer at top
        self._timer_label = tk.Label(
            self.frame, text=self._format_time(self._time_remaining),
            font=("Helvetica", 28, "bold"), fg="white", bg="black",
        )
        self._timer_label.pack(pady=10)

        # Main content: scores left/right, event log center
        content = tk.Frame(self.frame, bg="black")
        content.pack(fill=tk.BOTH, expand=True, padx=10)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.columnconfigure(2, weight=1)

        # Red team scores (left)
        red_frame = tk.Frame(content, bg="black")
        red_frame.grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(
            red_frame, text="RED TEAM", font=("Helvetica", 16, "bold"),
            fg="red", bg="black",
        ).pack()

        self._red_scores_frame = tk.Frame(red_frame, bg="black")
        self._red_scores_frame.pack(fill=tk.BOTH, expand=True)

        self._red_total_label = tk.Label(
            red_frame, text="Total: 0", font=("Helvetica", 14, "bold"),
            fg="red", bg="black",
        )
        self._red_total_label.pack(pady=5)

        # Event log (center)
        log_frame = tk.Frame(content, bg="black")
        log_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(
            log_frame, text="Event Log", font=("Helvetica", 16, "bold"),
            fg="white", bg="black",
        ).pack()

        self._event_log = tk.Text(
            log_frame, width=40, height=25, bg="#111", fg="white",
            font=("Courier", 10), state=tk.DISABLED, wrap=tk.WORD,
        )
        self._event_log.pack(fill=tk.BOTH, expand=True)
        self._event_log.tag_config("friendly_fire", foreground="yellow")
        self._event_log.tag_config("base_hit", foreground="cyan")

        # Green team scores (right)
        green_frame = tk.Frame(content, bg="black")
        green_frame.grid(row=0, column=2, sticky="nsew", padx=5)

        tk.Label(
            green_frame, text="GREEN TEAM", font=("Helvetica", 16, "bold"),
            fg="green", bg="black",
        ).pack()

        self._green_scores_frame = tk.Frame(green_frame, bg="black")
        self._green_scores_frame.pack(fill=tk.BOTH, expand=True)

        self._green_total_label = tk.Label(
            green_frame, text="Total: 0", font=("Helvetica", 14, "bold"),
            fg="green", bg="black",
        )
        self._green_total_label.pack(pady=5)

        # Back button (hidden during game, shown after)
        self._back_btn = tk.Button(
            self.frame, text="F1 - Back to Player Entry",
            font=("Helvetica", 14), command=self._go_back,
            bg="#333", fg="white",
        )

        self._refresh_scores()

    def _on_countdown_complete(self):
        self._countdown = None
        self._game_running = True

        # Broadcast game start
        self.network.transmit(GAME_START_CODE)

        # Start receiving UDP events
        self.network.start_receiving(self._on_udp_receive)

        # Start music
        self.music_manager.play_random_track()

        # Start game timer
        self._tick_timer()

        # Start pygame event polling (for music chaining)
        self._poll_pygame()

        # Start flashing leading team total
        self._flash_totals()

        # Bind F1
        self.root.bind("<F1>", lambda e: self._go_back())

    def _tick_timer(self):
        self._timer_label.config(text=self._format_time(self._time_remaining))
        if self._time_remaining <= 0:
            self._end_game()
            return
        self._time_remaining -= 1
        self._timer_id = self.root.after(1000, self._tick_timer)

    def _poll_pygame(self):
        for event in pygame.event.get():
            if event.type == MUSIC_END_EVENT:
                self.music_manager.handle_music_end_event()
        self._pygame_poll_id = self.root.after(100, self._poll_pygame)

    def _flash_totals(self):
        red_total = self.game_state.get_team_total(TEAM_RED)
        green_total = self.game_state.get_team_total(TEAM_GREEN)

        self._flash_state = not self._flash_state

        if red_total > green_total:
            fg = "red" if self._flash_state else "black"
            self._red_total_label.config(fg=fg)
            self._green_total_label.config(fg="green")
        elif green_total > red_total:
            fg = "green" if self._flash_state else "black"
            self._green_total_label.config(fg=fg)
            self._red_total_label.config(fg="red")
        else:
            self._red_total_label.config(fg="red")
            self._green_total_label.config(fg="green")

        self._flash_id = self.root.after(500, self._flash_totals)

    def _on_udp_receive(self, tx_id, hit_id):
        if not self._game_running:
            return

        result = self.scoring_engine.process_event(tx_id, hit_id)
        if result is None:
            return

        # Log the event
        tag = ""
        if result.is_friendly_fire:
            tag = "friendly_fire"
        elif result.is_base_hit:
            tag = "base_hit"

        self._event_log.config(state=tk.NORMAL)
        self._event_log.insert(tk.END, result.event_text + "\n", tag)
        self._event_log.see(tk.END)
        self._event_log.config(state=tk.DISABLED)

        # Retransmit: send the hit equipment ID back
        self.network.transmit(hit_id)

        # For friendly fire, also send the transmitter's ID
        if result.is_friendly_fire:
            self.network.transmit(tx_id)

        # Refresh scores
        self._refresh_scores()

    def _refresh_scores(self):
        # Clear and rebuild red team scores
        for widget in self._red_scores_frame.winfo_children():
            widget.destroy()
        red_players = sorted(
            self.game_state.get_players_by_team(TEAM_RED),
            key=lambda p: p.score, reverse=True,
        )
        for p in red_players:
            row = tk.Frame(self._red_scores_frame, bg="black")
            row.pack(fill=tk.X, pady=1)
            if p.has_base_hit and self._base_icon:
                tk.Label(row, image=self._base_icon, bg="black").pack(side=tk.LEFT)
            tk.Label(
                row, text=f"  {p.codename}", font=("Helvetica", 11),
                fg="white", bg="black", anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(
                row, text=str(p.score), font=("Helvetica", 11, "bold"),
                fg="red", bg="black",
            ).pack(side=tk.RIGHT)

        red_total = self.game_state.get_team_total(TEAM_RED)
        self._red_total_label.config(text=f"Total: {red_total}")

        # Clear and rebuild green team scores
        for widget in self._green_scores_frame.winfo_children():
            widget.destroy()
        green_players = sorted(
            self.game_state.get_players_by_team(TEAM_GREEN),
            key=lambda p: p.score, reverse=True,
        )
        for p in green_players:
            row = tk.Frame(self._green_scores_frame, bg="black")
            row.pack(fill=tk.X, pady=1)
            if p.has_base_hit and self._base_icon:
                tk.Label(row, image=self._base_icon, bg="black").pack(side=tk.LEFT)
            tk.Label(
                row, text=f"  {p.codename}", font=("Helvetica", 11),
                fg="white", bg="black", anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(
                row, text=str(p.score), font=("Helvetica", 11, "bold"),
                fg="green", bg="black",
            ).pack(side=tk.RIGHT)

        green_total = self.game_state.get_team_total(TEAM_GREEN)
        self._green_total_label.config(text=f"Total: {green_total}")

    def _end_game(self):
        self._game_running = False

        # Broadcast game end three times
        for _ in range(3):
            self.network.transmit(GAME_END_CODE)

        # Stop receiving and music
        self.network.stop_receiving()
        self.music_manager.stop()

        # Stop polling
        if self._pygame_poll_id:
            self.root.after_cancel(self._pygame_poll_id)
            self._pygame_poll_id = None
        if self._flash_id:
            self.root.after_cancel(self._flash_id)
            self._flash_id = None

        # Update timer display
        self._timer_label.config(text="Game Over!")

        # Show back button
        self._back_btn.pack(pady=10)

    def _go_back(self):
        if self._game_running:
            return
        self.root.unbind("<F1>")
        self.on_back()

    @staticmethod
    def _format_time(seconds):
        m = seconds // 60
        s = seconds % 60
        return f"Time Remaining: {m}:{s:02d}"

    def destroy(self):
        # Cancel all pending after calls
        for aid in (self._timer_id, self._pygame_poll_id, self._flash_id):
            if aid:
                try:
                    self.root.after_cancel(aid)
                except Exception:
                    pass
        if self._countdown:
            self._countdown.destroy()
        self.root.unbind("<F1>")
        self.frame.destroy()
