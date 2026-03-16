from fastapi import FastAPI
from .models import *
from .routers import graph_router
from .routers import delivery_router
from . import dependencies

app = FastAPI()

app.include_router(graph_router.router)

app.include_router(delivery_router.router)

locations = dependencies.get_locations()
dispatcher = dependencies.get_dispatcher()

@app.get("/")
def root():
    return {"graph": locations.adjs, "drivers": dispatcher.drivers}
