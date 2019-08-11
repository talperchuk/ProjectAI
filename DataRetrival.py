import requests
import json
import pandas as pd
import numpy as np
from DataProcess import *


apiToken = 'ApiToken f058958a-d8bd-47cc-95d7-7ecf98610e47'


def getStations(station=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/',
                            headers={'Authorization': apiToken}) if station == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}'.format(station),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/stations_data.json".format(file_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationDailyData(station, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily'.format(station, channel),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_daily.json".format(file_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyData(station, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly'.format(station),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly'.format(station, channel),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_monthly.json".format(file_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationDailyDataForDate(station, year, month, day, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/daily/{}/{}/{}'.format(station, year, month, day),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/daily/{}/{}/{}'.format(station, channel, year, month, day),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}-{}.json".format(file_name, year, month, day), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationMonthlyDataForMonth(station, year, month, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data/monthly/{}/{}'.format(station, year, month),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}/monthly/{}/{}'.format(station, channel, year, month),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}.json".format(file_name, year, month), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()


def getStationRangeData(station, start_year, start_month, start_day, end_year, end_month, end_name, channel=-1, file_name=""):
    response = requests.get('https://api.ims.gov.il/v1/envista/stations/{}/data?from={}/{}/{}&to={}/{}/{}'.format(station, start_year, start_month, start_day, end_year, end_month, end_name),
                            headers={'Authorization': apiToken}) if channel == -1 else requests.get(
        'https://api.ims.gov.il/v1/envista/stations/{}/data/{}?from={}/{}/{}&to={}/{}/{}'.format(station, channel, start_year, start_month, start_day, end_year, end_month, end_name),
        headers={'Authorization': apiToken})

    if file_name != "":
        with open("./data/{}_{}-{}-{}-{}-{}-{}.json".format(file_name, start_year, start_month, start_day, end_year, end_month, end_name), 'w') as jsonTarget:
            json.dump(response.json(), jsonTarget)
    return response.json()
