import tkinter as tk
from tkinter import simpledialog, messagebox
from game_state import Player
from settings import MAX_PLAYERS_PER_TEAM, TEAM_RED, TEAM_GREEN, RED_BASE_CODE, GREEN_BASE_CODE


class PlayerEntryScreen:
    def __init__(self, root, game_state, database, network, on_start_game):
        self.root = root
        self.game_state = game_state
        self.database = database
        self.network = network
        self.on_start_game = on_start_game

        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Storage for entry widgets
        self.red_entries = []   # list of (id_entry, codename_label)
        self.green_entries = []

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Title
        title = tk.Label(
            self.frame, text="Edit Current Game",
            font=("Helvetica", 24, "bold"), fg="white", bg="black",
        )
        title.pack(pady=10)

        # Main columns container
        columns = tk.Frame(self.frame, bg="black")
        columns.pack(fill=tk.BOTH, expand=True, padx=20)

        # Red team column
        red_frame = tk.Frame(columns, bg="black")
        red_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(
            red_frame, text="RED TEAM", font=("Helvetica", 18, "bold"),
            fg="red", bg="black",
        ).pack(pady=5)

        red_header = tk.Frame(red_frame, bg="black")
        red_header.pack(fill=tk.X)
        tk.Label(red_header, text="#", width=3, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(red_header, text="Player ID", width=12, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(red_header, text="Codename", width=16, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(red_header, text="Equip ID", width=8, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)

        for i in range(MAX_PLAYERS_PER_TEAM):
            row = tk.Frame(red_frame, bg="black")
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=str(i + 1), width=3, fg="white", bg="black",
                     font=("Helvetica", 10)).pack(side=tk.LEFT)
            id_entry = tk.Entry(row, width=12, font=("Helvetica", 10))
            id_entry.pack(side=tk.LEFT, padx=2)
            codename_lbl = tk.Label(row, text="", width=16, fg="white",
                                    bg="black", font=("Helvetica", 10), anchor="w")
            codename_lbl.pack(side=tk.LEFT, padx=2)
            equip_lbl = tk.Label(row, text="", width=8, fg="white",
                                 bg="black", font=("Helvetica", 10), anchor="w")
            equip_lbl.pack(side=tk.LEFT, padx=2)
            id_entry.bind("<Return>", lambda e, idx=i, t=TEAM_RED: self._on_id_enter(idx, t))
            id_entry.bind("<Tab>", lambda e, idx=i, t=TEAM_RED: self._on_id_enter(idx, t) or "break")
            self.red_entries.append((id_entry, codename_lbl, equip_lbl))

        # Green team column
        green_frame = tk.Frame(columns, bg="black")
        green_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(
            green_frame, text="GREEN TEAM", font=("Helvetica", 18, "bold"),
            fg="green", bg="black",
        ).pack(pady=5)

        green_header = tk.Frame(green_frame, bg="black")
        green_header.pack(fill=tk.X)
        tk.Label(green_header, text="#", width=3, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(green_header, text="Player ID", width=12, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(green_header, text="Codename", width=16, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(green_header, text="Equip ID", width=8, fg="white", bg="black",
                 font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)

        for i in range(MAX_PLAYERS_PER_TEAM):
            row = tk.Frame(green_frame, bg="black")
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=str(i + 1), width=3, fg="white", bg="black",
                     font=("Helvetica", 10)).pack(side=tk.LEFT)
            id_entry = tk.Entry(row, width=12, font=("Helvetica", 10))
            id_entry.pack(side=tk.LEFT, padx=2)
            codename_lbl = tk.Label(row, text="", width=16, fg="white",
                                    bg="black", font=("Helvetica", 10), anchor="w")
            codename_lbl.pack(side=tk.LEFT, padx=2)
            equip_lbl = tk.Label(row, text="", width=8, fg="white",
                                 bg="black", font=("Helvetica", 10), anchor="w")
            equip_lbl.pack(side=tk.LEFT, padx=2)
            id_entry.bind("<Return>", lambda e, idx=i, t=TEAM_GREEN: self._on_id_enter(idx, t))
            id_entry.bind("<Tab>", lambda e, idx=i, t=TEAM_GREEN: self._on_id_enter(idx, t) or "break")
            self.green_entries.append((id_entry, codename_lbl, equip_lbl))

        # Bottom button bar
        btn_bar = tk.Frame(self.frame, bg="black")
        btn_bar.pack(fill=tk.X, pady=10, padx=20)

        tk.Button(
            btn_bar, text="F5 / F3 - Start Game", font=("Helvetica", 12),
            command=self._start_game, bg="#333", fg="white",
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_bar, text="F12 - Clear All", font=("Helvetica", 12),
            command=self._clear_all, bg="#333", fg="white",
        ).pack(side=tk.RIGHT, padx=10)

    def _bind_keys(self):
        self.root.bind("<F5>", lambda e: self._start_game())
        self.root.bind("<F3>", lambda e: self._start_game())
        self.root.bind("<F12>", lambda e: self._clear_all())

    def _unbind_keys(self):
        self.root.unbind("<F5>")
        self.root.unbind("<F3>")
        self.root.unbind("<F12>")

    def _on_id_enter(self, row_index, team):
        entries = self.red_entries if team == TEAM_RED else self.green_entries
        id_entry, codename_lbl, equip_lbl = entries[row_index]

        # Remove old player if this row is being re-entered
        old_equip_text = equip_lbl.cget("text").strip()
        if old_equip_text:
            try:
                self.game_state.remove_player(int(old_equip_text))
            except (ValueError, KeyError):
                pass
            equip_lbl.config(text="")
            codename_lbl.config(text="")

        player_id = id_entry.get().strip()
        if not player_id:
            return

        # Look up codename in DB
        codename = None
        if self.database:
            codename = self.database.get_codename(player_id)

        if codename is None:
            # Prompt for new codename
            codename = simpledialog.askstring(
                "New Player",
                f"Player ID {player_id} not found.\nEnter codename:",
                parent=self.root,
            )
            if not codename:
                return
            # Insert into DB
            if self.database:
                self.database.insert_player(player_id, codename)

        codename_lbl.config(text=codename)

        # Check for duplicate player ID
        for p in self.game_state.get_all_players():
            if p.player_id == player_id:
                messagebox.showerror("Error", f"Player ID {player_id} already registered as {p.codename}.")
                codename_lbl.config(text="")
                return

        # Prompt for equipment ID
        equip_str = simpledialog.askstring(
            "Equipment ID",
            f"Enter equipment ID for {codename}:",
            parent=self.root,
        )
        if not equip_str:
            codename_lbl.config(text="")
            return
        try:
            equip_id = int(equip_str)
        except ValueError:
            messagebox.showerror("Error", "Equipment ID must be a number.")
            codename_lbl.config(text="")
            return

        # Reject base station codes
        if equip_id in (RED_BASE_CODE, GREEN_BASE_CODE):
            messagebox.showerror("Error", f"Equipment ID {equip_id} is reserved for base stations.")
            codename_lbl.config(text="")
            return

        # Check for duplicate equipment ID
        existing = self.game_state.get_player_by_equip(equip_id)
        if existing:
            messagebox.showerror("Error", f"Equipment ID {equip_id} already assigned to {existing.codename}.")
            codename_lbl.config(text="")
            equip_lbl.config(text="")
            return

        equip_lbl.config(text=str(equip_id))

        # Register player in game state
        player = Player(
            player_id=player_id,
            codename=codename,
            team=team,
            equipment_id=equip_id,
        )
        self.game_state.add_player(player)

        # Broadcast equipment ID via UDP
        self.network.transmit(equip_id)

    def _start_game(self):
        red_players = self.game_state.get_players_by_team(TEAM_RED)
        green_players = self.game_state.get_players_by_team(TEAM_GREEN)
        if not red_players or not green_players:
            messagebox.showwarning(
                "Cannot Start",
                "At least one player required on each team.",
            )
            return
        self._unbind_keys()
        self.on_start_game()

    def _clear_all(self):
        self.game_state.reset()
        for entries in (self.red_entries, self.green_entries):
            for id_entry, codename_lbl, equip_lbl in entries:
                id_entry.delete(0, tk.END)
                codename_lbl.config(text="")
                equip_lbl.config(text="")

    def destroy(self):
        self._unbind_keys()
        self.frame.destroy()
