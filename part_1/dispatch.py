from . import graph_algos

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
        self.available = False

    def complete_request(self, request):
        self.assigned_requests.remove(request)
        self.available = True
    
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

    def __init__(self, graph, drivers=None, requests=None):
        self.graph = graph

        self.drivers = []
        if drivers is not None:
            for driver in drivers:
                try:
                    self.add_driver(driver)
                except ValueError:
                    pass

        self.requests = {}
        if requests is not None:
            for request in requests:
                try:
                    self.add_request(request)
                except ValueError:
                    pass

    
    def add_driver(self, driver):
        self.graph.validate_location(driver.current_location)
        self.drivers.append(driver)

    def validate_request(self, request):
        self.graph.validate_location(request.pickup_location)
        self.graph.validate_location(request.dropoff_location)
    
    def add_request(self, request):
        self.validate_request(request)
        self.requests[request] = None

    def assign_request(self, request):
        self.validate_request(request)
        path_finder = graph_algos.PathFinder(self.graph)
        pickup_distances = {}
        if not self.drivers:
            raise ValueError("no drivers available")
        closest_driver = None
        for driver in self.drivers:
            if driver.available:
                try:
                    shortest = path_finder.shortest_distance(driver.current_location, request.pickup_location)
                    closest_driver = driver
                except ValueError:
                    pass
        if closest_driver is None:
            raise ValueError("no drivers available")
        for driver in self.drivers:
            if driver.available:
                try:
                    curr_distance = path_finder.shortest_distance(driver.current_location, request.pickup_location)
                except ValueError:
                    curr_distance = -1
                if curr_distance != -1 and curr_distance < shortest:
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
            raise KeyError(f"No driver with driver_id {driver_id}")          