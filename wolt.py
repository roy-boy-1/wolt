class Graph:

    def __init__(self, adjs=None):
        self.adjs = adjs if adjs is not None else {}

    def add_location(self, name):
        if not self.adjs.get(name):
            self.adjs[name] = {}
        else:
            raise ValueError("location provided already exists")
    
    def add_road(self, source, destination, distance):
        if not self.adjs.get(source) or not self.adjs.get(destination):
            raise KeyError("one or more of the locations does not exist")
        elif distance <= 0:
            raise ValueError("distance has to be positive")
        else:
            self.adjs[source][destination] = distance
    
    def _road_exists(self, source, destination):
        return (self.adjs.get(source) and self.adjs.get(destination)
             and self.adjs[source].get(destination))
    
    def remove_road(self, source, destination):
        if not self._road_exists(source, destination):
            raise KeyError("road does not exist")
        else:
            del self.adjs[source][destination]
    
    def block_road(self, source, destination):
        if not self._road_exists(source, destination):
            raise KeyError("road does not exist")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def unblock_road(self, source, destination):
        if not self._road_exists(source, destination):
            raise KeyError("road does not exist")
        elif not self._is_blocked(source, destination):
            raise ValueError("road is not blocked")
        else:
            self.adjs[source][destination] = -self.adjs[source][destination]
    
    def get_neighbors(self, location):
        if not self.adjs.get(location): 
            raise KeyError("location does not exist")
        else:
            return {neighbor: distance for neighbor, distance in self.adjs[location].items() if distance > 0}
        

    


    
    


            