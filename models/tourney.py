from dataclasses import dataclass
from datetime import date


@dataclass
class Tourney:
    tourney_id: str
    tourney_name: str
    surface: str
    tourney_date: str