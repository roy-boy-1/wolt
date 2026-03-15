import graph_algos

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
        path_finder = graph_algos.PathFinder(self.graph)
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