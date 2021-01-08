import os

# URL REGION BEGIN
ATP_MATCHES_2018_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2018.csv'
ATP_MATCHES_2019_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2019.csv'
ATP_MATCHES_2020_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2020.csv'
ATP_RANKINGS_CURRENT_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_current.csv'
ATP_RANKINGS_10S_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_10s.csv'
ATP_PLAYERS_CSV_URL = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv'
# URL REGION END

# FILE REGION BEGIN
ROOT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

PLAYERS_2018_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/players_2018.csv')
PLAYERS_2019_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/players_2019.csv')
PLAYERS_2020_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/players_2020.csv')
PLAYERS_ALL_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/players_all.csv')

MATCHES_2018_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/matches_2018.csv')
MATCHES_2019_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/matches_2019.csv')
MATCHES_2020_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/matches_2020.csv')
MATCHES_ALL_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/matches_all.csv')

TOURNAMENTS_2018_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/tournaments_2018.csv')
TOURNAMENTS_2019_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/tournaments_2019.csv')
TOURNAMENTS_2020_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/tournaments_2020.csv')
TOURNAMENTS_ALL_CSV_PATH = os.path.join(ROOT_DIR_PATH, 'csv/tournaments_all.csv')
# FILE REGION END
