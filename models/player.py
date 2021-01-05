from dataclasses import dataclass


@dataclass
class Player:
    player_id: str
    first_name: str
    last_name: str
    country_code: str
    current_rank: int
