from dataclasses import dataclass
from settings import (
    TAG_POINTS, FRIENDLY_FIRE_PENALTY, BASE_HIT_POINTS,
    RED_BASE_CODE, GREEN_BASE_CODE, TEAM_RED, TEAM_GREEN,
)


@dataclass
class ScoringResult:
    event_text: str
    is_friendly_fire: bool = False
    is_base_hit: bool = False


class ScoringEngine:
    def __init__(self, game_state):
        self.game_state = game_state

    def process_event(self, transmitter_equip_id, hit_equip_id):
        shooter = self.game_state.get_player_by_equip(transmitter_equip_id)
        if shooter is None:
            return None

        # Ignore self-hits
        if transmitter_equip_id == hit_equip_id:
            return None

        # Red base hit (hit_equip_id == 53) — green player scores
        if hit_equip_id == RED_BASE_CODE:
            if shooter.team != TEAM_GREEN:
                return None
            shooter.score += BASE_HIT_POINTS
            shooter.has_base_hit = True
            return ScoringResult(
                event_text=f"{shooter.codename} hit the RED base! (+{BASE_HIT_POINTS})",
                is_base_hit=True,
            )

        # Green base hit (hit_equip_id == 43) — red player scores
        if hit_equip_id == GREEN_BASE_CODE:
            if shooter.team != TEAM_RED:
                return None
            shooter.score += BASE_HIT_POINTS
            shooter.has_base_hit = True
            return ScoringResult(
                event_text=f"{shooter.codename} hit the GREEN base! (+{BASE_HIT_POINTS})",
                is_base_hit=True,
            )

        # Look up the target player
        target = self.game_state.get_player_by_equip(hit_equip_id)
        if target is None:
            return None

        # Friendly fire (same team)
        if shooter.team == target.team:
            shooter.score -= FRIENDLY_FIRE_PENALTY
            target.score -= FRIENDLY_FIRE_PENALTY
            return ScoringResult(
                event_text=f"{shooter.codename} hit teammate {target.codename}! (-{FRIENDLY_FIRE_PENALTY} each)",
                is_friendly_fire=True,
            )

        # Normal tag (opposing team)
        shooter.score += TAG_POINTS
        return ScoringResult(
            event_text=f"{shooter.codename} hit {target.codename} (+{TAG_POINTS})",
        )
