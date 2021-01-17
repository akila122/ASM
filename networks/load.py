from loguru import logger
from networkx import read_gexf


@logger.catch(reraise=True)
def load_network(path):
    return read_gexf(path)
