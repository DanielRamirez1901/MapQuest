import urllib.parse
import requests

MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "74W0oLyxXK4C9GKbl8mr6l7y5eL28T2F"

UNITS = {"1": ("kilometers", 1.61), "2": ("meters", 1609.34), "3": ("miles", 1)}

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

    url = MAIN_API + urllib.parse.urlencode({"key": KEY, "from": orig, "to": dest})
    print("URL: " + url)
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("\n" + "=" * 40)
        print(f"DIRECTIONS FROM {orig.upper()} TO {dest.upper()}")
        print("=" * 40)

        distance = json_data["route"]["distance"]
        unit, factor = UNITS[units]
        distance *= factor
        print(f"Distance: {distance:.2f} {unit}")

        print(f"Duration: {json_data['route']['formattedTime']}")
        print("=" * 40)

        print("DIRECTIONS:")
        for idx, each in enumerate(json_data["route"]["legs"][0]["maneuvers"], start=1):
            unit, factor = UNITS[units]
            distance = each["distance"] * factor
            print(f"{idx:>2}. {each['narrative']} ({distance:.2f} {unit})")
        print("=" * 40, "\n")

    else:
        print("*" * 16)
        if json_status == 402:
            print(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
        elif json_status == 611:
            print(f"Status Code: {json_status}; Missing an entry for one or both locations.")
        else:
            print(f"For Status Code: {json_status}; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("*" * 16, "\n")
