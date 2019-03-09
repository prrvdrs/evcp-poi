import json
import geopy.distance
import csv
import os
import re
import time
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

'''
Create new file that will contain the parsed data
'''

csvfile = open('data/coordinates_PoI.csv', 'w')
writer = csv.writer(csvfile, delimiter=',',lineterminator='\n',quotechar = '"')
writer.writerow(["coordinates_cp","coordinates_pi","distance_vincenty","id","name", "place_id", "rating", "user_rating","scope", "vicinity",
                 "type_raw", "type_one", "type_two",
                 "type"])

'''
Loop folder with json files

Source:
- http://carrefax.com/new-blog/2017/1/16/draft
- https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory/30255302

'''
directory = 'C:/Users/pierr/Documents/Projects/EV_Charge_Geo/data/API_Response'

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        #f = open(filename)
        print(os.path.join(directory, filename))
        with open(os.path.join(directory, filename), errors= 'ignore') as f:
            data = json.load(f)
            #pprint(data['results'])
            for i in data['results']:
                filenameStage = re.search('(\d{1,2}\.\d+\-\d{1,2}\.\d+)', filename)
                coordinatesCP = re.sub('-', ',-', filenameStage.group(0))
                coordinatesPI = str(i['geometry']['location']['lat']) + ',' + str(i['geometry']['location']['lng'])
                distanceVincenty = geopy.distance.vincenty(coordinatesCP, coordinatesPI).km
                id = i['id']
                name = i['name']
                placeId = i['place_id']

                ''' Extract Rating '''
                if 'rating' not in i:
                    rating = ''
                else:
                    rating = i['rating']

                ''' # of User Ratings '''
                if 'user_ratings_total' not in i:
                    userRating = ''
                else:
                    userRating = i['user_ratings_total']

                scope = i['scope']
                #vicinity = i['vicinity']
                if 'vicinity' not in i:
                    vicinity = ''
                else:
                    vicinity = i['vicinity']
                typeRaw = i['types']

                googlePlacesType =    ["administrative_area_level_1", "administrative_area_level_2",
                                       "administrative_area_level_3", "administrative_area_level_4",
                                       "administrative_area_level_5", "colloquial_area", "country",
                                       "establishment", "finance", "floor", "food", "general_contractor", "geocode", "health",
                                       "intersection", "locality", "natural_feature", "neighborhood", "place_of_worship",
                                       "political", "point_of_interest", "post_box", "postal_code", "postal_code_prefix",
                                       "postal_code_suffix", "postal_town", "premise", "room", "route", "street_address",
                                       "street_number", "sublocality", "sublocality_level_4", "sublocality_level_5",
                                       "sublocality_level_3", "sublocality_level_2", "sublocality_level_1", "subpremise",
                                       "accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery",
                                       "bank",
                                       "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station",
                                       "cafe",
                                       "campground", "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery",
                                       "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist",
                                       "department_store", "doctor", "electrician", "electronics_store", "embassy",
                                       "fire_station",
                                       "florist", "funeral_home", "furniture_store", "gas_station", "gym", "hair_care",
                                       "hardware_store", "hindu_temple", "home_goods_store", "hospital", "insurance_agency",
                                       "jewelry_store", "laundry", "lawyer", "library", "liquor_store",
                                       "local_government_office",
                                       "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental",
                                       "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking",
                                       "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office",
                                       "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school",
                                       "shoe_store",
                                       "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket",
                                       "synagogue", "taxi_stand", "train_station", "transit_station", "travel_agency",
                                       "veterinary_care", "zoo"]

                ''' Google Classification 1 '''
                googlePlacesTypeOne = ["administrative_area_level_1","administrative_area_level_2",
                                       "administrative_area_level_3","administrative_area_level_4",
                                       "administrative_area_level_5","colloquial_area","country",
                                       "establishment","finance","floor","food","general_contractor","geocode","health",
                                       "intersection","locality","natural_feature","neighborhood","place_of_worship",
                                       "political","point_of_interest","post_box","postal_code","postal_code_prefix",
                                       "postal_code_suffix","postal_town","premise","room","route","street_address",
                                       "street_number","sublocality","sublocality_level_4","sublocality_level_5",
                                       "sublocality_level_3","sublocality_level_2","sublocality_level_1","subpremise"]

                ''' Google Classification 2'''

                googlePlacesTypeTwo = ["accounting","airport","amusement_park","aquarium","art_gallery","atm","bakery","bank",
                                       "bar","beauty_salon","bicycle_store","book_store","bowling_alley","bus_station","cafe",
                                       "campground","car_dealer","car_rental","car_repair","car_wash","casino","cemetery",
                                       "church","city_hall","clothing_store","convenience_store","courthouse","dentist",
                                       "department_store","doctor","electrician","electronics_store","embassy","fire_station",
                                       "florist","funeral_home","furniture_store","gas_station","gym","hair_care",
                                       "hardware_store","hindu_temple","home_goods_store","hospital","insurance_agency",
                                       "jewelry_store","laundry","lawyer","library","liquor_store","local_government_office",
                                       "locksmith","lodging","meal_delivery","meal_takeaway","mosque","movie_rental",
                                       "movie_theater","moving_company","museum","night_club","painter","park","parking",
                                       "pet_store","pharmacy","physiotherapist","plumber","police","post_office",
                                       "real_estate_agency","restaurant","roofing_contractor","rv_park","school","shoe_store",
                                       "shopping_mall","spa","stadium","storage","store","subway_station","supermarket",
                                       "synagogue","taxi_stand","train_station","transit_station","travel_agency",
                                       "veterinary_care","zoo"]
                #googlePlacesTypeThree = []


                typeOne = []
                for p in set(typeRaw).intersection(set(googlePlacesTypeOne)):
                    typeOne.append(p)
                typeTwo = []
                for q in set(typeRaw).intersection(set(googlePlacesTypeTwo)):
                    typeTwo.append(q)
                typeThree = "placeholder"


                labeling =[]
                for g in set(googlePlacesType):
                    for h in set(typeRaw):
                        if g == h:
                            x = 1
                            break
                        else:
                            x = 0
                    labeling.append(x)

                writer.writerow([coordinatesCP, coordinatesPI, distanceVincenty, id, name, placeId, rating, userRating,
                                 scope, vicinity, typeRaw, typeOne, typeTwo, labeling])
    else:
        continue
    time.sleep(1)  # limit requests per second.