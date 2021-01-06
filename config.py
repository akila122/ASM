import os

# URL REGION BEGIN
ATP_MATCHES_2018_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2018.csv'
ATP_MATCHES_2019_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2019.csv'
ATP_MATCHES_2020_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2020.csv'
ATP_RANKINGS_CURRENT_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_current.csv'
ATP_RANKINGS_10S_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_10s.csv'
ATP_PLAYERS_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv'
# URL REGION END

# GITHUB DATA REGION BEGIN
PLAYERS_ID_INDEX = 0
PLAYERS_FIRST_NAME_INDEX = 1
PLAYERS_LAST_NAME_INDEX = 2
PLAYERS_COUNTRY_CODE_INDEX = 5

RANKINGS_CURRENT_RANK_INDEX = 1
# GITHUB DATA REGION END

# FILE REGION BEGIN
ROOT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PLAYERS_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/players.csv')
# FILE REGION END
