import requests
import json
def add_loc(loc):

    url = r"http://127.0.0.1:8000/locations"
    location = {
        "name": loc
    }

    response = requests.post(url, json=location)

    print(response.status_code)
    print(response.json())

def add_road(s, de, d):
    url = r"http://127.0.0.1:8000/roads"
    road = {
        "source": s,
        "destination": de,
        "distance": d,
    }

    response = requests.post(url, json=road)

    print(response.status_code)
    print(response.json())

def add_driver(name, location):
    url = r"http://127.0.0.1:8000/drivers"
    driver = {
        "name": name,
        "location": location,
    }

    response = requests.post(url, json=driver)

    print(response.status_code)
    print(response.json())

def add_request(pickup, dropoff):
    url = r"http://127.0.0.1:8000/requests"
    request = {
        "pickup_location": {"name": pickup},
        "dropoff_location": {"name": dropoff},
    }

    response = requests.post(url, json=request)

    print(response.status_code)
    print(response.json())

def assign_request(id):
    url = f"http://127.0.0.1:8000/assign/{id}"
    response = requests.post(url)
    print(response.status_code)
    print(response.json())

add_loc("A")
add_loc("B")
add_loc("C")
add_loc("B")

add_road({"name": "A"}, {"name": "B"}, 3)
add_road({"name": "A"}, {"name": "B"}, 3)

add_driver("Roy", location={"name": "A"})
add_driver("Roy", location={"name": "B"})

add_request("A", "B")

assign_request(0)


