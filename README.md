# Wolt
## Part 1
Wolt is a project for efficient delivery management.  

graph_algos.py contains the classes Graph and PathFinder for general graph capabilities and shortest path finding.  
dispatch.py contains the classes Driver, DeliveryRequest and Dispatcher for handling deliveries and assigning them to appropriate drivers.  

Also included is a demo.py script. Use 
```bash
python -m demos.demo 
```
to run it.

## Part 2
Wolt is now a REST API.  

main.py contains POST endpoints for adding locations, roads, drivers, delivery requests and for assigning delivery requests.  
It also contains GET endpoints, namely root for a view of the location graph and drivers and /path for getting the shortest path between two locations.  

Also included is a demo_requests.py script. Use
```bash
python -m demos.demo_requests
```
to run it.