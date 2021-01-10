from typing import Set

from loguru import logger
from networkx import Graph, write_gexf

from data_manipulation import load_data_csv, load_2018_dict, load_2019_dict, load_2020_dict, load_all_dict
from models import Match, Player
from config import _2018_NETWORK_GEXF_PATH, _2019_NETWORK_GEXF_PATH, _2020_NETWORK_GEXF_PATH, NOVAK_PLAYER_ID, \
    NOVAK_NETWORK_GEFX_PATH, RAFAEL_NETWORK_GEFX_PATH, RAFAEL_PLAYER_ID, ROGER_NETWORK_GEFX_PATH, ROGER_PLAYER_ID, \
    AGGREGATE_NETWORK_GEXF_PATH


@logger.catch(reraise=True)
def build_and_write_all_networks(data_2018, data_2019, data_2020, data_all):
    network_2018 = build_regular(data_2018['players'], data_2018['matches'], name='2018')
    write_gexf(network_2018, _2018_NETWORK_GEXF_PATH)
    logger.success(f'Network written to {_2018_NETWORK_GEXF_PATH}')

    network_2019 = build_regular(data_2019['players'], data_2019['matches'], name='2019')
    write_gexf(network_2019, _2019_NETWORK_GEXF_PATH)
    logger.success(f'Network written to {_2019_NETWORK_GEXF_PATH}')

    network_2020 = build_regular(data_2020['players'], data_2020['matches'], name='2020')
    write_gexf(network_2020, _2020_NETWORK_GEXF_PATH)
    logger.success(f'Network written to {_2020_NETWORK_GEXF_PATH}')

    network_all = build_regular(data_all['players'], data_all['matches'], name='all')
    write_gexf(network_all, AGGREGATE_NETWORK_GEXF_PATH)
    logger.success(f'Network written to {AGGREGATE_NETWORK_GEXF_PATH}')

    network_novak = build_ego(data_all['players'], data_all['matches'], NOVAK_PLAYER_ID)
    write_gexf(network_novak, NOVAK_NETWORK_GEFX_PATH)
    logger.success(f'Network written to {NOVAK_NETWORK_GEFX_PATH}')

    network_rafael = build_ego(data_all['players'], data_all['matches'], RAFAEL_PLAYER_ID)
    write_gexf(network_rafael, RAFAEL_NETWORK_GEFX_PATH)
    logger.success(f'Network written to {RAFAEL_NETWORK_GEFX_PATH}')

    network_roger = build_ego(data_all['players'], data_all['matches'], ROGER_PLAYER_ID)
    write_gexf(network_roger, ROGER_NETWORK_GEFX_PATH)
    logger.success(f'Network written to {ROGER_NETWORK_GEFX_PATH}')


@logger.catch(reraise=True)
def build_regular(players: Set[Player], matches: Set[Match], name='N/A') -> Graph:
    network = Graph(name=name)
    for player in players:
        _add_player_node(network, player)
    for match in matches:
        _add_match_edge(network, match)
    logger.success(f'Done building {name} network.')
    return network


@logger.catch(reraise=True)
def build_ego(players: Set[Player], matches: Set[Match], ego_id: str) -> Graph:
    ego = next(iter([player for player in players if player.player_id == ego_id]), None)
    if not ego:
        raise Exception(f'Player id not found for {ego_id}.')
    network = Graph(name=f'Ego{ego.first_name}{ego.last_name}')
    ego_matches = set(
        [match for match in matches if match.loser_id == ego.player_id or match.winner_id == ego.player_id]
    )
    alters_ids = set([
        match.loser_id for match in ego_matches if match.winner_id == ego.player_id
    ]).union(set([
        match.winner_id for match in ego_matches if match.loser_id == ego.player_id
    ]))
    alters = set([
        player for player in players if player.player_id in alters_ids
    ])
    for player in set([ego]).union(alters):
        _add_player_node(network, player)
    for match in matches:
        if match in ego_matches or match.winner_id in alters_ids and match.loser_id in alters_ids:
            _add_match_edge(network, match)
    logger.success(f'Done building {network.graph["name"]} network.')
    return network


def _add_player_node(network, player):
    network.add_node(player.player_id, label=f'{player.first_name} {player.last_name}',
                     first_name=player.first_name, last_name=player.last_name,
                     country_code=player.country_code, current_rank=player.current_rank,
                     current_points=player.current_points)


def _add_match_edge(network, match):
    if network.has_edge(*match):
        network.get_edge_data(*match)['weight'] = network.get_edge_data(*match)['weight'] + 1
    else:
        network.add_edge(*match, weight=1)
