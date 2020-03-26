import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import time
import random


#--------------------Data Cleaning --------------------
#------------Used API to get longitude and latitute----
# Exported the data so I dont have to use the API again and again

# from opencage.geocoder import OpenCageGeocode
# key = 'Insert_API_Key'
# geocoder = OpenCageGeocode(key)

# country = 'Ireland'

# data = pd.read_csv('irelandCensus.csv')
# data = data.drop(['Both sexes'], axis=1)
# data['Density'] = data['4761865'] / 4761865

# latitude_list = []
# longitude_list = []

# for index, row in data.iterrows():
#     state = row['State']
#     query = str(state) + ',' + str(country)
#     result = geocoder.geocode(query)
#     lati = result[0]['geometry']['lat']
#     longi = result[0]['geometry']['lng']
#     latitude_list.append(lati)
#     longitude_list.append(longi)
#     print(str(lati) + ' ' + str(longi))
#     time.sleep(2)

# data['Latitude'] = latitude_list
# data['Longitude'] = longitude_list

# data.to_csv(r'/home/hotshot/Desktop/ModifiedData.csv', index=False, header=True)

# -----------------------End of data cleaning------------------------------

# I've genrated the data needed, now gonna use the ModifiedData.csv for rest of the program

#-------------------------Generating the heatmap -------------------------------------

# Using the modified data now, generated from the section above
modData = pd.read_csv('ModifiedData.csv')

# renaing the population
modData = modData.rename(columns={"4761865": "Population"})

NumberOfClients = 2500

clients = []
county = []
latituteCl = []
longitudeCl = []
affected = []

sigma = 0.14


def makeDataForState(numberOfPeople):

    for i in range(len(numberOfPeople)):
        for j in range(numberOfPeople[i]):
            state = modData.loc[i, 'State']
            clientName = 'client' + str(j) + str(state)
            lati = modData.loc[i, 'Latitude']
            longi = modData.loc[i, 'Longitude']
            newlati = np.random.normal(lati, sigma)
            newlongi = np.random.normal(longi, sigma)
            affectedcorona = random.choice(range(2))

            clients.append(clientName)
            county.append(state)
            latituteCl.append(newlati)
            longitudeCl.append(newlongi)
            affected.append(affectedcorona)


numberOfPeople = (modData['Density'] * NumberOfClients).astype(int)
numberOfPeople = numberOfPeople.tolist()

makeDataForState(numberOfPeople)

clientDict = {
    'Client': clients,
    'County': county,
    'Latitude': latituteCl,
    'Longitude': longitudeCl,
    'Affected': affected
}

clientData = pd.DataFrame(clientDict)

clientData.plot(kind='scatter', x='Longitude', y='Latitude',
                alpha=0.5, c='Affected', cmap=plt.get_cmap("jet"), colorbar=True)
plt.show()
