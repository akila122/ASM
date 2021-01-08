from typing import Set
from loguru import logger
from pandas import read_csv
from models import Player, Match, Tourney


@logger.catch(reraise=True)
def load_players(path) -> Set[Player]:
    df = read_csv(path)
    data = set()
    for index, row in df.iterrows():
        data.add(Player(
            player_id=row['player_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            country_code=row['country_code'],
            current_rank=row['current_rank'],
            current_points=row['current_points']

        ))
    logger.success(f'Loaded {len(data)} Player entries from {path}.')
    return data


@logger.catch(reraise=True)
def load_matches(path) -> Set[Match]:
    df = read_csv(path)
    data = set()
    for index, row in df.iterrows():
        data.add(Match(
            tourney_id=row['tourney_id'],
            surface=row['surface'],
            winner_id=row['winner_id'],
            loser_id=row['loser_id']
        ))
    logger.success(f'Loaded {len(data)} Match entries from {path}.')
    return data


@logger.catch(reraise=True)
def load_tournaments(path) -> Set[Tourney]:
    df = read_csv(path)
    data = set()
    for index, row in df.iterrows():
        data.add(Tourney(
            tourney_id=row['tourney_id'],
            tourney_name=row['tourney_name'],
            surface=row['surface'],
            tourney_date=row['tourney_date'],
        ))
    logger.success(f'Loaded {len(data)} Tourney entries from {path}.')
    return data


@logger.catch(reraise=True)
def load_data(path) -> Set:
    if 'players' in path:
        return load_players(path)
    elif 'matches' in path:
        return load_matches(path)
    elif 'tournaments' in path:
        return load_tournaments(path)
