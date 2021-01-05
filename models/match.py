from dataclasses import dataclass


@dataclass
class Match:
    tourney_id: str
    surface: str
    winner_id: str
    loser_id: str
    winner_rank: int
    loser_rank: int
