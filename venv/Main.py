def main_function(address_list):
    import json, statistics, MMITMWorker


    #Request to Googles distance matrix api. Params: Origins = start location(point a), Destinations  = Location to find a point between (point b)
    #location_request = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=w53nw|nw53dn|ec3p3dq&destinations=w53nw|nw53dn|ec3p3dq&mode=transit&key="+api_key).json()

    lat_list = []
    long_list = []
    #coordinate_list = dict.fromkeys(["w53nw", "nw53dn", "ec2r8ah"])
    coordinate_list = dict.fromkeys(address_list)



    for address in coordinate_list:
        coordinate_list[address] = MMITMWorker.convert_to_coordinates(address, lat_list, long_list)

    central_coord = MMITMWorker.central_point_calculator(lat_list,long_list)

    search = MMITMWorker.restaurant_finder(central_coord)



    travel_times = MMITMWorker.travel_time_finder(coordinate_list, central_coord)


    results=search['results']

    results = sorted(results, key=lambda k: k['rating'], reverse=True)

    for result in results:
        print("{}, {}".format(result['name'], result['rating']))


    print("Average travel time of: {} minutes".format(statistics.mean(travel_times)))



    print("break")




    #gmaps = googlemaps.Client(key=api_key)

    return (results,travel_times)

if __name__ == '__main__':
    addresses = []
    while True:
        addresses.append(input("Enter Address"))
        if input("Done Y/N?") == "Y":
            break
    main_function(addresses)

