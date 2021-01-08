from dataclasses import dataclass


@dataclass
class Match:
    tourney_id: str = None
    surface: str = None
    winner_id: str = None
    loser_id: str = None

    # For Set Impl
    def __eq__(self, other):
        return id(self) == id(self)

    def __hash__(self):
        return id(self)
