import urllib.parse
import requests

#MapQuest API Main URL
MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
#API key used to access the MapQuest API.
KEY = "74W0oLyxXK4C9GKbl8mr6l7y5eL28T2F"
#Dictionary that stores the available units of measurement and their equivalence in miles.
UNITS = {"1": ("kilometers", 1.61), "2": ("meters", 1609.34), "3": ("miles", 1), "4": ("feet", 5280), "5": ("yards", 1760)}

def get_directions(orig, dest, units):
    """
    Function that uses the MapQuest API to get the distance, 
    duration and maneuvers needed to get from the source location 
    to the destination location. This function calls the parse_json() 
    function to parse the JSON data returned by the API and calls the
    print_directions() function to print the results.

    """
    url = MAIN_API + urllib.parse.urlencode({"key": KEY, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        distance, duration, maneuvers = parse_json(json_data, units)
        print_directions(orig, dest, distance, duration, maneuvers, units)
    else:
        handle_error(json_status)

def parse_json(json_data, units):
    """
    Function that parses the JSON data returned by the MapQuest 
    API and returns the distance, duration and maneuvers required 
    in the units specified by the user.

    """
    distance = json_data["route"]["distance"] * UNITS[units][1]
    duration = json_data["route"]["formattedTime"]
    maneuvers = json_data["route"]["legs"][0]["maneuvers"]
    for man in maneuvers:
        man["distance"] *= UNITS[units][1]
    return distance, duration, maneuvers

def print_directions(orig, dest, distance, duration, maneuvers, units):
    """
    Function that prints the necessary instructions to get 
    from the origin location to the destination location, 
    including the estimated distance and duration of the trip, 
    as well as the necessary maneuvers.

    """
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
    """
    Function that handles errors returned by the MapQuest
    API and displays an error message accordingly.

    """
    print("*" * 16)
    if json_status == 402:
        print(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
    elif json_status == 611:
        print(f"Status Code: {json_status}; Missing an entry for one or both locations.")
    else:
        print(f"For Status Code: {json_status}; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
    print("*" * 16, "\n")

# The while True block is responsible for prompting the 
# user to enter the start location, the destination location 
# and the selection of units of measurement.
while True:
    orig = input("Starting Location: ")
    if orig in ("quit", "q"):
        break
    dest = input("Destination: ")
    if dest in ("quit", "q"):
        break
    while True:
        print("Select units:")
        for key, value in UNITS.items():
            print(f"{key}. {value[0]}")
        units = input("Enter unit number: ")
        if units in UNITS:
            break
        print("Invalid selection. Please enter a valid unit number.")
    get_directions(orig, dest, units)
