from fastapi import APIRouter, HTTPException, status, Depends
from ..models import *
from ..part_1 import graph_algos
from .. import dependencies

router = APIRouter()


@router.post("/locations/", status_code=status.HTTP_201_CREATED)
def add_location(location: Location, locations: graph_algos.Graph = Depends(dependencies.get_locations)):
    try:
        locations.add_location(location.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    return location

@router.post("/roads/", status_code=status.HTTP_201_CREATED)
def add_road(road: Road, locations: graph_algos.Graph = Depends(dependencies.get_locations)):
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

@router.get("/path", status_code=status.HTTP_200_OK)
def get_shortest_path(start: str, end: str, path_finder: graph_algos.PathFinder = Depends(dependencies.get_path_finder)):
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