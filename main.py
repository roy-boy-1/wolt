from fastapi import FastAPI, HTTPException, status, Depends
from .models import *
from datetime import datetime
from .part_1 import dispatch
from .part_1 import graph_algos
from .routers import graph_router
from .routers import delivery_router
from . import dependencies

app = FastAPI()

app.include_router(graph_router.router)

app.include_router(delivery_router.router)

@app.get("/")
def root(locations: graph_algos.Graph = Depends(dependencies.get_locations),
         dispatcher: dispatch.Dispatcher = Depends(dependencies.get_dispatcher)):
    return {"graph": locations.adjs, "drivers": dispatcher.drivers}


    

    

