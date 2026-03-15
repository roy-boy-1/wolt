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
    
class Driver:
    
    def __init__(self, driver_id, name, current_location=None, available=True, assigned_requests=None):
        self.driver_id = driver_id
        self.name = name
        self.current_location = current_location
        self.available = available
        if assigned_requests is not None:
            self.assigned_requests = assigned_requests
        else:
            self.assigned_requests = []
    
    def assign_request(self, request):
        self.assigned_requests.append(request)

    def complete_request(self, request):
        self.assigned_requests.remove(request)
    
    def move_to(self, location):
        self.current_location = location

class DeliveryRequest:
    
    def __init__(self, request_id, pickup_location, dropoff_location, created_at, status="pending"):
        self.request_id = request_id
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.status = status
        self.created_at = created_at

class Dispatcher:

    def __init__(self, graph, drivers=None, requests = None):
        self.graph = graph
        if drivers is None:
            self.drivers = []
        else:
            self.drivers = drivers
        
        if requests is None:
            self.requests = {}
        else:
            self.requests = requests
    
    def assign_request(self, request):
        path_finder = PathFinder(self.graph)
        pickup_distances = {}
        if not self.drivers:
            raise ValueError("No drivers available")
        i = 0
        while not self.drivers[i].available:
            i+=1
        if (i == len(self.drivers)):
            raise ValueError("No drivers available")
        closest_driver = self.drivers[i]
        shortest = path_finder.shortest_distance(closest_driver.current_location, request.pickup_location)
        for driver in self.drivers[i+1:]:
            if driver.available:
                curr_distance = path_finder.shortest_distance(driver.current_location, request.pickup_location)
                if curr_distance < shortest:
                    shortest = curr_distance
                    closest_driver = driver
        closest_driver.assign_request(request)
        request.status = "assigned"
        self.requests[request] = closest_driver
    
    def get_active_requests(self):
        return self.requests

    def get_driver_assignments(self, driver_id):
        driver_exists = False
        for driver in self.drivers:
            if driver.driver_id == driver_id:
                driver_exists = True
                return driver.assigned_requests
        if not driver_exists:
            raise KeyError("No driver with provided driver_id")
        




 






    
    


            