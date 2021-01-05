from loguru import logger
from pandas import read_csv
from models import Player
from config import ATP_PLAYERS_CSV_URL, ATP_RANKINGS_CURRENT_CSV_URL, PLAYERS_FIRST_NAME_INDEX, PLAYERS_ID_INDEX, \
    PLAYERS_LAST_NAME_INDEX, PLAYERS_COUNTRY_CODE_INDEX


@logger.catch(reraise=True)
def parse_players() -> [Player]:
    players_df = read_csv(ATP_PLAYERS_CSV_URL)
    logger.info(f'Fetched data from {ATP_PLAYERS_CSV_URL}')
    current_rankings_df = read_csv(ATP_RANKINGS_CURRENT_CSV_URL)
    logger.info(f'Fetched data from {ATP_RANKINGS_CURRENT_CSV_URL}')
    players = []
    for index, row in players_df.iterrows():
        players.append(Player(
            player_id=row[PLAYERS_ID_INDEX],
            first_name=row[PLAYERS_FIRST_NAME_INDEX],
            last_name=row[PLAYERS_LAST_NAME_INDEX],
            country_code=row[PLAYERS_COUNTRY_CODE_INDEX],
            current_rank=-1
        ))
    return players


print(parse_players())
