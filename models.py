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

class DeliveryRequest(BaseModel):
    pickup_location: Location
    dropoff_location: Location