import graph_algos
import dispatch
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

class Location(BaseModel):
    name: str

class Road(BaseModel):
    source: Location
    destination: Location
    distance: float

class Driver(BaseModel):
    name: str
    location: Location

app = FastAPI()

dispatcher = dispatch.Dispatcher(graph=graph_algos.Graph())
locations = dispatcher.graph
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


    
    


