from .part_1 import dispatch
from .part_1 import graph_algos

class AllData:
    def __init__(self):
        self.dispatcher = dispatch.Dispatcher(graph=graph_algos.Graph())
        self.locations = self.dispatcher.graph
        self.path_finder = graph_algos.PathFinder(self.locations)
        self.ids = {"drivers": 0, "requests": 0}

all_data = AllData()

def get_dispatcher() -> dispatch.Dispatcher:
    return all_data.dispatcher

def get_locations() -> graph_algos.Graph:
    return all_data.dispatcher.graph

def get_path_finder() -> graph_algos.PathFinder:
    return all_data.path_finder

def get_ids() -> dict:
    return all_data.ids

