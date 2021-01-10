from typing import Set, Dict
from loguru import logger
from pandas import read_csv
from models import Player, Match, Tourney
from config import MATCHES_2020_CSV_PATH, MATCHES_2019_CSV_PATH, MATCHES_2018_CSV_PATH, MATCHES_ALL_CSV_PATH, \
    PLAYERS_2020_CSV_PATH, PLAYERS_2019_CSV_PATH, PLAYERS_2018_CSV_PATH, PLAYERS_ALL_CSV_PATH, \
    TOURNAMENTS_2020_CSV_PATH, TOURNAMENTS_2019_CSV_PATH, TOURNAMENTS_2018_CSV_PATH, TOURNAMENTS_ALL_CSV_PATH


@logger.catch(reraise=True)
def load_players_csv(path) -> Set[Player]:
    df = read_csv(path)
    data = set()
    for index, row in df.iterrows():
        data.add(Player(
            player_id=int(row['player_id']),
            first_name=row['first_name'],
            last_name=row['last_name'],
            country_code=row['country_code'],
            current_rank=row['current_rank'],
            current_points=row['current_points']

        ))
    logger.success(f'Loaded {len(data)} Player entries from {path}.')
    return data


@logger.catch(reraise=True)
def load_matches_csv(path) -> Set[Match]:
    df = read_csv(path)
    data = set()
    for index, row in df.iterrows():
        data.add(Match(
            tourney_id=row['tourney_id'],
            surface=row['surface'],
            winner_id=int(row['winner_id']),
            loser_id=int(row['loser_id'])
        ))
    logger.success(f'Loaded {len(data)} Match entries from {path}.')
    return data


@logger.catch(reraise=True)
def load_tournaments_csv(path) -> Set[Tourney]:
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
def load_data_csv(path) -> Set:
    if 'players' in path:
        return load_players_csv(path)
    elif 'matches' in path:
        return load_matches_csv(path)
    elif 'tournaments' in path:
        return load_tournaments_csv(path)


@logger.catch(reraise=True)
def load_all_dict() -> Dict[str, Set]:
    return {'players': load_data_csv(PLAYERS_ALL_CSV_PATH), 'matches': load_data_csv(MATCHES_ALL_CSV_PATH),
            'tournaments': load_data_csv(TOURNAMENTS_ALL_CSV_PATH)}


@logger.catch(reraise=True)
def load_2020_dict() -> Dict[str, Set]:
    return {'players': load_data_csv(PLAYERS_2020_CSV_PATH), 'matches': load_data_csv(MATCHES_2020_CSV_PATH),
            'tournaments': load_data_csv(TOURNAMENTS_2020_CSV_PATH)}


@logger.catch(reraise=True)
def load_2019_dict() -> Dict[str, Set]:
    return {'players': load_data_csv(PLAYERS_2019_CSV_PATH), 'matches': load_data_csv(MATCHES_2019_CSV_PATH),
            'tournaments': load_data_csv(TOURNAMENTS_2019_CSV_PATH)}


@logger.catch(reraise=True)
def load_2018_dict() -> Dict[str, Set]:
    return {'players': load_data_csv(PLAYERS_2018_CSV_PATH), 'matches': load_data_csv(MATCHES_2018_CSV_PATH),
            'tournaments': load_data_csv(TOURNAMENTS_2018_CSV_PATH)}
