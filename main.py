"""mytask"""
import argparse, folium, math
from geopy.geocoders import Nominatim
def line_processing(line):
    """
    Returns list of film's name and place
    >>> line_processing("'*VanLifeAttila' (2016) {'Over' a Film by Attila (3.31)}    	Wells, British Columbia, Canada	(shooting Over)")
    ['*VanLifeAttila', 'Wells, British Columbia, Canada']
    """
    lst_tab = line.split("\t")
    lst_of_name_place = []
    if len(lst_tab)!=2:
        lst_tab.pop()
        place = lst_tab[-1]
    else:
        place = lst_tab[-1][:-1]
    name = lst_tab[0].split()[0][1:-1]
    lst_of_name_place.append(name)
    lst_of_name_place.append(place)
    return lst_of_name_place
def distance_calculator(lat, lon, place):
    """
    Returns distance between location of user and location of film
    >>> line_processing("'*VanLifeAttila' (2016) {'Over' a Film by Attila (3.31)}    	Wells, British Columbia, Canada	(shooting Over)")
    ['*VanLifeAttila', 'Wells, British Columbia, Canada']
    """
    geolocator = Nominatim(user_agent="labka")
    try:
        location = geolocator.geocode(place)
        lat_place = location.latitude
        lon_place = location.longitude
    except:
        try:
            name = place.split(",")[1:]
            new_name = ""
            for word in name:
                new_name += word + ","
            new_name = new_name[:-1]
            location = geolocator.geocode(new_name)
            lat_place = location.latitude
            lon_place = location.longitude
        except:
            return None
    distance = 2*6400*math.asin(math.sqrt((math.sin(lat_place/2-lat/2))**2 + math.cos(lat)*math.cos(lat_place)*(math.sin(lon_place/2 - lon/2))**2))
    return distance
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('year', type = str)
    parser.add_argument('latitude', type = float)
    parser.add_argument('longitude', type = float)
    parser.add_argument('path_to_dataset', type = str)

    args = parser.parse_args()
    year = args.year
    latitude = args.latitude
    longitude = args.longitude
    path_to_dataset = args.path_to_dataset
    # latitude = 48.314775
    # longitude = 25.082925
    # year = "2017"
    # path_to_dataset = r'C:\Users\tetia\.vscode\projects\locations1.list'
    year_str = "(" + year + ")"
    lst =[]
    with open(path_to_dataset, 'r') as file:
        for line in file:
            if year_str in line:
                lst.append(line_processing(line))
    new_lst = []
    for i in range (len(lst)):
        distance = distance_calculator(latitude, longitude, lst[i][-1])
        if distance != None:
            new_lst.append([lst[i][0], lst[i][-1], distance])
    sorted_lst = sorted(new_lst, key = lambda x: x[-1])[:10]


    map = folium.Map(location = [latitude, longitude])
    fg_list = []
    fg = folium.FeatureGroup(name = "Films")
    circle_markers = folium.FeatureGroup(name = "Circle markers")
    for i in range(len(sorted_lst)):
        geolocator = Nominatim(user_agent="labka")
        try:
            location = geolocator.geocode(sorted_lst[i][-2])
            lat = location.latitude
            lon = location.longitude
        except:
            name = sorted_lst[i][-2].split(",")[1:]
            new_name = ""
            for word in name:
                new_name += word + ","
            new_name = new_name[:-1]
            location = geolocator.geocode(new_name)
            lat = location.latitude
            lon = location.longitude
        fg.add_child(folium.Marker(location = [lat, lon], popup = sorted_lst[i][0], icon = folium.Icon(icon = "camera", color = "green")))
        circle_markers.add_child(folium.CircleMarker(location = [lat, lon], radius = 25, color = "orange", fill_color = "orange"))
    fg_list.append(fg)
    fg_list.append(circle_markers)

    location_of_user = folium.FeatureGroup(name = "location of user")
    location_of_user.add_child(folium.Marker(location = [latitude, longitude], popup = "You're here!", icon = folium.Icon(icon = "home",color = "red")))
    fg_list.append(location_of_user)

    folium.TileLayer('cartodbdark_matter').add_to(map)

    for fg in fg_list:
        map.add_child(fg)
    map.add_child(folium.LayerControl())
    map.save('Map.html')
    print("Done!")
if __name__ == "__main__":
    main()