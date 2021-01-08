from dataclasses import dataclass


@dataclass
class Player:
    player_id: str = None
    first_name: str = None
    last_name: str = None
    country_code: str = None
    current_rank: int = None

    # For Set Impl
    def __eq__(self, other):
        return self.player_id == other.player_id

    def __hash__(self):
        return hash(self.player_id)
