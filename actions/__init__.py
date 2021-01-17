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


@write_csv('task1.csv')
def task_1(network: Graph):
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
    return tuple((sorted(ret, key=lambda x: x['average_opponents'], reverse=True)))


network_ = load_network(AGGREGATE_NETWORK_GEXF_PATH)
print(task_1(network_))
