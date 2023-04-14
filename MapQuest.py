import urllib.parse
import requests

MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "74W0oLyxXK4C9GKbl8mr6l7y5eL28T2F"

UNITS = {"1": ("kilometers", 1.61), "2": ("meters", 1609.34), "3": ("miles", 1)}

def get_directions(orig, dest, units):
    url = MAIN_API + urllib.parse.urlencode({"key": KEY, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        distance, duration, maneuvers = parse_json(json_data, units)
        print_directions(orig, dest, distance, duration, maneuvers, units)
    else:
        handle_error(json_status)

def parse_json(json_data, units):
    distance = json_data["route"]["distance"] * UNITS[units][1]
    duration = json_data["route"]["formattedTime"]
    maneuvers = json_data["route"]["legs"][0]["maneuvers"]
    for man in maneuvers:
        man["distance"] *= UNITS[units][1]
    return distance, duration, maneuvers

def print_directions(orig, dest, distance, duration, maneuvers, units):
    unit = UNITS[units][0]
    print("\n" + "=" * 40)
    print(f"DIRECTIONS FROM {orig.upper()} TO {dest.upper()}")
    print("=" * 40)
    print(f"Distance: {distance:.2f} {unit}")
    print(f"Duration: {duration}")
    print("=" * 40)
    print("DIRECTIONS:")
    for idx, man in enumerate(maneuvers, start=1):
        print(f"{idx:>2}. {man['narrative']} ({man['distance']:.2f} {unit})")
    print("=" * 40, "\n")

def handle_error(json_status):
    print("*" * 16)
    if json_status == 402:
        print(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
    elif json_status == 611:
        print(f"Status Code: {json_status}; Missing an entry for one or both locations.")
    else:
        print(f"For Status Code: {json_status}; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
    print("*" * 16, "\n")

while True:
    orig = input("Starting Location: ")
    if orig in ("quit", "q"):
        break
    dest = input("Destination: ")
    if dest in ("quit", "q"):
        break
    while True:
        units = input("Select units (1 for kilometers, 2 for meters, 3 for miles): ")
        if units in UNITS:
            break
        print("Invalid selection. Please enter 1, 2, or 3.")
    get_directions(orig, dest, units)
