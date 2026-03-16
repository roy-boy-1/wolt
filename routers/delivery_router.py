from fastapi import FastAPI, HTTPException, status, APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from ..part_1 import dispatch
from ..part_1 import graph_algos
from ..models import Driver, DeliveryRequest
from .. import dependencies

router = APIRouter()

@router.post("/drivers/", status_code=status.HTTP_201_CREATED)
def add_driver(driver: Driver, dispatcher: dispatch.Dispatcher = 
               Depends(dependencies.get_dispatcher), 
               ids =
                 Depends(dependencies.get_ids)):
    name, location = driver.name, driver.location.name
    try:
        dispatcher.add_driver(
            dispatch.Driver(driver_id=ids["drivers"], name=name, current_location=location)
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    ids["drivers"] += 1
    return driver



@router.post("/requests", status_code=status.HTTP_201_CREATED)
def add_request(request: DeliveryRequest,
                dispatcher: dispatch.Dispatcher = 
               Depends(dependencies.get_dispatcher), 
               ids = Depends(dependencies.get_ids)):
    pickup = request.pickup_location.name
    dropoff = request.dropoff_location.name
    request_to_add = dispatch.DeliveryRequest(ids["requests"], pickup,
                                                  dropoff, datetime.now())
    try:
        dispatcher.add_request(request_to_add)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    ids["requests"] += 1 
    return request
    

@router.post("/assign/{request_id}", status_code=status.HTTP_201_CREATED)
def assign_request(request_id: int,
                   dispatcher: dispatch.Dispatcher = 
               Depends(dependencies.get_dispatcher), 
               path_finder: graph_algos.PathFinder = 
               Depends(dependencies.get_path_finder)):
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