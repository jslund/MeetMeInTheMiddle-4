import requests, json, googlemaps, time, statistics

api_key = "AIzaSyByX6yhr9aQ7JcIVbzCPptcNlMLylH1Wmo"

#Request to Googles distance matrix api. Params: Origins = start location(point a), Destinations  = Location to find a point between (point b)
#location_request = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=w53nw|nw53dn|ec3p3dq&destinations=w53nw|nw53dn|ec3p3dq&mode=transit&key="+api_key).json()

lat_list = []
long_list = []
coordinate_list = dict.fromkeys(["w53nw", "nw53dn", "ec2r8ah"])

def convert_to_coordinates(address):
    geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=" + api_key).json()

    long_lat = geocode_request['results'][0]['geometry']['location']

    lat_list.append(long_lat['lat'])
    long_list.append(long_lat['lng'])
    return long_lat

for address in coordinate_list:
    coordinate_list[address] = convert_to_coordinates(address)

central_lat = sum(lat_list)/len(lat_list)
central_long = sum(long_list) / len(long_list)

central_coord = {}
central_coord['lat']=central_lat
central_coord['long']=central_long
central_coord['coord']=str(central_lat) + "%2C" + str(central_long)

#Search for nearby restaurants
search = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(central_lat)+","+str(central_long)+"&radius=1500&type=restaurant&key="+api_key).json()
if search['next_page_token']:

    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(central_lat)+","+str(central_long)+"&radius=1500&pagetoken="+search['next_page_token']+"&type=restaurant&key="+api_key

    time.sleep(1)

    search_page_2 = requests.get(search_url).json()

    search['results']= search['results']+search_page_2['results']
    try:
        search['next_page_token'] = search_page_2['next_page_token']
    except:
        print("")

citymapper_api_key = "389ed968f524f307e432cfd142122165"

travel_times = []

for address in coordinate_list:
    start_coord = str(coordinate_list[address]['lat']) + "%2C" + str(coordinate_list[address]['lng'])

    coordinate_list[address]['travel_time'] = requests.get("https://developer.citymapper.com/api/1/traveltime/?startcoord="+start_coord+"&endcoord="+central_coord['coord']+"&key="+citymapper_api_key).json()
    travel_times.append(coordinate_list[address]['travel_time']['travel_time_minutes'])






results=search['results']

results = sorted(results, key=lambda k: k['rating'], reverse=True)

for result in results:
    print(result['name'])
    print(result['rating'])


print("Average travel time of: {} minutes".format(statistics.mean(travel_times)))



print("break")




#gmaps = googlemaps.Client(key=api_key)



