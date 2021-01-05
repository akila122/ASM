from loguru import logger
from pandas import read_csv
from models import Player
from config import ATP_PLAYERS_CSV_URL, ATP_RANKINGS_CURRENT_CSV_URL, PLAYERS_FIRST_NAME_INDEX, PLAYERS_ID_INDEX, \
    PLAYERS_LAST_NAME_INDEX, PLAYERS_COUNTRY_CODE_INDEX


@logger.catch(reraise=True)
def parse_players() -> [Player]:
    players_df = read_csv(ATP_PLAYERS_CSV_URL, header=None)
    logger.info(f'Fetched data from {ATP_PLAYERS_CSV_URL}')
    cr_df = read_csv(ATP_RANKINGS_CURRENT_CSV_URL, header=None,
                                   names=['date', 'rank', 'player_id', 'points'])
    logger.info(f'Fetched data from {ATP_RANKINGS_CURRENT_CSV_URL}')
    players = []
    for index, row in players_df.iterrows():
        players.append(Player(
            player_id=row[PLAYERS_ID_INDEX],
            first_name=row[PLAYERS_FIRST_NAME_INDEX],
            last_name=row[PLAYERS_LAST_NAME_INDEX],
            country_code=row[PLAYERS_COUNTRY_CODE_INDEX],
            current_rank=int(cr_df[cr_df.player_id == row[PLAYERS_ID_INDEX]]['rank'] or -1)
        ))
        return players


print(parse_players())
