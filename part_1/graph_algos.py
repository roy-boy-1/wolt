import heapq

class Graph:

    def __init__(self, adjs=None):
        self.adjs = adjs if adjs is not None else {}

    def location_exists(self, location):
        return location in self.adjs
    
    def validate_location(self, location):
        if not self.location_exists(location):
            raise KeyError(f"location {location} does not exist")

    def add_location(self, name):
        if not self.location_exists(name):
            self.adjs[name] = {}
        else:
            raise ValueError(f"location {name} already exists")
    
    
    
    
    def road_exists(self, source, destination):
        return (self.location_exists(source) and
                 self.location_exists(destination) and 
                 destination in self.adjs[source])
    
    def validate_road(self, source, destination):
        if not self.road_exists(source, destination):
            raise KeyError(f"road ({source}, {destination}) does not exist")
    
    def add_road(self, source, destination, distance):
        self.validate_location(source)
        self.validate_location(destination)
        if distance <= 0:
            raise ValueError(f"distance has to be positive, {distance} is not")
        elif self.road_exists(source, destination):
            raise ValueError(f"road ({source}, {destination}) already exists")
        else:
            self.adjs[source][destination] = distance
    
    
    def remove_road(self, source, destination):
        self.validate_road(source, destination)
        del self.adjs[source][destination]
    
    def is_blocked(self, source, destination):
        self.validate_road(source, destination)
        return self.adjs[source][destination] < 0
    
    def block_road(self, source, destination):
        self.validate_road(source, destination)
        if self.is_blocked(source, destination):
            raise ValueError(f"road ({source}, {destination}) is already blocked")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def unblock_road(self, source, destination):
        self.validate_road(source, destination)
        if not self.is_blocked(source, destination):
            raise ValueError(f"road ({source}, {destination}) is not blocked")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def get_neighbors(self, location):
        self.validate_location(location)
        return {neighbor: distance for neighbor, distance in
                self.adjs[location].items() if distance > 0}
        

class PathFinder:

    def __init__(self, graph: Graph):
        self.graph = graph
    
    def dijkstra(self, start, end):
        self.graph.validate_location(start)
        self.graph.validate_location(end)
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
            raise ValueError(f"no valid path between {start} and {end}")
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