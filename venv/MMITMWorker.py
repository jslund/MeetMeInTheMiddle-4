def convert_to_coordinates(address, lat_list, long_list):
    import requests,os
    api_key = os.environ.get("api_key")
    geocode_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=" + api_key).json()

    long_lat = geocode_request['results'][0]['geometry']['location']

    lat_list.append(long_lat['lat'])
    long_list.append(long_lat['lng'])
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
    import requests, time, os
    api_key = os.environ.get("api_key")
    # Search for nearby restaurants
    search = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(central_coord['lat']) + "," + str(
            central_coord['long']) + "&radius=1500&type=restaurant&key=" + api_key).json()
    if search['next_page_token']:

        search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(
            central_coord['lat']) + "," + str(central_coord['long']) + "&radius=1500&pagetoken=" + search[
                         'next_page_token'] + "&type=restaurant&key=" + api_key

        time.sleep(1)

        search_page_2 = requests.get(search_url).json()

        search['results'] = search['results'] + search_page_2['results']
        try:
            search['next_page_token'] = search_page_2['next_page_token']
        except:
            print("")
    return search


def travel_time_finder(coordinate_list, central_coord):
    import requests,os
    citymapper_api_key = os.environ.get("citymapper_api_key")
    travel_times = []
    for address in coordinate_list:
        start_coord = str(coordinate_list[address]['lat']) + "%2C" + str(coordinate_list[address]['lng'])

        coordinate_list[address]['travel_time'] = requests.get(
            "https://developer.citymapper.com/api/1/traveltime/?startcoord=" + start_coord + "&endcoord=" +
            central_coord['coord'] + "&key=" + citymapper_api_key).json()
        travel_times.append(coordinate_list[address]['travel_time']['travel_time_minutes'])
    return travel_times
