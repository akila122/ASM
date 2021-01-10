from dataclasses import dataclass

from models import Player


@dataclass
class Match:
    tourney_id: str = None
    surface: str = None
    winner_id: int = None
    loser_id: int = None

    # For Set Impl
    def __eq__(self, other):
        return id(self) == id(self)

    def __hash__(self):
        return id(self)

    # For unpacking Match to (str, str) in pythonic way
    # eg *match -> (winner_id,loser_id) which can be used as networkx edge
    def __iter__(self):
        return iter((self.winner_id, self.loser_id))


class MatchWrapper(Match):
    pass
