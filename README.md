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

Activate with 
```bash
fastapi dev
```

main.py contains the main application, which uses the router found in routers/graph_router.py for manipulating the graph and its locations (creating a location or a road and finding the shortest path between two locations) and the router found in
routers/delivery_router.py for operations realting to deliveries (creating drivers and creating and assigning requests)

Also included is a demo_requests.py script. Use
```bash
python -m demos.demo_requests
```
to run it.