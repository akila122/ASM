from typing import Set

from loguru import logger
from pandas import read_csv, DataFrame
from tqdm import tqdm

from config import ATP_PLAYERS_CSV_URL, ATP_RANKINGS_CURRENT_CSV_URL, ATP_MATCHES_2018_CSV_URL, \
    ATP_MATCHES_2019_CSV_URL, ATP_MATCHES_2020_CSV_URL, PLAYERS_2018_CSV_PATH, PLAYERS_2019_CSV_PATH, \
    PLAYERS_2020_CSV_PATH, PLAYERS_ALL_CSV_PATH, MATCHES_2018_CSV_PATH, MATCHES_2019_CSV_PATH, MATCHES_2020_CSV_PATH, \
    MATCHES_ALL_CSV_PATH, TOURNAMENTS_2020_CSV_PATH, TOURNAMENTS_2019_CSV_PATH, TOURNAMENTS_2018_CSV_PATH, \
    TOURNAMENTS_ALL_CSV_PATH
from models import Player, Match, Tourney


@logger.catch(reraise=True)
def fetch_data(write=True) -> (Set[Player], Set[Match], Set[Tourney]):
    # Matches data
    matches_source_urls = [ATP_MATCHES_2018_CSV_URL, ATP_MATCHES_2019_CSV_URL, ATP_MATCHES_2020_CSV_URL]
    matches_dfs = [read_csv(source_url) for source_url in matches_source_urls]
    logger.info(f'Fetched {[len(df) for df in matches_dfs]} atp_matches entries data from {matches_source_urls}. ')

    # Players data
    players_df = read_csv(ATP_PLAYERS_CSV_URL, header=None,
                          names=['player_id', 'first_name', 'last_name', 'hand', 'dob', 'country_code'],
                          index_col=False)
    logger.info(f'Fetched {len(players_df)} atp_players entries from {ATP_PLAYERS_CSV_URL} [{len(players_df)}]')

    rankings_df = read_csv(ATP_RANKINGS_CURRENT_CSV_URL, header=None,
                           names=['date', 'rank', 'player_id', 'points'])
    logger.info(f'Fetched {len(rankings_df)} atp_rankings_current entries from {ATP_RANKINGS_CURRENT_CSV_URL}')

    # Dump init
    matches: [Set[Match]] = [set() for _ in range(len(matches_dfs))]
    tournaments: [Set[Tourney]] = [set() for _ in range(len(matches_dfs))]
    players: [Set[Player]] = [set() for _ in range(len(matches_dfs))]

    for i, df in enumerate(matches_dfs):
        logger.info(f'Parsing {matches_source_urls[i]}.')
        for index, row in tqdm(df.iterrows(), total=len(df)):
            new_match = Match(tourney_id=row['tourney_id'], surface=row['surface'],
                              winner_id=row['winner_id'], loser_id=row['loser_id'],
                              )
            matches[i].add(new_match)
            dummy_tourney = Tourney(tourney_id=new_match.tourney_id)
            if dummy_tourney not in tournaments[i]:
                new_tourney = Tourney(tourney_id=row['tourney_id'], tourney_name=row['tourney_name'],
                                      surface=row['surface'], tourney_date=row['tourney_date'])
                tournaments[i].add(new_tourney)
            dummy_winner = Player(player_id=new_match.winner_id)
            if dummy_winner not in players[i]:
                player_id = new_match.winner_id
                new_player_df = players_df.query(f'player_id == {player_id}')
                current_ranking = rankings_df.query(f'player_id == {player_id}')
                if new_player_df.empty:
                    logger.error(
                        f'Player_id={player_id} found in {matches_source_urls[i]} as a winner_id'
                        f'but not found in {ATP_PLAYERS_CSV_URL}.'
                        f'Skipping this player.'
                    )
                elif len(new_player_df) != 1:
                    logger.error(
                        f'Player_id={player_id} found in {matches_source_urls[i]} as a winner_id'
                        f'contained {len(new_player_df)} times in {ATP_PLAYERS_CSV_URL}.'
                        f'Skipping this player.'
                    )
                else:
                    if len(current_ranking) > 1:
                        current_ranking = current_ranking.iloc[[0]]
                        logger.warning(
                            f'Player_id={player_id} found in {matches_source_urls[i]} as a winner_id'
                            f'contained {len(current_ranking)} times in {ATP_RANKINGS_CURRENT_CSV_URL}.'
                            f'Using first rank from atp_rankings_current.'
                        )
                    players[i].add(Player(
                        player_id=new_player_df['player_id'].item(),
                        first_name=new_player_df['first_name'].item(),
                        last_name=new_player_df['last_name'].item(),
                        country_code=new_player_df['country_code'].item(),
                        current_rank=int(current_ranking['rank']) if not current_ranking.empty else -1
                    ))
            dummy_loser = Player(player_id=new_match.loser_id)
            if dummy_loser not in players[i]:
                player_id = new_match.loser_id
                new_player_df = players_df.query(f'player_id == {player_id}')
                current_ranking = rankings_df.query(f'player_id == {player_id}')
                if new_player_df.empty:
                    logger.error(
                        f'Player_id={player_id} found in {matches_source_urls[i]} as a loser_id'
                        f'but not found in {ATP_PLAYERS_CSV_URL}.'
                        f'Skipping this player.'
                    )
                elif len(new_player_df) != 1:
                    logger.error(
                        f'Player_id={player_id} found in {matches_source_urls[i]} as a loser_id'
                        f'contained {len(new_player_df)} times in {ATP_PLAYERS_CSV_URL}.'
                        f'Skipping this player.'
                    )
                else:
                    if len(current_ranking) > 1:
                        current_ranking = current_ranking.iloc[[0]]
                        logger.warning(
                            f'Player_id={player_id} found in {matches_source_urls[i]} as a loser_id'
                            f'contained {len(current_ranking)} times in {ATP_RANKINGS_CURRENT_CSV_URL}.'
                            f'Using first rank from atp_rankings_current.'
                        )
                    players[i].add(Player(
                        player_id=new_player_df['player_id'].item(),
                        first_name=new_player_df['first_name'].item(),
                        last_name=new_player_df['last_name'].item(),
                        country_code=new_player_df['country_code'].item(),
                        current_rank=int(current_ranking['rank']) if not current_ranking.empty else -1
                    ))
        logger.success(
            f'Parsed total {len(players[i])} Players, {len(matches[i])} Matches and {len(tournaments[i])} Tournaments'
            f' from {matches_source_urls[i]}.'
        )

    if write:
        path_map = {
            'players': [PLAYERS_2018_CSV_PATH, PLAYERS_2019_CSV_PATH, PLAYERS_2020_CSV_PATH, PLAYERS_ALL_CSV_PATH],
            'matches': [MATCHES_2018_CSV_PATH, MATCHES_2019_CSV_PATH, MATCHES_2020_CSV_PATH, MATCHES_ALL_CSV_PATH],
            'tournaments': [TOURNAMENTS_2018_CSV_PATH, TOURNAMENTS_2019_CSV_PATH, TOURNAMENTS_2020_CSV_PATH,
                            TOURNAMENTS_ALL_CSV_PATH]
        }
        all_index = 3
        for i, df in enumerate(matches_dfs):
            _write_csv(players[i], path_map['players'][i])
            logger.success(f"Players data written to {path_map['players'][i]}")

            _write_csv(matches[i], path_map['matches'][i])
            logger.success(f"Matches data written to {path_map['matches'][i]}")

            _write_csv(tournaments[i], path_map['tournaments'][i])
            logger.success(f"Tournaments data written to {path_map['tournaments'][i]}")

        players_union = set()
        for players_ in players:
            players_union = players_union.union(players_)
        _write_csv(players_union, path_map['players'][all_index])
        logger.success(f"Players data written to {path_map['players'][all_index]}")

        matches_union = set()
        for matches_ in matches:
            matches_union = matches_union.union(matches_)
        _write_csv(matches_union, path_map['matches'][all_index])
        logger.success(f"Matches data written to {path_map['matches'][all_index]}")

        tournaments_union = set()
        for tournaments_ in tournaments:
            tournaments_union = tournaments_union.union(tournaments_)
        _write_csv(tournaments_union, path_map['tournaments'][all_index])
        logger.success(f"Tournaments data written to {path_map['tournaments'][all_index]}")

    logger.success(
        f'Players entries count by years ascending {[len(players_) for players_ in players]}.')
    logger.success(
        f'Matches data entries count by years ascending {[len(matches_) for matches_ in matches]}.')
    logger.success(
        f'Tournaments data entries count by years ascending {[len(tournaments_) for tournaments_ in tournaments]}.')
    if write:
        logger.success(
            f'Unions [[Player], [Match], [Tourney]] [{len(players_union)}, {len(matches_union)}, {len(tournaments_union)}].')

    return players, matches, tournaments


@logger.catch(reraise=True)
def _write_csv(source, write_to):
    data = [vars(x) for x in source]
    df = DataFrame(data)
    df.to_csv(write_to, index=False)


fetch_data()
