import json
import os
import zipfile

import requests



def load_data(filepath):
    # js_obj = open(filepath, "r")
    # p_obj = json.load(js_obj)
    p_obj = json.loads(filepath)
    return p_obj

def get_bars_json(url_destination):
    # url = 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=84505'
    session = requests.Session()
    session.proxies.update({'http': 'xz.avp.ru:8080', 'https': 'xz.avp.ru:8080', })
    session_result = session.get(url_destination)
    if os.path.isfile('temp_arch'):
        os.remove('temp_arch')
    with open('temp_arch', mode='bx') as temp:
        temp.write(session_result.content)
    return "temp_arch"

def zip_to_json(arch):
    with zipfile.ZipFile(arch) as zf:
        internal_file = zf.namelist()[0]
        # print (zf.read(internal_file))
        internal_file_text = zf.read(internal_file).decode('Windows-1251')

    return internal_file_text



def get_biggest_bar(p_obj):
    max = 0
    address = None
    id = None
    biggest_bar_list = []
    for i in p_obj:
        if i['SeatsCount'] > max:
            max = i['SeatsCount']
            address = i['Address']
            id = i['ID']
            biggest_bar_list.clear()
            elem_dict = {id: (max, address)}
            biggest_bar_list.append(elem_dict)
        elif i['SeatsCount'] == max:
            address = i['Address']
            id = i['ID']
            elem_dict = {id: (max, address)}
            biggest_bar_list.append(elem_dict)
    return biggest_bar_list



def get_smallest_bar(p_obj):
    min = p_obj[0]['SeatsCount']
    address = None
    id = None
    smallest_bar_list = []
    for i in p_obj:
        if i['SeatsCount'] < min:
            min = i['SeatsCount']
            address = i['Address']
            id = i['ID']
            smallest_bar_list.clear()
            elem_dict = {id: (min, address)}
            smallest_bar_list.append(elem_dict)
        elif i['SeatsCount'] == min:
            address = i['Address']
            id = i['ID']
            elem_dict = {id: (min, address)}
            smallest_bar_list.append(elem_dict)
    return smallest_bar_list



def get_closest_bar(p_obj, longitude, latitude):
    address = None
    id = None
    min_distance = p_obj[0]['geoData']['coordinates'][0]*p_obj[0]['geoData']['coordinates'][0] + p_obj[0]['geoData']['coordinates'][1]*p_obj[0]['geoData']['coordinates'][1]
    nearest_bar_list = []
    for i in p_obj:
        if (i['geoData']['coordinates'][0]-latitude)*(i['geoData']['coordinates'][0]-latitude) + (i['geoData']['coordinates'][1]-longitude)*(i['geoData']['coordinates'][1]-longitude) < min_distance:
            min_distance = (i['geoData']['coordinates'][0]-latitude)*(i['geoData']['coordinates'][0]-latitude) + (i['geoData']['coordinates'][1]-longitude)*(i['geoData']['coordinates'][1]-longitude)
            address = i['Address']
            id = i['ID']
            nearest_bar_list.clear()
            elem_dict = {id: (min_distance, address)}
            nearest_bar_list.append(elem_dict)
        elif (i['geoData']['coordinates'][0]-latitude)*(i['geoData']['coordinates'][0]-latitude) + (i['geoData']['coordinates'][1]-longitude)*(i['geoData']['coordinates'][1]-longitude) == min_distance:
            address = i['Address']
            id = i['ID']
            elem_dict = {id: (min_distance, address)}
            nearest_bar_list.append(elem_dict)
    return nearest_bar_list





if __name__ == '__main__':

    # p = load_data('sample.json')
    # print( p[0]['geoData']['coordinates'][0]*p[0]['geoData']['coordinates'][0])

    bars_json_destination = get_bars_json('https://op.mos.ru/EHDWSREST/catalog/export/get?id=84505')
    sample_json = zip_to_json(bars_json_destination)

    lat = 55.6312211
    long = 37.4804456

    my_list_biggest =  get_biggest_bar(load_data(sample_json))
    my_list_smallest = get_smallest_bar(load_data(sample_json))
    my_list_nearest = get_closest_bar(load_data(sample_json), lat, long)

    #print('The biggest bar. ID: %s; seats: %d; address: %s' % (id, max, address))


    print ('Biggest: ', my_list_biggest)
    print ('Smallest: ', my_list_smallest)
    print ('Nearest: ', my_list_nearest)

    # for i in my_list:
    #     for key in i:
    #         print(key, i[key])
        #print('The biggest bar. ID: %s; seats: %d; address: %s' % (key, my_list[key].[0], address))


