import graph_algos, dispatch

graph = graph_algos.Graph({'A': {'B': 4, 'C': 2}, 
           'B': {'D': 5, 'A': 4, 'C': 1},
           'C': {'B': 1, 'D': 8, 'A': 2}, 
           'D': {'E': 2, 'C': 8, 'B': 5},
           'E': {'D' : 2},
           })

driver1 = dispatch.Driver(1, "Roy", "A")
driver2 = dispatch.Driver(2, "Boy", "D")

request = dispatch.DeliveryRequest(0, "B", "E", "2026-03-13")

dispatcher = dispatch.Dispatcher(graph, drivers=[driver1, driver2], requests={request: None})

dispatcher.assign_request(request)

pathfinder = graph_algos.PathFinder(graph)

assigned_driver = dispatcher.get_active_requests()[request]

print(f"The request from {request.pickup_location} to {request.dropoff_location} was assigned to driver {assigned_driver.name}.")
print(f"The route they should take to the pickup location is {pathfinder.shortest_path(assigned_driver.current_location, request.pickup_location)}.")      
print(f"Then to get to the dropoff location they should take {pathfinder.shortest_path(request.pickup_location,
      request.dropoff_location)}.")
print(f"The total distance will be {pathfinder.shortest_distance(assigned_driver.current_location,
      request.pickup_location) + pathfinder.shortest_distance(request.pickup_location,
      request.dropoff_location)}.")