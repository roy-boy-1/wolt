from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from .part_1 import dispatch
from .part_1 import graph_algos



class Location(BaseModel):
    name: str

class Road(BaseModel):
    source: Location
    destination: Location
    distance: float

class Driver(BaseModel):
    name: str
    location: Location

class DeliveryRequest(BaseModel):
    pickup_location: Location
    dropoff_location: Location


app = FastAPI()

dispatcher = dispatch.Dispatcher(graph=graph_algos.Graph())
locations = dispatcher.graph
path_finder = graph_algos.PathFinder(locations)
num_of_drivers = 0
num_of_requests = 0

@app.get("/")
def root():
    return {"graph": locations.adjs, "drivers": dispatcher.drivers}

@app.post("/locations/", status_code=status.HTTP_201_CREATED)
def add_location(location: Location):
    try:
        locations.add_location(location.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    return location

@app.post("/roads/", status_code=status.HTTP_201_CREATED)
def add_road(road: Road):
    source, destination = road.source.name, road.destination.name
    try:
        locations.add_road(source, destination, road.distance)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        if road.distance <= 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return road
    
@app.post("/drivers/", status_code=status.HTTP_201_CREATED)
def add_driver(driver: Driver):
    global num_of_drivers
    name, location = driver.name, driver.location.name
    try:
        dispatcher.add_driver(
            dispatch.Driver(driver_id=num_of_drivers, name=name, current_location=location)
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    num_of_drivers += 1
    return driver

@app.get("/path", status_code=status.HTTP_200_OK)
def get_shortest_path(start: str, end: str):
    try:
        path = path_finder.shortest_path(start, end)
        distance = path_finder.shortest_distance(start, end)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    return {"path": path.split('->'),
            "distance": distance}

@app.post("/requests", status_code=status.HTTP_201_CREATED)
def add_request(request: DeliveryRequest):
    global num_of_requests
    pickup = request.pickup_location.name
    dropoff = request.dropoff_location.name
    request_to_add = dispatch.DeliveryRequest(num_of_requests, pickup,
                                                  dropoff, datetime.now())
    try:
        dispatcher.add_request(request_to_add)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    num_of_requests += 1 
    return request
    

@app.post("/assign/{request_id}", status_code=status.HTTP_201_CREATED)
def assign_request(request_id: int):
    required_request = None
    for request in dispatcher.requests:
        if request.request_id == request_id:
            required_request = request
    if required_request == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no request with corresponding request id")
    try: 
        dispatcher.assign_request(required_request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    
    assigned_driver = dispatcher.requests[required_request]
    return {
        "driver": dispatcher.requests[required_request],
        "route_to_pickup": path_finder.shortest_path(
            assigned_driver.current_location,
            required_request.pickup_location).split("->"),
        "route_to_dropoff": path_finder.shortest_path(
            required_request.pickup_location, 
            required_request.dropoff_location
        ).split("->")
    }
    

