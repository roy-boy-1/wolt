import heapq

class Graph:

    def __init__(self, adjs=None):
        self.adjs = adjs if adjs is not None else {}

    def location_exists(self, location):
        return self.adjs.get(location) is not None

    def add_location(self, name):
        if not self.location_exists(name):
            self.adjs[name] = {}
        else:
            raise ValueError("location provided already exists")
    
    def add_road(self, source, destination, distance):
        if not self.location_exists(source) or not self.location_exists(destination):
            raise KeyError("one or more of the locations does not exist")
        elif distance <= 0:
            raise ValueError("distance has to be positive")
        else:
            self.adjs[source][destination] = distance
    
    def road_exists(self, source, destination):
        return (self.location_exists(source) and
                 self.location_exists(destination) and self.adjs[source].get(destination) is not None)
    
    
    def remove_road(self, source, destination):
        if not self.road_exists(source, destination):
            raise KeyError("road does not exist")
        else:
            del self.adjs[source][destination]
    
    def is_blocked(self, source, destination):
        if not self.road_exists(source, destination):
            raise KeyError("road does not exist")
        else:
            return self.adjs[source][destination] < 0
    
    def block_road(self, source, destination):
        if not self.road_exists(source, destination):
            raise KeyError("road does not exist")
        elif self.is_blocked(source, destination):
            raise ValueError("road is already blocked")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def unblock_road(self, source, destination):
        if not self.road_exists(source, destination):
            raise KeyError("road does not exist")
        elif not self.is_blocked(source, destination):
            raise ValueError("road is not blocked")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def get_neighbors(self, location):
        if not self.location_exists(location):
            raise KeyError("location does not exist")
        else:
            return {neighbor: distance for neighbor, distance in
                     self.adjs[location].items() if distance > 0}
        

class PathFinder:

    def __init__(self, graph: Graph):
        self.graph = graph
    
    def dijkstra(self, start, end):
        if (not self.graph.location_exists(start)
             or not self.graph.location_exists(end)):
            raise KeyError("one or more of the locations does not exist")
        else:
            min_heap = [(0, start)]
            distances = {location: -1 for location in self.graph.adjs}
            distances[start] = 0
            previous = {location: None for location in self.graph.adjs}

            while min_heap:
                curr_dist, curr_loc = heapq.heappop(min_heap)
                
                for n, dist in self.graph.get_neighbors(curr_loc).items():
                    if distances[n] != -1:
                        if curr_dist + dist < distances[n]:
                            distances[n] = curr_dist + dist
                            previous[n] = curr_loc
                    else:
                        distances[n] = curr_dist + dist
                        heapq.heappush(min_heap, (curr_dist + dist, n))
                        previous[n] = curr_loc
            
            if distances[end] == -1:
                raise ValueError("no valid path")
            else:
                return distances, previous
            
    def shortest_distance(self, start, end):
        return self.dijkstra(start, end)[0][end]
    
    def shortest_path(self, start, end):
        result = ""
        previous = self.dijkstra(start, end)[1]
        while previous[end] is not None:
            result += end + ">-"
            end = previous[end]
        return start + result[::-1]