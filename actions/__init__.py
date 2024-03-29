from statistics import mean

import pandas as pd
from loguru import logger
from networkx import Graph
from pandas import DataFrame

from config import AGGREGATE_NETWORK_GEXF_PATH
from networks import load_network


@logger.catch(reraise=True)
def write_csv(path):
    def decorator(function):
        def wrapper(*args, **kwargs):
            source = function(*args, **kwargs)
            data = [x for x in source]
            df = DataFrame(data)
            df.to_csv(path, index=False)
            logger.info(f'Results for {function.__name__} written to {path}.')
            return source

        return wrapper

    return decorator


@write_csv('csv/task1.csv')
def task_1():
    """
    What's the average number of players per each player
    """
    network = load_network(AGGREGATE_NETWORK_GEXF_PATH)
    ret = []
    for player_id in network.nodes():
        node = network.nodes[player_id]
        weights = [network[player_id][adj]['weight'] for adj in network[player_id]]
        ret.append({
            'player_id': player_id,
            'first_name': node['first_name'],
            'last_name': node['last_name'],
            'average_opponents': round(sum(weights) / 3, 3)
        })
    return sorted(ret, key=lambda x: x['average_opponents'], reverse=True)


@write_csv('csv/task2.csv')
def task_2():
    """
    Which players have played against the most other players
    """
    network = load_network(AGGREGATE_NETWORK_GEXF_PATH)
    ret = []
    for player_id in network.nodes():
        node = network.nodes[player_id]
        ret.append({
            'player_id': player_id,
            'first_name': node['first_name'],
            'last_name': node['last_name'],
            'degree': len(network[player_id])
        })
    return sorted(ret, key=lambda x: x['degree'], reverse=True)


@write_csv('csv/task3.csv')
def task3():
    pass
