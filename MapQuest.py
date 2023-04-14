import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "74W0oLyxXK4C9GKbl8mr6l7y5eL28T2F"

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    
    while True:
        units = input("Select units (1 for kilometers, 2 for meters, 3 for miles): ")
        if units in ['1', '2', '3']:
            break
        print("Invalid selection. Please enter 1, 2, or 3.")
    
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + url)
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print("\n" + "="*40)
        print("DIRECTIONS FROM", orig.upper(), "TO", dest.upper())
        print("="*40)
        
        print("Distance:", end=" ")
        distance = json_data["route"]["distance"]
        if units == '1':
            distance *= 1.61  # convert to kilometers
            print("{:.2f} kilometers".format(distance))
        elif units == '2':
            distance *= 1609.34  # convert to meters
            print("{:.2f} meters".format(distance))
        else:
            print("{:.2f} miles".format(distance))
        
        print("Duration:", json_data["route"]["formattedTime"])
        print("="*40)
        
        print("DIRECTIONS:")
        for idx, each in enumerate(json_data["route"]["legs"][0]["maneuvers"], start=1):
            print("{:>2}. {:>5} ({:.2f} {})".format(idx, each["narrative"], 
                                                     each["distance"] * 1.61 if units == '1' else each["distance"], 
                                                     "km" if units == '1' else "miles"))
        print("="*40, "\n")
    
    elif json_status == 402:
        print("****************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("****************\n")
    elif json_status == 611:
        print("****************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("****************\n")
    else:
        print("************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************\n")
