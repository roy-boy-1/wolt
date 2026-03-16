from fastapi import APIRouter, HTTPException, status
from ..models import *
from .. import dependencies

router = APIRouter()
locations = dependencies.get_locations()
path_finder = dependencies.get_path_finder()

@router.post("/locations/", status_code=status.HTTP_201_CREATED)
def add_location(location: Location):
    try:
        locations.add_location(location.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    return location

@router.post("/roads/", status_code=status.HTTP_201_CREATED)
def add_road(road: Road):
    source, destination = road.source.name, road.destination.name
    try:
        locations.add_road(source, destination, road.distance)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=str(e))
    except ValueError as e:
        if road.distance <= 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                 detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=str(e))
    return road

@router.get("/path", status_code=status.HTTP_200_OK)
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
