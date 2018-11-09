import requests,os,time, statistics


def convert_to_coordinates(address):
    api_key = os.environ.get("api_key")
    geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=" + api_key).json()

    long_lat = geocode_request['results'][0]['geometry']['location']

    long_lat = {str(k):str(v)for k,v in long_lat.items()}


    #lat_list.append(long_lat['lat'])
    #long_list.append(long_lat['lng'])
    return long_lat


def central_point_calculator(lat_list, long_list):
    central_lat = sum(lat_list) / len(lat_list)
    central_long = sum(long_list) / len(long_list)

    central_coord = {}
    central_coord['lat'] = central_lat
    central_coord['long'] = central_long
    central_coord['coord'] = str(central_lat) + "%2C" + str(central_long)
    return central_coord


def restaurant_finder(central_coord):
    api_key = os.environ.get("api_key")
    # Search for nearby restaurants
    search = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + central_coord +"&radius=1500&type=restaurant&key=" + api_key).json()
    if search['next_page_token']:

        search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + central_coord + "&radius=1500&pagetoken=" + search[
                         'next_page_token'] + "&type=restaurant&key=" + api_key

        time.sleep(1)

        search_page_2 = requests.get(search_url).json()

        search['results'] = search['results'] + search_page_2['results']
        try:
            search['next_page_token'] = search_page_2['next_page_token']
        except:
            print("")
    return search


def travel_time_finder(coordinate_list):
    api_key = os.environ.get('api_key')

    #coordinate_list = ["w53nw", "nw53dn", "ec2r8ah"]
    desirable_locations = ['Birmingham, UK', 'Manchester', 'London', 'Sheffield', 'Knaresborough', 'Brighton,uk', 'Leeds,uk', 'Glasgow,uk', 'Newcastle,uk', 'Bristol,uk']

    coordinates_string = "|"
    coordinates_string = coordinates_string.join(coordinate_list)

    desirable_locations_string = "|"
    desirable_locations_string = desirable_locations_string.join(desirable_locations)

    travel_times = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json?&origins={}&destinations={}&mode=transit&region=gb&key={}".format(
            coordinates_string, desirable_locations_string, api_key)).json()

    return travel_times

def location_selector(travel_times):
    destinations = dict.fromkeys(travel_times['destination_addresses'])

    for k, destination in enumerate(destinations):
        destinations[destination] = dict.fromkeys(travel_times['origin_addresses'])
        for i, origin in enumerate(destinations[destination]):
            destinations[destination][origin] = travel_times['rows'][i]['elements'][k]['duration']['value']

    average_times = {}

    for destination in destinations:
        average_times[destination] = statistics.mean(destinations[destination].values())

    best_location = {}

    best_location['location'] = min(average_times, key=average_times.get)
    best_location['average_time'] = average_times[best_location['location']]
    best_location['travel_times'] = {str(k):str((int(v)/60)) for k,v in destinations[best_location['location']].items()}

    return best_location
