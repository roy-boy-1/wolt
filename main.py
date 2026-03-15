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


    
    


