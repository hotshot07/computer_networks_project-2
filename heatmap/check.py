import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import time
import random

import geopandas as gpd
import descartes
from shapely.geometry import Point, Polygon

irelandMap = gpd.read_file(
    'Ireland/Counties__OSi_National_Statutory_Boundaries__Generalised_20m.shp')


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

irelandMap.plot()


plt.show()

# mergedData = irelandMap.set_index(‘NAME’).join(data_for_map.set_index('county'))
