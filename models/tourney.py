from dataclasses import dataclass
from datetime import date


@dataclass
class Tourney:
    tourney_id: str = None
    tourney_name: str = None
    surface: str = None
    tourney_date: str = None

    # For Set Impl
    def __eq__(self, other):
        return self.tourney_id == other.tourney_id

    def __hash__(self):
        return hash(self.tourney_id)
