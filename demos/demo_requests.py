import requests

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
        "source": {"name": s},
        "destination": {"name": de},
        "distance": d,
    }

    response = requests.post(url, json=road)

    print(response.status_code)
    print(response.json())

def add_driver(name, location):
    url = r"http://127.0.0.1:8000/drivers"
    driver = {
        "name": name,
        "location": {"name": location},
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

add_road("A", "B", 3)
add_road("A", "B", 3)
add_road("A", "C", 1)
add_road("B", "C", 1)
add_road("B", "C", 0)

add_driver("Reagan", "A")
add_driver("Brett", "B")
add_driver("Alpha-Beta", "D")

add_request("A", "B")
add_request("A", "C")
add_request("A", "D")
add_request("D", "E")

assign_request(0)
assign_request(1)
assign_request(2)
