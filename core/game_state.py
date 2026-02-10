from dataclasses import dataclass


@dataclass
class Player:
    player_id: str
    codename: str
    team: str
    equipment_id: int
    score: int = 0
    has_base_hit: bool = False


class GameState:
    def __init__(self):
        # equipment_id -> Player
        self._by_equip = {}
        # team -> list of Players
        self._by_team = {"red": [], "green": []}

    def add_player(self, player):
        self._by_equip[player.equipment_id] = player
        self._by_team[player.team].append(player)

    def remove_player(self, equipment_id):
        player = self._by_equip.pop(equipment_id, None)
        if player:
            team_list = self._by_team.get(player.team, [])
            if player in team_list:
                team_list.remove(player)

    def get_player_by_equip(self, equipment_id):
        return self._by_equip.get(equipment_id)

    def get_players_by_team(self, team):
        return list(self._by_team.get(team, []))

    def get_team_total(self, team):
        return sum(p.score for p in self._by_team.get(team, []))

    def get_all_players(self):
        return list(self._by_equip.values())

    def reset(self):
        self._by_equip.clear()
        self._by_team = {"red": [], "green": []}

    def reset_scores(self):
        for player in self._by_equip.values():
            player.score = 0
            player.has_base_hit = False
