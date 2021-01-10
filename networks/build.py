from typing import Set

from loguru import logger
from networkx import Graph, write_gexf

from config import PLAYERS_ALL_CSV_PATH, MATCHES_ALL_CSV_PATH
from data_manipulation import load_data
from models import Match, Player


@logger.catch(reraise=True)
def build_network(players: Set[Player], matches: Set[Match], name='N/A') -> Graph:
    network = Graph(name=name)
    for player in players:
        network.add_node(player.player_id, label=f'{player.first_name} {player.last_name}',
                         first_name=player.first_name, last_name=player.last_name,
                         country_code=player.country_code, current_rank=player.current_rank,
                         current_points=player.current_points)
    for match in matches:
        if network.has_edge(*match):
            network.get_edge_data(*match)['weight'] = network.get_edge_data(*match)['weight'] + 1
        else:
            network.add_edge(*match, weight=1)
    return network


players_ = load_data(PLAYERS_ALL_CSV_PATH)
matches_ = load_data(MATCHES_ALL_CSV_PATH)
network_ = build_network(players_, matches_, name="test")
write_gexf(network_, "test.gexf")
