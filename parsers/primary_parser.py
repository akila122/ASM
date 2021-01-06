from loguru import logger
from tqdm import tqdm
from pandas import read_csv, DataFrame
from models import Player
from config import ATP_PLAYERS_CSV_URL, ATP_RANKINGS_CURRENT_CSV_URL, PLAYERS_FIRST_NAME_INDEX, PLAYERS_ID_INDEX, \
    PLAYERS_LAST_NAME_INDEX, PLAYERS_COUNTRY_CODE_INDEX, ATP_MATCHES_2018_CSV_URL, ATP_MATCHES_2019_CSV_URL, \
    ATP_MATCHES_2020_CSV_URL, PLAYERS_CSV_PATH


@logger.catch(reraise=True)
def parse_players(write=True) -> [Player]:
    players_df = read_csv(ATP_PLAYERS_CSV_URL, header=None)
    logger.info(f'Fetched {len(players_df)} atp_players entries from {ATP_PLAYERS_CSV_URL} [{len(players_df)}]')

    cr_df = read_csv(ATP_RANKINGS_CURRENT_CSV_URL, header=None,
                     names=['date', 'rank', 'player_id', 'points'])
    logger.info(f'Fetched {len(cr_df)} atp_rankings_current entries from {ATP_RANKINGS_CURRENT_CSV_URL}')

    matches18_df = read_csv(ATP_MATCHES_2018_CSV_URL)
    logger.info(f'Fetched {len(matches18_df)} atp_matches_2018 entries from {ATP_MATCHES_2018_CSV_URL}')

    matches19_df = read_csv(ATP_MATCHES_2019_CSV_URL)
    logger.info(f'Fetched {len(matches19_df)} atp_matches_2019 entries from {ATP_MATCHES_2019_CSV_URL}')

    matches20_df = read_csv(ATP_MATCHES_2020_CSV_URL)
    logger.info(f'Fetched {len(matches20_df)} atp_matches_2020 entries from {ATP_MATCHES_2020_CSV_URL}')

    players = []
    for index, row in tqdm(players_df.iterrows(), total=len(players_df)):
        player_id = row[PLAYERS_ID_INDEX]

        if matches18_df.query(f'winner_id == {player_id} | loser_id == {player_id}').empty and \
                matches19_df.query(f'winner_id == {player_id} | loser_id == {player_id}').empty and \
                matches20_df.query(f'winner_id == {player_id} | loser_id == {player_id}').empty:
            continue

        current_ranking = cr_df.query(f'player_id == {row[PLAYERS_ID_INDEX]}')
        if len(current_ranking) > 1:
            current_ranking = current_ranking.iloc[[0]]
        players.append(Player(
            player_id=row[PLAYERS_ID_INDEX],
            first_name=row[PLAYERS_FIRST_NAME_INDEX],
            last_name=row[PLAYERS_LAST_NAME_INDEX],
            country_code=row[PLAYERS_COUNTRY_CODE_INDEX],
            current_rank=int(current_ranking['rank']) if not current_ranking.empty else -1
        ))
    logger.success(f'Players parsing done. Parsed [{len(players)}] entries.')

    if write:
        logger.info(f'Writing players data to {PLAYERS_CSV_PATH}')
        data = [vars(player) for player in players]
        df = DataFrame(data)
        df.to_csv(PLAYERS_CSV_PATH)
        logger.success(f'Players data written to {PLAYERS_CSV_PATH}')

    return players


parse_players()
