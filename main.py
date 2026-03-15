import graph_algos
import dispatch
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

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
    if locations.location_exists(location.name):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail="location already exists")
    locations.add_location(location.name)
    return location

@app.post("/roads/", status_code=status.HTTP_201_CREATED)
def add_road(road: Road):
    source, destination = road.source.name, road.destination.name
    if not (locations.location_exists(source) and
            locations.location_exists(destination)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="one or more of the locations does not exists")
    if locations.road_exists(source, destination):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="road already exists")
    locations.add_road(source, destination, road.distance)
    return road
    
@app.post("/drivers/", status_code=status.HTTP_201_CREATED)
def add_driver(driver: Driver):
    global num_of_drivers
    name, location = driver.name, driver.location.name
    if not locations.location_exists(location):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="location does not exist")
    dispatcher.drivers.append(dispatch.Driver(driver_id=num_of_drivers, name=name, current_location=location))
    num_of_drivers += 1
    return driver

@app.get("/path", status_code=status.HTTP_200_OK)
def get_shortest_path(start: str, end: str):
    if not (locations.location_exists(start) and locations.location_exists(end)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="one or more of the location does not exist")
    path = path_finder.shortest_path(start, end)
    distance = path_finder.shortest_distance(start, end)
    return {"path": path.split('->'),
            "distance": distance}

@app.post("/requests", status_code=status.HTTP_201_CREATED)
def add_request(request: DeliveryRequest):
    global num_of_requests
    pickup = request.pickup_location.name
    dropoff = request.dropoff_location.name
    if not (locations.location_exists(pickup) and locations.location_exists(dropoff)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="one or more of the location does not exist")
    dispatcher.requests[dispatch.DeliveryRequest(num_of_requests, pickup,
                                                  dropoff, datetime.now())] = None
    num_of_requests += 1 
    return request

