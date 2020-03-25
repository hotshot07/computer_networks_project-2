import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from opencage.geocoder import OpenCageGeocode
import time


#--------------------Data Cleaning --------------------
#------------Used API to get longitude and latitute----
# Exported the data so I dont have to use the API again and again

'''
key = 'Insert_API_Key'
geocoder = OpenCageGeocode(key)

country = 'Ireland'

data = pd.read_csv('irelandCensus.csv')
data = data.drop(['Both sexes'], axis=1)
data['Density'] = data['4761865'] / 4761865

latitude_list = []
longitude_list = []

for index, row in data.iterrows():
    state = row['State']
    query = str(state) + ',' + str(country)
    result = geocoder.geocode(query)
    lati = result[0]['geometry']['lat']
    longi = result[0]['geometry']['lng']
    latitude_list.append(lati)
    longitude_list.append(longi)
    print(str(lati) + ' ' + str(longi))
    time.sleep(2)

data['Latitude'] = latitude_list
data['Longitude'] = longitude_list

data.to_csv(r'/home/hotshot/Desktop/ModifiedData.csv', index=False, header=True)

'''
